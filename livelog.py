import requests
import os
import concurrent.futures
import tqdm
import time
import colorama
from colorama import Fore
from termcolor import colored
from urllib.parse import urlparse

os.system("clear" if os.name == "posix" else "cls")

colorama.init(autoreset=True)
print("\n")
banner = r"""
.____    .__               .____
|    |   |__|__  __ ____   |    |    ____   ____  ______
|    |   |  \  \/ // __ \  |    |   /  _ \ / ___\/  ___/
|    |___|  |\   /\  ___/  |    |__(  <_> ) /_/  >___ \
|_______ \__| \_/  \___  > |_______ \____/\___  /____  >
        \/             \/          \/    /_____/     \/

        """

print(colored(banner, "cyan"))

# Pause for effect
time.sleep(0.5)

print("\n")
# Animated developer information display
dev_info = [
    "\nDeveloper  : Tausif Zaman",
    "Github     : tausifzaman"
]

for line in dev_info:
    print(Fore.YELLOW + line)
    time.sleep(0.5)  # Delay between lines
print("\n\n")
def check_url(url):
    """Check if the URL is accessible."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code < 400
    except requests.RequestException:
        return False

def process_line(line):
    """Process and validate a line from the log file."""
    parts = line.strip().split(':', 2)
    if len(parts) == 3:
        raw_url = parts[0]
        parsed_url = urlparse(raw_url)
        if not parsed_url.scheme:
            raw_url = "http://" + raw_url  # Default to HTTP if missing

        if check_url(raw_url):
            return line
    return None

def is_valid_filename(filename):
    """Check if filename is valid and does not contain path traversal characters."""
    return not (filename.startswith("/") or ".." in filename or filename.startswith("\\"))

def filter_valid_logs(file_path):
    """Filter and retain only valid logs."""
    if not is_valid_filename(file_path):
        print("Invalid filename! Possible path traversal attempt detected.")
        return

    if not os.path.exists(file_path):
        print("File not found!")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    max_threads = min(10, os.cpu_count() * 2)  # Limit concurrency to avoid overloading
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        valid_lines = []
        with tqdm.tqdm(total=len(lines), desc="Processing", unit="line") as progress:
            futures = {executor.submit(process_line, line): line for line in lines}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    valid_lines.append(result)
                progress.update(1)

    temp_file = file_path + ".tmp"
    with open(temp_file, 'w', encoding='utf-8') as file:
        file.writelines(valid_lines)

    # Ask for confirmation before replacing the file
    confirm = input(f"Overwrite original file {file_path}? (y/n): ").strip().lower()
    if confirm == 'y':
        os.replace(temp_file, file_path)
        print(f"Filtering complete! Valid logs saved in {file_path}")
    else:
        print("Operation canceled. The original file remains unchanged.")

if __name__ == "__main__":
    log_file = input("Enter the log file name: ").strip()
    filter_valid_logs(log_file)
