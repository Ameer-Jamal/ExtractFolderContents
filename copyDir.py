#!/usr/bin/env python3

import os
import sys
import pyperclip
from shutil import which

VERSION = "1.0.0"

def get_code_context(folder_path):
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

                        # Preview: first 20 lines only
                        preview = ''.join(lines[:20]).rstrip()
                        print(f"\n📄 Preview of {file_path} (first 20 lines):\n{'-' * 60}\n{preview}\n{'-' * 60}")
                except UnicodeDecodeError:
                    print(f"Skipping binary/non-text file: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return output_text

def maybe_offer_path_install():
    if which("copyDir") is None:
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
    if len(sys.argv) == 2:
        arg = sys.argv[1].strip().lower()

        if arg in {"-h", "--help"}:
            print("Usage: copyDir <folder_path|pwd|.>\nCopies code files into clipboard from given folder.")
            sys.exit(0)

        if arg in {"-v", "--version"}:
            print(f"copyDir version {VERSION}")
            sys.exit(0)

        folder_to_copy = os.getcwd() if arg in {"pwd", "."} else arg

        if not os.path.isdir(folder_to_copy):
            print(f"❌ Error: '{folder_to_copy}' is not a valid directory.")
            sys.exit(1)

        all_text = get_code_context(folder_to_copy)
        if all_text:
            pyperclip.copy(all_text)
            print("✅ Content copied to clipboard.")
        else:
            print("⚠️ No valid text-based code files found.")

    else:
        maybe_offer_path_install()
        folder_to_copy = input("📁 Enter folder path: ").strip()
        if folder_to_copy in {"pwd", "."}:
            folder_to_copy = os.getcwd()

        if not os.path.isdir(folder_to_copy):
            print(f"❌ '{folder_to_copy}' is not a valid directory.")
        else:
            all_text = get_code_context(folder_to_copy)
            if all_text:
                pyperclip.copy(all_text)
                print("✅ Content copied to clipboard.")
            else:
                print("⚠️ No valid text-based code files found.")
