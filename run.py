"""
Entry point for running the Telegram bot.
Run this file from the project root: python run.py
"""

import asyncio
import logging
import os
import signal
import sys
import time
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.exceptions import TelegramNetworkError, TelegramServerError
from aiohttp import ClientConnectorError, ClientError
from bot.config import BOT_TOKEN, HR_GROUP_ID, COMPANY_NAME
from bot.handlers import main_handlers, application_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Lock file path for single-instance mechanism
LOCK_FILE = Path(__file__).parent / ".bot_instance.lock"


def acquire_instance_lock() -> bool:
    """
    Acquire single-instance lock.
    Returns True if lock acquired successfully, False otherwise.
    If another instance is running, it will be terminated.
    """
    current_pid = os.getpid()

    # Check if lock file exists
    if LOCK_FILE.exists():
        try:
            # Read PID from lock file
            old_pid = int(LOCK_FILE.read_text().strip())

            # Check if the process is still running
            try:
                # Signal 0 doesn't kill, just checks if process exists
                os.kill(old_pid, 0)
                # Process is still running - terminate it
                logger.warning(
                    f"Another bot instance found (PID: {old_pid}). "
                    f"Terminating old instance..."
                )
                try:
                    # Send termination signal
                    if sys.platform == "win32":
                        # Windows: use SIGTERM (available in Python 3.7+)
                        os.kill(old_pid, signal.SIGTERM)
                    else:
                        # Unix-like: use SIGTERM
                        os.kill(old_pid, signal.SIGTERM)

                    # Give it a moment to terminate
                    time.sleep(0.5)

                    # Check again - if still running, force kill
                    try:
                        os.kill(old_pid, 0)
                        logger.warning(
                            f"Force killing old instance (PID: {old_pid})..."
                        )
                        if sys.platform != "win32":
                            # SIGKILL only available on Unix
                            os.kill(old_pid, signal.SIGKILL)
                        else:
                            # On Windows, SIGTERM should be sufficient
                            # If not, process cleaned up on next start
                            os.kill(old_pid, signal.SIGTERM)
                    except (ProcessLookupError, OSError):
                        pass  # Process already terminated
                except (ProcessLookupError, OSError) as e:
                    # Process already terminated or doesn't exist
                    logger.info(
                        f"Old instance (PID: {old_pid}) " f"already terminated: {e}"
                    )
            except (ProcessLookupError, OSError):
                # Process doesn't exist - stale lock file
                logger.info(
                    f"Lock file exists but process (PID: {old_pid}) "
                    f"is not running. Removing stale lock."
                )
                LOCK_FILE.unlink(missing_ok=True)
        except (ValueError, OSError) as e:
            # Invalid PID in lock file or read error - remove it
            logger.warning(f"Invalid lock file content: {e}. Removing stale lock.")
            LOCK_FILE.unlink(missing_ok=True)

    # Create lock file with current PID
    try:
        LOCK_FILE.write_text(str(current_pid))
        logger.info(f"Instance lock acquired (PID: {current_pid})")
        return True
    except OSError as e:
        logger.error(f"Failed to create lock file: {e}")
        return False


def release_instance_lock():
    """Release the single-instance lock file."""
    try:
        if LOCK_FILE.exists():
            # Verify it's our PID before deleting
            try:
                lock_pid = int(LOCK_FILE.read_text().strip())
                if lock_pid == os.getpid():
                    LOCK_FILE.unlink(missing_ok=True)
                    logger.info("Instance lock released")
                else:
                    logger.warning(
                        f"Lock file contains different PID "
                        f"({lock_pid} vs {os.getpid()}). "
                        f"Not removing lock file."
                    )
            except (ValueError, OSError):
                # Invalid content or read error - remove anyway
                LOCK_FILE.unlink(missing_ok=True)
                logger.info("Stale lock file removed")
    except OSError as e:
        logger.warning(f"Failed to remove lock file: {e}")


def is_network_error(error: Exception) -> bool:
    """Check if error is transient network issue (NOT a code bug)"""
    error_str = str(error).lower()

    # Windows network errors (WinError 121, 122, etc.)
    if "winerror" in error_str or "121" in error_str or "122" in error_str:
        return True

    # aiohttp network errors
    if isinstance(error, (ClientConnectorError, ClientError)):
        return True

    # Telegram API network errors
    # (aiogram handles these internally, catch if they propagate)
    if isinstance(error, (TelegramNetworkError, TelegramServerError)):
        return True

    # OSError network-related errors
    network_keywords = ["network", "connection", "timeout", "semaphore"]
    if isinstance(error, OSError) and any(
        keyword in error_str for keyword in network_keywords
    ):
        return True

    return False


async def main():
    """Main function to run the bot"""

    # Acquire single-instance lock
    if not acquire_instance_lock():
        logger.error("Failed to acquire instance lock. Exiting.")
        sys.exit(1)

    try:
        # Check if BOT_TOKEN is set
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN is not set! Please set it in .env file")
            return

        if not HR_GROUP_ID:
            logger.warning(
                f"HR_GROUP_ID is not set! Applications for {COMPANY_NAME} "
                f"won't be sent to HR group"
            )

        # Initialize bot and dispatcher
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher(storage=MemoryStorage())

        # Register routers
        dp.include_router(main_handlers.router)
        dp.include_router(application_handlers.router)

        # Start polling
        # Note: aiogram's start_polling() has built-in retry logic for network
        # errors. This function handles transient network issues automatically.
        logger.info("Bot started! Polling for updates...")
        try:
            allowed = dp.resolve_used_update_types()
            await dp.start_polling(bot, allowed_updates=allowed)
        except (TelegramNetworkError, TelegramServerError) as e:
            # These should be handled internally by aiogram, but if they
            # propagate:
            logger.warning(
                f"Telegram API network error (transient - NOT a code bug): "
                f"{type(e).__name__}: {e}\n"
                f"This is typically due to temporary network connectivity "
                f"issues.\n"
                f"aiogram will automatically retry. If this persists, check "
                f"your internet connection."
            )
            raise
        except (ClientConnectorError, ClientError) as e:
            # aiohttp connection errors (WinError 121/122 often appear here)
            logger.warning(
                f"Network connectivity error (transient - NOT a code bug): "
                f"{type(e).__name__}: {e}\n"
                f"Common causes: Internet disconnection, firewall blocking, "
                f"DNS issues, or Telegram API temporary outage.\n"
                f"aiogram handles retries automatically. If this persists, "
                f"check network connectivity."
            )
            raise
        finally:
            # Ensure clean shutdown
            await bot.session.close()
            logger.info("Bot session closed.")
    finally:
        # Release instance lock on all exit paths
        release_instance_lock()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
        sys.exit(0)
    except (
        TelegramNetworkError,
        TelegramServerError,
        ClientConnectorError,
        ClientError,
    ) as e:
        # Network errors - these are transient, NOT code bugs
        error_msg = (
            f"\n{'='*60}\n"
            f"NETWORK ERROR DETECTED (This is NOT a code bug):\n"
            f"Type: {type(e).__name__}\n"
            f"Error: {e}\n"
            f"\nExplanation:\n"
            f"WinError 121/122 and similar network errors are transient "
            f"connectivity issues:\n"
            f"  - Internet connection interruptions\n"
            f"  - Firewall/proxy blocking Telegram API\n"
            f"  - DNS resolution failures\n"
            f"  - Telegram API temporary outages\n"
            f"\naiogram's start_polling() has built-in retry logic.\n"
            f"If the bot exited, restart it. Normal operation will resume "
            f"once connectivity is restored.\n"
            f"{'='*60}\n"
        )
        logger.error(error_msg)
        sys.exit(1)
    except OSError as e:
        # Check if it's a network-related OSError (WinError 121/122)
        if is_network_error(e):
            error_msg = (
                f"\n{'='*60}\n"
                f"NETWORK ERROR DETECTED (This is NOT a code bug):\n"
                f"Type: {type(e).__name__}\n"
                f"Error: {e}\n"
                f"\nExplanation:\n"
                f"This is a Windows network error (likely WinError 121/122):\n"
                f"  - Semaphore timeout expired (connection timeout)\n"
                f"  - Insufficient system resources\n"
                f"  - Network adapter issues\n"
                f"\nThis is NOT a bug in the bot code. It's a transient "
                f"network/system issue.\n"
                f"Restart the bot when connectivity is restored.\n"
                f"{'='*60}\n"
            )
            logger.error(error_msg)
            sys.exit(1)
        else:
            # Non-network OSError (file system, etc.)
            logger.error(f"OS Error: {type(e).__name__}: {e}")
            sys.exit(1)
    except Exception as e:
        # Other unexpected errors - log with full context
        logger.error(
            f"Unexpected error: {type(e).__name__}: {e}\n"
            f"Traceback (if needed, check full exception details):",
            exc_info=True,
        )
        sys.exit(1)
