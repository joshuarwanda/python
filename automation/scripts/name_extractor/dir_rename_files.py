import os
import sys

def rename_files(directory, current_standard, new_standard):
    try:
        for filename in os.listdir(directory):
            if current_standard in filename:
                new_filename = filename.replace(current_standard, new_standard)
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
        print("Files renamed successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python dir_rename_files.py <directory> <current_standard> <new_standard>")
        sys.exit(1)

    directory = sys.argv[1]
    current_standard = sys.argv[2]
    new_standard = sys.argv[3]

    rename_files(directory, current_standard, new_standard)