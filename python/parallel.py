import os
import subprocess
import threading

def execute_command(command):
    subprocess.call(command, shell=True)

def track_progress(total_commands, completed_commands):
    percent_complete = (completed_commands / total_commands) * 100
    print(f"Progress: {completed_commands}/{total_commands} ({percent_complete:.2f}%)")

def execute_parallel(commands, num_cores):
    total_commands = len(commands)
    completed_commands = 0
    threads = []

    for _ in range(num_cores):
        thread = threading.Thread(target=worker_thread, args=(commands,))
        thread.start()
        threads.append(thread)

    while completed_commands < total_commands:
        completed_commands = sum(thread.is_alive() for thread in threads)
        track_progress(total_commands, completed_commands)

    print("All commands executed.")

def worker_thread(commands):
    while True:
        try:
            command = commands.pop(0)
            execute_command(command)
        except IndexError:
            break

# Read commands from cmd.txt file
with open('/home/robert/collagen_fibril/dla-collagen/cmds/stress_cmd.txt', 'r') as file:
    commands = file.read().splitlines()

num_cores = 3  # Number of cores to use for parallel execution
execute_parallel(commands, num_cores)

