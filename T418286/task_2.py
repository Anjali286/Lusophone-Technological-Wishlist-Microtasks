import requests
import csv
import sys
from urllib.parse import urlparse, urlencode, parse_qs

# Configure
time_out = 5
# Input filename
input_file = "Task 2 - Intern.csv"

request_header = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/147.0.7727.55 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

# Handle URL based edgecases

# Adding protocol prefix if missing
def fix_missing_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://"+url
    return url
    
# Attempt to fetch URL and print the status code or specific error message
def check_url(url, current, total):
    try:
        response = requests.get(url, timeout = time_out, allow_redirects = True, headers = request_header)
        print(f"[{current}/{total}] ({response.status_code}) {url}")
        return
    
    # print specific exceptions
    except requests.exceptions.MissingSchema:
        print(f"[{current}/{total}] (Invalid URL: Missing Schema) {url}")
        return
    except requests.exceptions.InvalidURL:
        print(f"[{current}/{total}] (Invalid URL: Malformed) {url}")
        return
    except requests.exceptions.SSLError:
        print(f"[{current}/{total}] (SSL Error) {url}")
        return
    except requests.exceptions.TooManyRedirects:
        print(f"[{current}/{total}] (Too Many Redirects) {url}")
        return
    except requests.exceptions.Timeout:
        print(f"[{current}/{total}] (Timeout) {url}")
        return
    except requests.exceptions.ConnectionError as e:
        if "NameResolutionError" in str(e) or "Failed to resolve" in str(e):
          print(f"[{current}/{total}] (DNS Resolution Error) {url}")
          return
        else:
          print(f"[{current}/{total}] (Connection error) {url}")
          return
    except Exception as e:
      print(f"[{current}/{total}] (Unknown Error - {str(e)[:60]}) {url}")
      return
    
#Normalize url for duplicate detection, removing http/https, www or slashes
def normalize(url):
    url = url.strip();
    url = url.replace("https://","").replace("http://","")
    url = url.replace("www.","")
    url = url.rstrip("/")
    return url.lower()


def main():
    try:
        with open(input_file, "r", encoding = "utf-8-sig") as file:
          reader = csv.DictReader(file)
          rows_to_process = list(reader)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit()
    
    # If no rows to process, print message and exit
    if not rows_to_process:
        print(f"File '{input_file}' is empty.")
        file.close()
        sys.exit()
    
    current = 0
    total = len(rows_to_process)

    visited_urls = set()

    for row in rows_to_process:
  
        # Skip empty row
        if not row:
          continue

        url = row.get("urls", "")

        # Remove whitespaces from url
        url=url.strip()

        if not url:
          continue

        # Skip if not a URL
        if not url.startswith("http") and "." not in url:
          continue

        # Add protocol prefix if missing
        url = fix_missing_url(url)

        # Normalize url, check for duplicates, and skip it with a warningif already visited
        normalized_url = normalize(url)
        if normalized_url in visited_urls:
          continue
        visited_urls.add(normalized_url)

        # Visit URL and print status code or error message
        current += 1
        check_url(url, current, total)

if __name__ == "__main__":
    main()
