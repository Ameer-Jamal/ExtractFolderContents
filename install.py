#!/usr/bin/env python3

import os
import shutil
import sys

INSTALL_PATH = os.path.expanduser("~/bin")
SCRIPT_NAME = "copyDir"
SOURCE_FILE = "copyDir.py"
TARGET_FILE = os.path.join(INSTALL_PATH, SCRIPT_NAME)


def append_to_shell_rc(rc_file, line):
    rc_path = os.path.expanduser(rc_file)
    if not os.path.exists(rc_path):
        with open(rc_path, 'w') as f:
            f.write(f"{line}\n")
        return True

    with open(rc_path, 'r') as f:
        content = f.read()

    if line not in content:
        with open(rc_path, 'a') as f:
            f.write(f"\n{line}\n")
        return True
    return False


def install():
    if not os.path.exists(SOURCE_FILE):
        print(f"❌ Error: '{SOURCE_FILE}' not found.")
        sys.exit(1)

    os.makedirs(INSTALL_PATH, exist_ok=True)
    if os.path.exists(TARGET_FILE) or os.path.islink(TARGET_FILE):
        os.remove(TARGET_FILE)
    os.symlink(os.path.abspath(SOURCE_FILE), TARGET_FILE)
    os.chmod(TARGET_FILE, 0o755)

    if INSTALL_PATH not in os.environ.get("PATH", ""):
        shell = os.environ.get("SHELL", "")
        rc_file = "~/.bashrc"
        if "zsh" in shell:
            rc_file = "~/.zshrc"
        elif "fish" in shell:
            rc_file = "~/.config/fish/config.fish"

        export_line = f'export PATH="{INSTALL_PATH}:$PATH"'
        modified = append_to_shell_rc(rc_file, export_line)
        print(f"➕ Added to {rc_file}: {export_line}" if modified else f"ℹ️ PATH already in {rc_file}")
        print(f"✅ Installed '{SCRIPT_NAME}' to {TARGET_FILE}")
        print(f"🔄 Restart your terminal or run: source {rc_file}")
    else:
        print(f"✅ Installed '{SCRIPT_NAME}' to {TARGET_FILE} and ready to use.")


if __name__ == "__main__":
    install()
