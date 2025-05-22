#!/usr/bin/env python3
# Command Line Variant

import os
import sys
import pyperclip

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
                        file_content = f.read()
                        output_text += f"\n\n--- FILE: {file_path} ---\n\n{file_content}"
                except UnicodeDecodeError:
                    print(f"Skipping binary/non-text file: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return output_text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: copyDir <folder_path>")
        sys.exit(1)

    folder_to_copy = sys.argv[1]

    if not os.path.isdir(folder_to_copy):
        print(f"Error: '{folder_to_copy}' is not a valid directory.")
        sys.exit(1)

    all_text = get_code_context(folder_to_copy)
    if all_text:
        pyperclip.copy(all_text)
        print(all_text)
        print("\n✅ Content copied to clipboard.")
    else:
        print("No valid text-based code files found.")
