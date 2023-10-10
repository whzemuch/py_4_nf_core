import pandas #!/usr/bin/env python3

import argparse
import pandas as pd
import re
import subprocess
from pathlib import Path

def tsv_to_dict(filename: str) -> dict:
    """Convert columns from a TSV file into a dictionary."""
    df = pd.read_csv(filename, sep='\t')
    if 'experiment_alias' not in df.columns or 'fastq_md5' not in df.columns:
        raise ValueError("The TSV file must contain both 'experiment_alias' and 'fastq_md5' columns.")
    return df.set_index('experiment_alias')['fastq_md5'].to_dict()

def extract_sample_id(filename: str) -> str:
    """Extract the GSM identifier from a given filename."""
    match = re.search(r'GSM\d+', filename)
    if not match:
        raise ValueError(f"No GSM identifier found in filename: {filename}")
    return match.group(0)

def _verify_one_md5(file_path: Path, md5_dict: dict) -> bool:
    """Verify the MD5 hash of a file against a provided dictionary using the Linux md5sum utility."""
    result = subprocess.run(['md5sum', file_path], capture_output=True, text=True)
    calculated_md5 = result.stdout.split()[0]
    sample_id = extract_sample_id(file_path.name)
    expected_md5 = md5_dict.get(sample_id)
    if not expected_md5:
        raise KeyError(f"{sample_id} not found in provided dictionary.")
    return calculated_md5 == expected_md5

def main(args):
    """Main function to verify MD5 hashes for FASTQ files using a provided TSV file."""
    md5_dict = tsv_to_dict(args.tsv_file)
    unmatched_sample_ids = []
    for file in Path(args.fastq_folder).glob("*.fastq.gz"):
        if not _verify_one_md5(file, md5_dict):
            sample_id = extract_sample_id(file.name)
            print(f"Unmatched MD5 for sample: {sample_id}")
            unmatched_sample_ids.append(sample_id)
    return unmatched_sample_ids

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify MD5 hashes for FASTQ files using a provided TSV file.")
    parser.add_argument("tsv_file", type=str, help="Path to the TSV file containing GSM identifiers and MD5 hashes.")
    parser.add_argument("fastq_folder", type=str, help="Path to the folder containing FASTQ files.")
    args = parser.parse_args()
    unmatched = main(args)
    if unmatched:
        print("\nSample IDs with unmatched MD5 values:")
        for sample_id in unmatched:
            print(sample_id)
    else:
        print("All samples matched their expected MD5 values.")

