#!/usr/bin/env python3

import os
import sys
import pyperclip
from shutil import which

VERSION = "1.0.0"

def get_code_context(folder_path, preview_lines=None):
    output_text = ""
    excluded_dirs = {
        ".git", "node_modules", "venv", "__pycache__", "build", "dist", "target",
        "out", "bin", "obj", "coverage", "logs", "tmp", "temp", "cache",
        ".idea", ".vscode", ".mypy_cache", ".pytest_cache"
    }

    valid_extensions = {
        ".py", ".js", ".ts", ".html", ".css", ".txt", ".json", ".md", ".java", ".c",
        ".cpp", ".go", ".sh", ".rb", ".php", ".swift", ".kt", ".rs", ".r", ".pl",
        ".lua", ".hs", ".erl", ".ex", ".exs", ".scala", ".clj", ".cljs", ".groovy",
        ".sql", ".xml", ".yml", ".yaml", ".ini", ".cfg", ".conf", ".bat", ".cmd",
        ".ps1", ".dockerfile", ".tf", ".toml", ".lock"
    }

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in files:
            if os.path.splitext(file)[1].lower() in valid_extensions:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        file_content = ''.join(lines)
                        output_text += f"\n\n--- FILE: {file_path} ---\n\n{file_content}"
                        if preview_lines is not None:
                            preview = ''.join(lines[:preview_lines]).rstrip()
                            print(f"\n📄 Preview of {file_path} (first {preview_lines} lines):\n{'-' * 60}\n{preview}\n{'-' * 60}")
                except UnicodeDecodeError:
                    print(f"Skipping binary/non-text file: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return output_text

def maybe_offer_path_install():
    if which("copyDir") is None:
        if sys.stdin.isatty():
            response = input("❓ 'copyDir' not found in PATH. Add it now? [y/N] ").strip().lower()
            if response == 'y':
                target_path = os.path.expanduser("~/bin/copyDir")
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                with open(target_path, 'w') as f_out:
                    with open(__file__, 'r') as f_in:
                        f_out.write(f_in.read())
                os.chmod(target_path, 0o755)
                print(f"✅ Installed at {target_path}")
                print("🔄 Please restart your terminal or run:\n    export PATH=\"$HOME/bin:$PATH\"")
            else:
                print("ℹ️ Skipping PATH installation.")

if __name__ == "__main__":
    preview_lines = None
    folder_to_copy = None

    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print("Usage: copyDir <folder_path|pwd|.> [--showContent [N]]")
        print("Copies code files into clipboard from the given folder.")
        print("--showContent         Show full file content")
        print("--showContent N       Show first N lines only")
        sys.exit(0)

    if "--version" in args or "-v" in args:
        print(f"copyDir version {VERSION}")
        sys.exit(0)

    if "--showContent" in args:
        idx = args.index("--showContent")
        try:
            val = args[idx + 1]
            preview_lines = int(val)
            args.pop(idx + 1)
        except (IndexError, ValueError):
            preview_lines = 9999999  # Effectively "full file"
        args.pop(idx)

    if len(args) == 1:
        arg = args[0].strip().lower()
        folder_to_copy = os.getcwd() if arg in {"pwd", "."} else arg

    # If a valid path is already given, proceed non-interactively
    if folder_to_copy:
        if not os.path.isdir(folder_to_copy):
            print(f"❌ Error: '{folder_to_copy}' is not a valid directory.")
            sys.exit(1)
        all_text = get_code_context(folder_to_copy, preview_lines)
        if all_text:
            pyperclip.copy(all_text)
            print("✅ Content copied to clipboard.")
        else:
            print("⚠️ No valid text-based code files found.")
    # Otherwise, only allow prompting in interactive environments
    elif sys.stdin.isatty():
        maybe_offer_path_install()
        folder_to_copy = input("📁 Enter folder path: ").strip()
        if folder_to_copy in {"pwd", "."}:
            folder_to_copy = os.getcwd()

        if not os.path.isdir(folder_to_copy):
            print(f"❌ '{folder_to_copy}' is not a valid directory.")
        else:
            all_text = get_code_context(folder_to_copy, preview_lines)
            if all_text:
                pyperclip.copy(all_text)
                print("✅ Content copied to clipboard.")
            else:
                print("⚠️ No valid text-based code files found.")
