# Working Professionally in Cursor: A Guide for PyCharm Users

## Welcome to Cursor! 🎉

This guide will help you transition from PyCharm to Cursor and work professionally with Python projects.

---

## Part 1: Understanding Your Current Project Structure

### Current State
Your project currently has:
- `main.py` - A simple Python file with a print statement

This is a minimal setup. We'll transform it into a professional structure.

---

## Part 2: Cursor vs PyCharm - Key Differences

### 1. **Interface Philosophy**
- **PyCharm**: Full-featured IDE with everything visible
- **Cursor**: Minimalist, AI-powered editor (based on VS Code)
- **Key Difference**: Cursor focuses on AI assistance and clean interface

### 2. **Project Management**
- **PyCharm**: Project-based (opens entire project)
- **Cursor**: Folder-based (works with any folder)
- **Key Difference**: In Cursor, you open a folder, not a "project"

### 3. **Terminal Integration**
- **PyCharm**: Built-in terminal at bottom
- **Cursor**: Integrated terminal (View → Terminal or `` Ctrl+` ``)
- **Similar**: Both have terminal access, Cursor's is more flexible

### 4. **AI Features (Cursor's Superpower)**
- **Cursor**: Built-in AI chat (`` Ctrl+L ``) and inline suggestions
- **PyCharm**: Requires plugins for AI features
- **Key Advantage**: Cursor has AI assistance built-in

---

## Part 3: Essential Cursor Workflow Steps

### Step 1: Opening Your Project
1. **File → Open Folder** (or drag folder into Cursor)
2. Your workspace is now the folder you opened
3. The Explorer panel (left sidebar) shows your files

### Step 2: Understanding the Interface

**Left Sidebar (Explorer):**
- 📁 Files and folders
- 🔍 Search (`` Ctrl+Shift+F ``)
- 🔀 Source Control (Git)
- 🐛 Run and Debug
- 📦 Extensions

**Bottom Panel:**
- Terminal (`` Ctrl+` ``)
- Problems (linter errors)
- Output
- Debug Console

**Right Side:**
- AI Chat panel (`` Ctrl+L ``)
- Can be toggled on/off

### Step 3: Working with Python

#### A. Setting Up Virtual Environment

**In Cursor Terminal:**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
venv\Scripts\activate.bat

# Activate (Mac/Linux)
source venv/bin/activate
```

**Visual Indicator:**
- Terminal prompt shows `(venv)` when active
- Cursor automatically detects Python interpreter

#### B. Selecting Python Interpreter

1. **Press `` Ctrl+Shift+P ``** (Command Palette)
2. Type: `Python: Select Interpreter`
3. Choose your virtual environment's Python:
   - `.\venv\Scripts\python.exe` (Windows)
   - `./venv/bin/python` (Mac/Linux)

**Why this matters:** Cursor needs to know which Python to use for:
- IntelliSense (autocomplete)
- Linting (error checking)
- Running code

#### C. Installing Packages

```bash
# Make sure venv is activated
pip install package_name

# Save to requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt
```

### Step 4: Running Python Code

**Method 1: Terminal (Recommended for learning)**
```bash
python src/main.py
```

**Method 2: Run Button**
- Click the ▶️ button in the top-right
- Or press `` F5 `` (starts debugger)

**Method 3: Right-click → Run Python File in Terminal**

### Step 5: Using AI Features (Cursor's Unique Advantage)

#### A. AI Chat (`` Ctrl+L ``)
- Ask questions about your code
- Get explanations
- Request code changes
- Example: "Explain this function" or "Refactor this code"

#### B. Inline AI Suggestions
- Cursor suggests code as you type
- Press `` Tab `` to accept
- Press `` Esc `` to dismiss

#### C. Composer (`` Ctrl+I ``)
- Multi-file editing
- AI can modify multiple files at once
- Great for refactoring

### Step 6: Debugging

**Setting Breakpoints:**
1. Click left of line number (red dot appears)
2. Press `` F5 `` to start debugging
3. Use debug toolbar:
   - Continue (`` F5 ``)
   - Step Over (`` F10 ``)
   - Step Into (`` F11 ``)
   - Step Out (`` Shift+F11 ``)

**Debug Configuration:**
- Cursor auto-detects Python files
- Or create `.vscode/launch.json` for custom configs

### Step 7: Git Integration

**Basic Git in Cursor:**
1. **Source Control** icon (left sidebar) or `` Ctrl+Shift+G ``
2. See changed files
3. Stage changes (click `+` or `Stage All Changes`)
4. Commit (type message, press `` Ctrl+Enter ``)
5. Push/Pull (buttons at top)

**Terminal Git (More Control):**
```bash
git status
git add .
git commit -m "Your message"
git push
```

---

## Part 4: Professional Project Structure

### Why Structure Matters
- **Organization**: Easy to find files
- **Scalability**: Add features without chaos
- **Team Collaboration**: Others understand your code
- **Best Practices**: Industry standard

### Our Structure:
```
my_project/
├── src/              # All source code here
│   └── main.py       # Entry point
├── tests/            # All tests here
│   └── __init__.py
├── venv/             # Virtual environment (gitignored)
├── .gitignore        # What Git should ignore
├── requirements.txt  # Dependencies list
└── README.md         # Project documentation
```

### Key Principles:
1. **Separate source from tests**
2. **Keep dependencies listed**
3. **Never commit venv/** (too large, machine-specific)
4. **Document everything**

---

## Part 5: Essential Keyboard Shortcuts

### Navigation
- `` Ctrl+P `` - Quick file open
- `` Ctrl+Shift+F `` - Search in all files
- `` Ctrl+` `` - Toggle terminal
- `` Ctrl+B `` - Toggle sidebar

### Editing
- `` Ctrl+D `` - Select next occurrence (multi-cursor)
- `` Alt+Up/Down `` - Move line
- `` Shift+Alt+Up/Down `` - Copy line
- `` Ctrl+/ `` - Toggle comment

### AI Features
- `` Ctrl+L `` - Open AI chat
- `` Ctrl+I `` - Open Composer
- `` Tab `` - Accept AI suggestion

### Python-Specific
- `` F5 `` - Run/Debug
- `` Ctrl+Shift+P `` - Command Palette
- `` Ctrl+, `` - Settings

---

## Part 6: Daily Workflow Checklist

### Starting Your Day:
1. ✅ Open Cursor
2. ✅ Open your project folder
3. ✅ Activate virtual environment in terminal
4. ✅ Verify Python interpreter is selected
5. ✅ Pull latest changes (if using Git)

### While Coding:
1. ✅ Write code in `src/` directory
2. ✅ Use AI chat for questions (`` Ctrl+L ``)
3. ✅ Run code frequently to test
4. ✅ Check Problems panel for errors

### Before Committing:
1. ✅ Test your code
2. ✅ Check for linting errors
3. ✅ Update requirements.txt if needed
4. ✅ Write meaningful commit messages

---

## Part 7: Common Tasks Comparison

| Task | PyCharm | Cursor |
|------|---------|--------|
| Open Project | File → Open | File → Open Folder |
| Run Code | Right-click → Run | F5 or Run button |
| Terminal | View → Tool Windows → Terminal | Ctrl+` |
| Find File | Ctrl+Shift+N | Ctrl+P |
| Search Everywhere | Double Shift | Ctrl+Shift+F |
| Settings | File → Settings | Ctrl+, |
| Git | Built-in VCS | Source Control panel or terminal |
| Debug | Click gutter + Debug | Click gutter + F5 |
| AI Help | Plugin needed | Built-in (Ctrl+L) |

---

## Part 8: Best Practices in Cursor

### 1. **Use the Command Palette**
- `` Ctrl+Shift+P `` is your friend
- Type what you want to do
- Faster than menus

### 2. **Leverage AI**
- Don't hesitate to ask AI (`` Ctrl+L ``)
- Use for explanations, not just code generation
- Review AI suggestions before accepting

### 3. **Keep Terminal Open**
- `` Ctrl+` `` to toggle
- Essential for Python development
- Run commands, see output

### 4. **Use Extensions**
- Python extension (usually auto-installed)
- GitLens (enhanced Git)
- Pylint/Flake8 (linting)
- Install via Extensions panel (`` Ctrl+Shift+X ``)

### 5. **Organize Your Workspace**
- Use folders for organization
- Keep related files together
- Follow the project structure

---

## Part 9: Troubleshooting

### Python Not Found
- **Solution**: Select interpreter (`` Ctrl+Shift+P `` → "Python: Select Interpreter")
- Check virtual environment is activated

### Import Errors
- **Solution**: Make sure you're in the project root
- Check `PYTHONPATH` if needed
- Verify virtual environment has packages installed

### Terminal Not Working
- **Solution**: Check terminal settings (`` Ctrl+, `` → search "terminal")
- Try different shell (PowerShell, CMD, Git Bash)

### AI Not Responding
- **Solution**: Check internet connection
- Verify Cursor is up to date
- Check AI settings in preferences

---

## Part 10: Next Steps

1. **Explore the Interface**: Click around, try shortcuts
2. **Set Up Your Project**: Follow the structure we created
3. **Practice AI Features**: Ask questions, try Composer
4. **Install Extensions**: Enhance your workflow
5. **Build Something**: Apply what you learned

---

## Remember:
- **Cursor is VS Code + AI** - If you know VS Code, you know Cursor
- **AI is a tool, not a replacement** - Use it to learn and be more productive
- **Practice makes perfect** - The more you use it, the more natural it becomes
- **Ask questions** - Use AI chat (`` Ctrl+L ``) whenever stuck!

---

**Happy coding! 🚀**
