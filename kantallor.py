import requests
import subprocess
from bs4 import BeautifulSoup
from tabulate import tabulate
from urllib.parse import urljoin
from colorama import Fore, Style

# URL of the webpage
base_url = 'https://ipsniper.info/archive/latest/domainlists/public/'

# Strings to filter the file names
filter_strings = ['.gz']

try:
    # Send a GET request to the webpage
    response = requests.get(base_url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Error accessing the webpage. Status code: {response.status_code}")
        exit()

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the links on the webpage
    links = soup.find_all('a')

    # Filter and collect file details based on filter strings
    files = []
    for link in links:
        file_url = link.get('href')
        if file_url:
            file_name = file_url.rsplit('/', 1)[-1]
            lowercase_file_name = file_name.lower()
            if any(filter_string.lower() in lowercase_file_name for filter_string in filter_strings):
                full_url = urljoin(base_url, file_url)
                files.append([len(files) + 1, file_name, full_url])

    # Generate the table
    table_headers = [Fore.YELLOW + "No.", "File", "Download link" + Style.RESET_ALL]
    table = tabulate(files, headers=table_headers, tablefmt="fancy_grid")

    # Create the banner
    banner = f"""
{Fore.MAGENTA}
██╗  ██╗ █████╗ ███╗   ██╗████████╗ █████╗ ██╗     ██╗      ██████╗ ██████╗ 
██║ ██╔╝██╔══██╗████╗  ██║╚══██╔══╝██╔══██╗██║     ██║     ██╔═══██╗██╔══██╗
█████╔╝ ███████║██╔██╗ ██║   ██║   ███████║██║     ██║     ██║   ██║██████╔╝
██╔═██╗ ██╔══██║██║╚██╗██║   ██║   ██╔══██║██║     ██║     ██║   ██║██╔══██╗
██║  ██╗██║  ██║██║ ╚████║   ██║   ██║  ██║███████╗███████╗╚██████╔╝██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝
   KanTallor IP Sniper by SICARIO | 2023 
{Style.RESET_ALL}
"""

    # Print the banner and table
    print(banner)
    print(table)

    # Prompt user for download choice
    choice = input("\nSelect the number(s) of the file(s) to download (separated by commas) or 'all' to download all files: ")

    # Download selected files
    if choice.lower() == 'all':
        # Download all files
        for file in files:
            file_name = file[1]
            full_url = file[2]
            subprocess.run(["wget", full_url, "-O", file_name])
    else:
        # Download selected files
        selected_files = choice.split(",")
        for file_num in selected_files:
            try:
                file_num = int(file_num.strip())
                if file_num > 0 and file_num <= len(files):
                    file = files[file_num - 1]
                    file_name = file[1]
                    full_url = file[2]
                    subprocess.run(["wget", full_url, "-O", file_name])
                else:
                    print(f"Invalid file number: {file_num}. Skipping...")
            except ValueError:
                print(f"Invalid input: {file_num}. Skipping...")
            except KeyboardInterrupt:
                print("\nDownload interrupted by user.")
                break

except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
