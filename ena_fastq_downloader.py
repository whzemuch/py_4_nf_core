#!/usr/bin/env python

import pandas as pd
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from tqdm import tqdm
from pathlib import Path
import argparse

@dataclass
class AsperaConfig:
    id_dsa_file: str
    max_threads: int = 1

class AsperaDownloader:

    def __init__(self, ena_tsv_file, config):
        self.ena_tsv_file = ena_tsv_file
        self.config = config
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(str(self.ena_tsv_file), sep='\t')

    def filter_data(self, gsm_file_list=None):
        if self.df is None:
            self.load_data()

        # Check if gsm_file_list is provided and is not empty
        if gsm_file_list:
            self.df = self.df[self.df['experiment_alias'].isin(gsm_file_list)]

        return self.df

    def _construct_ascp_command(self, row):
        FASTQ_ASPERA = row['fastq_aspera']
        command = f"""ascp -QT -l 300m -P33001 -k 1 -i {self.config.id_dsa_file} era-fasp@{FASTQ_ASPERA} ."""
        return command

    def _run_command(self, cmd):
        subprocess.run(cmd, shell=True)

    def download(self, dry_run=False):
        if self.df is None:
            self.load_data()
        commands = self.df.apply(self._construct_ascp_command, axis=1).tolist()
        if dry_run:
            print("Dry Run: The following commands will be executed:")
            for cmd in commands:
                print(cmd)
            return
        with ThreadPoolExecutor(self.config.max_threads) as executor:
            list(tqdm(executor.map(self._run_command, commands), total=len(commands)))


def main():
    parser = argparse.ArgumentParser(description="Download files using Aspera.")
    parser.add_argument("ena_tsv_file", type=Path, help="Path to the ENA TSV file.")
    parser.add_argument("--id_dsa_file", 
    	                default="/projects/r_workspace/wangh5_py/.conda_env/kingfisher/etc/asperaweb_id_dsa.openssh",
    	                help="Path to the id_dsa file.")
    parser.add_argument("--max_threads", default=1, type=int, help="Maximum number of threads.")
    parser.add_argument("--gsm_list", nargs='+', help="List of GSM files.")
    parser.add_argument("--dry_run", action="store_true", help="Perform a dry run to show commands.")
    
    args = parser.parse_args() 

    config = AsperaConfig(id_dsa_file=args.id_dsa_file, max_threads=args.max_threads)
    downloader = AsperaDownloader(args.ena_tsv_file, config)
    downloader.filter_data(args.gsm_list)
    if args.dry_run:
        downloader.download(dry_run=True)
    else:
        downloader.download()

if __name__ == "__main__":
    main()




