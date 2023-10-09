import re
import pandas as pd
from pathlib import Path
import argparse

def rename_files_based_on_tsv(tsv_file, fastq_dir):
    # Load the TSV file into a DataFrame
    df = pd.read_csv(tsv_file, sep="\t")

    # Create a mapping of run_accession to study_alias and experiment_alias
    mapping = df.set_index("run_accession")[["study_alias", "experiment_alias"]].to_dict(orient="index")

    def get_new_filename(filename):
        # # Extract run_accession from the filename
        # run_accession = filename.split("_")[0]

        # Use regex to extract run_accession from the filename
        match = re.search(r"SRR\d+", filename)
        if not match:
            raise ValueError(f"Cannot find run_accession in {filename}")
    
        run_accession = match.group()
        study_alias = mapping[run_accession]["study_alias"]
        experiment_alias = mapping[run_accession]["experiment_alias"]
        return f"{study_alias}_{experiment_alias}_{filename}"

    # Iterate through the files and rename them
    for file_path in fastq_dir.glob("*.fastq.gz"):
        new_filename = get_new_filename(file_path.name)
        new_file_path = file_path.parent / new_filename
        file_path.rename(new_file_path)

def main():
    parser = argparse.ArgumentParser(description="Rename fastq.gz files based on a TSV file.")
    parser.add_argument("tsv_file", type=Path, help="Path to the TSV file.")
    parser.add_argument("fastq_dir", type=Path, help="Directory containing the fastq.gz files.")
    args = parser.parse_args()

    rename_files_based_on_tsv(args.tsv_file, args.fastq_dir)

if __name__ == "__main__":
    main()
