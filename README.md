# copyDir

**copyDir** is a simple command-line tool to copy readable code content from any directory into your clipboard. It supports all common code/text formats and skips binary or ignored folders.

## ✅ Features

- Supports CLI: `copyDir /your/project` or `copyDir pwd`
- Automatically copies to clipboard (cross-platform)
- Skips unnecessary folders like `.git`, `node_modules`, etc.
- Recognizes 40+ text-based file extensions

## 🚀 Usage

```bash
copyDir .         # Use current directory
copyDir pwd       # Same as above
copyDir /my/code  # Specific directory
```
## 💡 Installation
### 🧪 Want to use copyDir anywhere?
Option 1: Install manually to your PATH
```bash
chmod +x copyDir.py
mv copyDir.py ~/bin/copyDir
```
⚠️ If ~/bin is not already in your PATH, add this line to your ~/.zshrc or ~/.bashrc:

```bash
export PATH="$HOME/bin:$PATH"
```
Then reload your shell:

```bash
source ~/.zshrc   # or ~/.bashrc
```
Now you can use copyDir from anywhere:

```bash
copyDir .
```
### Option 2: Run automatic installer
```bash
python3 install.py
```
This will place copyDir in ~/bin and tell you if you need to add it to your PA
After that, just run:

```bash
copyDir .
```

## Command Arguments example : 
```bash
copyDir .                        # Copy current file No preview
copyDir . --showContent          # Show full content
copyDir . --showContent 20       # Show first 20 lines per file
copyDir pwd --showContent 50     # Show first 50 lines in current folder
```

## 🧪 Dependencies
Python 3

pyperclip → install with:

```bash
pip install pyperclip
```
## 📦 License
MIT