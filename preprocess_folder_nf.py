#!/usr/bin/env python3



import argparse
from pathlib import Path

def get_matching_folders(directory: Path, pattern: str) -> list:
    """
    Get a list of folders matching a given pattern from the specified directory.

    Args:
        directory (Path): Source directory path.
        pattern (str): Folder matching pattern.

    Returns:
        list: List of matching folders.
    """
    return [f for f in directory.glob(pattern) if f.is_dir()]

def process_single_folder(folder: Path, target_folder: Path, prefix: str, dry_run: bool) -> None:
    """
    Process a single folder: create a new folder in the target directory with a specified prefix,
    then create a 'fastq' subfolder and create symbolic links for each .fastq.gz file from the source folder.

    Args:
        folder (Path): Path to the source folder.
        target_folder (Path): Path to the target directory.
        prefix (str): Prefix for the new folder in the target directory.
        dry_run (bool): If True, simulate actions without making changes.
    """
    new_folder = target_folder / f"{prefix}{folder.name}"
    fastq_folder = new_folder / 'fastq'

    if dry_run:
        print("\n"+'*' *80) 
        print(f"Would create folder: {fastq_folder.absolute()}")
        print('*' *80 + '\n') 
        
        for fastq_file in folder.glob('*.fastq.gz'):
            print(f"Would create symbolic link: {fastq_folder / fastq_file.name} -> {fastq_file}")
        return

    new_folder.mkdir(parents=True, exist_ok=True)
    fastq_folder.mkdir(parents=True, exist_ok=True)

    for fastq_file in folder.glob('*.fastq.gz'):
        link_target = fastq_folder / fastq_file.name
        link_target.symlink_to(fastq_file)

def main(args) -> None:
    matching_folders = get_matching_folders(Path(args.directory), args.pattern)
    for folder in matching_folders:
        process_single_folder(folder, Path(args.target_folder), prefix="Project_", dry_run=args.dry_run)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process directory and create symbolic links for fastq.gz files.")
    parser.add_argument("directory", help="Source directory path.")
    parser.add_argument("pattern", help="Folder matching pattern.")
    parser.add_argument("target_folder", help="Target directory path.")
    parser.add_argument("--dry-run", "-n", action="store_true", default=False, help="Simulate actions without making changes.")
    args = parser.parse_args()

    main(args)

