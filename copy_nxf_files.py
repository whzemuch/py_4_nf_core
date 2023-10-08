#!/usr/bin/env python3



import argparse
from pathlib import Path
import shutil
from tqdm import tqdm

def find_files(directory, patterns):
    found_files = []
    for pattern in patterns:
        found_files.extend(directory.rglob(pattern))
    return found_files

def confirm_copy(file_list):
    print("The following files will be copied:")
    for f in file_list:
        print(f)
    answer = input("Do you want to proceed? (yes/no): ")
    return answer.lower() == 'yes'

def read_rules_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def main():
    parser = argparse.ArgumentParser(description='Copy pipeline files based on rules.')
    parser.add_argument('res_dir', help='Source directory where the result files are located.')
    parser.add_argument('target_dir', help='Target directory where the files will be copied to.')
    parser.add_argument('--rules_file', help='Path to the text file containing file patterns (one per line).')
    parser.add_argument('--rules', nargs='*', default=[], help='Additional rules for file patterns (e.g., *_peaks*, *.bigWig).')

    args = parser.parse_args()

    res_dir = Path(args.res_dir)
    target_dir = Path(args.target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    if args.rules_file:
        file_rules = read_rules_from_file(args.rules_file)
    else:
        file_rules = []

    file_rules.extend(args.rules)
    files_to_copy = find_files(res_dir, file_rules)

    if confirm_copy(files_to_copy):
        for file_path in tqdm(files_to_copy, desc="Copying files", unit="file"):
            parent_folder = file_path.parent.name
            target_subdir = target_dir / parent_folder
            target_subdir.mkdir(exist_ok=True)
            shutil.copy(file_path, target_subdir)
        print("Files copied successfully.")
    else:
        print("Operation cancelled.")

if __name__ == '__main__':
    main()

