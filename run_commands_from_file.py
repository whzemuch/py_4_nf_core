import subprocess
import argparse
from tqdm import tqdm

def run_commands_from_file(command_file, log_file):
    with open(command_file, 'r') as f:
        commands = f.readlines()

    with open(log_file, 'a') as log:
        for cmd in tqdm(commands, desc="Executing commands", unit="command"):
            cmd = cmd.strip()  # Remove any trailing or leading whitespace
            try:
                # Run the command and wait for it to complete
                subprocess.check_call(cmd, shell=True)
            except subprocess.CalledProcessError as e:
                # If an error occurs, write the error message to the log file
                log.write(f"Error executing command '{cmd}': {e}\n")

def main():
    parser = argparse.ArgumentParser(description="Execute commands from a file and log errors.")
    parser.add_argument("command_file", type=str, help="Path to the file containing the commands.")
    parser.add_argument("--log_file", type=str, default="errors.log", help="Path to the log file where errors will be written. Default is 'errors.log'.")
    args = parser.parse_args()

    run_commands_from_file(args.command_file, args.log_file)

if __name__ == "__main__":
    main()
