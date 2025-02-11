import os
import pyperclip  # Import the pyperclip library


def get_code_context(folder_path):
    """
    Traverses a folder, reads text-based code files, and formats them for context.
    Automatically copies the output to the clipboard.

    Args:
        folder_path (str): The path to the folder containing the code.

    Returns:
        str: A string containing the formatted file contents with headers,
             ready to be pasted.
    """
    output_text = ""
    excluded_dirs = {".git", "node_modules", "venv", "__pycache__"}  # Add any directories to exclude here
    valid_extensions = {".py", ".js", '.ts', ".html", ".css", ".txt", ".json", ".md", ".java", ".c", ".cpp", ".go",
                        ".sh"}

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]  # Modify dirs in-place to prune excluded directories
        for file in files:
            if os.path.splitext(file)[1].lower() in valid_extensions:  # Check file extension
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r',
                              encoding='utf-8') as f:  # Explicitly open in text mode with utf-8 encoding
                        file_content = f.read()
                        output_text += f"\n\n--- FILE: {file_path} ---\n\n{file_content}"
                except UnicodeDecodeError:
                    print(f"Skipping binary or non-text file: {file_path}")
                except Exception as e:
                    print(f"Error reading file: {file_path} - {e}")

    return output_text


if __name__ == "__main__":
    folder_to_copy = input("Enter the path to the folder you want to copy contents from: ")

    if not os.path.isdir(folder_to_copy):
        print(f"Error: '{folder_to_copy}' is not a valid directory.")
    else:
        all_text = get_code_context(folder_to_copy)
        if all_text:
            pyperclip.copy(all_text)  # Copy the output to the clipboard
            print("\n--- Copied Content (and automatically copied to clipboard!) ---\n")  # Modified message
            print(all_text)
            print("\n--- End of Copied Content ---")
            print(
                "\nThe content has been automatically copied to your clipboard and is ready to be pasted.")
        else:
            print("No valid text-based code files found in the specified folder or its subfolders.")
