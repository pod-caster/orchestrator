import os

def list_dir_structure(path, ignore=None, indent=0, output=None):
    ignore = set(ignore or [])
    for item in sorted(os.listdir(path)):
        if item in ignore:
            continue
        full_path = os.path.join(path, item)
        line = "    " * indent + "|-- " + item
        if output:
            output.write(line + "\n")
        else:
            print(line)
        if os.path.isdir(full_path):
            list_dir_structure(full_path, ignore, indent + 1, output)

def export_directory_tree(root_path, ignore=None, output_file="directory_structure.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(f"Directory structure for: {root_path}\n\n")
        list_dir_structure(root_path, ignore=ignore, output=f)
    print(f"✅ Directory structure exported to {output_file}")

if __name__ == "__main__":
    # Change these as needed
    ROOT_DIR = "."   # current directory
    IGNORE_FOLDERS = ["__pycache__", ".git", "node_modules", "pod_env"]
    OUTPUT_FILE = "directory_structure.md"  # can be .txt or .md

    export_directory_tree(ROOT_DIR, ignore=IGNORE_FOLDERS, output_file=OUTPUT_FILE)
