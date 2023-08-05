import os
import sys
import subprocess
from multiprocessing import Pool
from tqdm import tqdm

def run_command(command):
    try:
        subprocess.check_call(command, shell=True)
        return None
    except subprocess.CalledProcessError as e:
        return e
path = '/home/robert/Documentos/Data_zurik/Cmds/cmd_.txt'
def main(num_cores):
    if not os.path.exists(path):
        print("Error: cmd.txt not found.")
        sys.exit(1)

    with open(path, "r") as file:
        commands = [line.strip() for line in file]

    with Pool(processes=num_cores) as pool:
        errors = list(tqdm(pool.imap(run_command, commands), total=len(commands)))

    if any(errors):
        print("Some commands failed:")
        for error in errors:
            if error is not None:
                print(f"Command failed: {error.cmd}, return code: {error.returncode}")

if __name__ == "__main__":
    num_cores = 3
    main(num_cores)