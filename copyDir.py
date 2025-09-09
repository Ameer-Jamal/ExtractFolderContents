#!/usr/bin/env python3

import os
import sys
import pyperclip
from shutil import which
import shlex

VERSION = "1.0.0"

EXCLUDED_DIRS = {
    ".git", "node_modules", "venv", "__pycache__", "build", "dist", "target",
    "out", "bin", "obj", "coverage", "logs", "tmp", "temp", "cache",
    ".idea", ".vscode", ".mypy_cache", ".pytest_cache"
}

VALID_EXTENSIONS = {
    ".py", ".js", ".ts", ".html", ".css", ".txt", ".json", ".md", ".java", ".c",
    ".cpp", ".go", ".sh", ".rb", ".php", ".swift", ".kt", "kts", ".rs", ".r", ".pl",
    ".lua", ".hs", ".erl", ".ex", ".exs", ".scala", ".clj", ".cljs", ".groovy",
    ".sql", ".xml", ".yml", ".yaml", ".ini", ".cfg", ".conf", ".bat", ".cmd",
    ".ps1", ".dockerfile", ".tf", ".toml", ".lock"
}


def get_code_context(folder_path, preview_lines=None):
    output_text = ""
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        for file in files:
            if os.path.splitext(file)[1].lower() in VALID_EXTENSIONS:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    content = ''.join(lines)
                    output_text += f"\n\n--- FILE: {file_path} ---\n\n{content}"
                    if preview_lines is not None:
                        preview = ''.join(lines[:preview_lines]).rstrip()
                        print(
                            f"\n📄 Preview of {file_path} "
                            f"(first {preview_lines} lines):\n"
                            f"{'-' * 60}\n{preview}\n{'-' * 60}"
                        )
                except UnicodeDecodeError:
                    print(f"Skipping binary/non-text file: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return output_text


def get_text_for_path(path, preview_lines=None):
    if os.path.isdir(path):
        return get_code_context(path, preview_lines)
    if os.path.isfile(path):
        ext = os.path.splitext(path)[1].lower()
        if ext in VALID_EXTENSIONS:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return f"\n\n--- FILE: {path} ---\n\n{content}"
            except UnicodeDecodeError:
                print(f"Skipping binary/non-text file: {path}")
            except Exception as e:
                print(f"Error reading {path}: {e}")
        else:
            print(f"Skipping unsupported file: {path}")
    else:
        print(f"❌ Error: '{path}' is not a valid file or directory.")
    return ""


def maybe_offer_path_install():
    if which("copyDir") is None and sys.stdin.isatty():
        response = input("❓ 'copyDir' not found in PATH. Add it now? [y/N] ").strip().lower()
        if response == 'y':
            target_path = os.path.expanduser("~/bin/copyDir")
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, 'w') as fout, open(__file__, 'r') as fin:
                fout.write(fin.read())
            os.chmod(target_path, 0o755)
            print(f"✅ Installed at {target_path}")
            print("🔄 Please restart your terminal or run:\n    export PATH=\"$HOME/bin:$PATH\"")
        else:
            print("ℹ️ Skipping PATH installation.")


def _split_paths_from_text(text: str) -> list[str]:
    """
    Accepts:
      - comma-separated
      - newline-separated
      - Raycast-flattened space-separated (when newlines were removed)
    Handles quoted paths with spaces. When no commas/newlines are present,
    reconstructs absolute paths by grouping tokens that don't start a new path.
    """
    text = text.strip()
    if not text:
        return []

    # Fast path: commas or newlines present
    if ("," in text) or ("\n" in text) or (" " in text):
        items = []
        for line in text.replace(",", "\n").splitlines():
            line = line.strip()
            if line:
                items.extend(shlex.split(line))
        return items

    # Raycast-flattened case: split by spaces but preserve quoted chunks
    tokens = shlex.split(text)

    # Reconstruct groups:
    # start a new path when token starts with "/" or "~" or equals "pwd"/"."
    starters = ("/", "~")
    special = {"pwd", "."}
    grouped: list[list[str]] = []
    for tok in tokens:
        if tok in special or tok.startswith(starters):
            grouped.append([tok])
        else:
            if not grouped:
                grouped.append([tok])
            else:
                grouped[-1].append(tok)
    return [" ".join(g) for g in grouped]


if __name__ == "__main__":
    preview_lines = None
    raw = sys.argv[1:]  # Raycast provides a single text arg carrying N paths

    if "--help" in raw or "-h" in raw:
        print("Usage: copyDir <paths> [--showContent [N]]")
        print("Paths may be comma-, newline-, or space-separated (quotes supported).")
        sys.exit(0)

    if "--version" in raw or "-v" in raw:
        print(f"copyDir version {VERSION}")
        sys.exit(0)

    if "--showContent" in raw:
        idx = raw.index("--showContent")
        try:
            val = raw[idx + 1]
            preview_lines = int(val)
            raw.pop(idx + 1)
        except (IndexError, ValueError):
            preview_lines = None
        raw.pop(idx)

    # Expand one text argument into N paths
    joined = "\n".join(raw) if raw else ""
    args = _split_paths_from_text(joined)

    # Fallback to interactive or stdin if empty
    if not args and sys.stdin.isatty():
        maybe_offer_path_install()
        path_input = input("Enter paths (comma/newline/space separated; quote if needed): ").strip()
        args = _split_paths_from_text(path_input)
    elif not args:
        data = sys.stdin.read()
        args = _split_paths_from_text(data)

    if not args:
        print("Error: No paths provided.")
        sys.exit(1)

    # Normalize pwd/. to CWD
    args = [os.getcwd() if p in {"pwd", "."} else p for p in args]

    all_text = ""
    for p in args:
        all_text += get_text_for_path(p, preview_lines)

    if all_text:
        pyperclip.copy(all_text)
        print("Content copied to clipboard.")
        sys.exit(0)
    else:
        print("No valid text-based code files found.")
        sys.exit(1)
