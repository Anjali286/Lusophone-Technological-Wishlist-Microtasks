import requests
import csv
import sys
import re
import time
from urllib.parse import quote, urlparse
from datetime import datetime
from colorama import init, Fore, Style

#configure
time_out=10
max_url_length=2000
max_internet_retries=5
initial_wait=5
max_wait=60
max_url_retries=3

request_header={
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 11.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/134.0.0.0 Safari/537.36"
    ) 
}

# To reset color and initialize colorama
init(autoreset=True)

# Add timestamp to csv output file
time_stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
output_CSV=f"results{time_stamp}.csv"

# Add color to status code
def color_status(status_code):
  ORANGE="\033[38;5;208m"
  GREY=Style.BRIGHT + Fore.BLACK

  if isinstance(status_code,int):
    if 200<=status_code<300:
      return Fore.GREEN
    elif 300<=status_code<400:
      return Fore.YELLOW
    elif 400<=status_code<500:
      return ORANGE
    elif status_code>=500:
      return Fore.RED
  if status_code in ("Timeout", "Connection Error", "SSL Error","Too Many Redirects"):
    return Fore.MAGENTA
  if status_code=="Domain not found":
    return GREY
  if status_code=="Invalid URL":
    return Fore.YELLOW

  return Fore.RED

# Output csv file and summary
def get_category(status_code):
  if isinstance(status_code,int):
    if 200<=status_code<300:
      return "Working"
    elif 300<=status_code<400:
      return "Redirected"
    elif 400<=status_code<500:
      return "Client Error"
    elif status_code>=500:
      return "Server Error"
  if status_code=="Timeout":
    return "Timeout"
  if status_code=="Connection Error":
    return "Connection Error"
  if status_code=="Domain not found":
    return "Domain not found"
  return "Unknown Error"


results_log=[]
def log_result(status_code, url):
  category=get_category(status_code)
  results_log.append({
      "status_code":str(status_code),
      "url":url,
      "category":category
  })

def print_result(status_code,url,current,total):
  color=color_status(status_code)
  print(color+ f"[{current}/{total}] ({status_code}) {url}")
  log_result(status_code,url)

def print_summary():
  counts={
      "Working":0,
      "Redirected":0,
      "Client Error":0,
      "Server Error":0,
      "Timeout":0,
      "Connection Error":0,
      "Domain not found":0,
      "Unknown Error":0,
  }
  for result in results_log:
    category=result["category"]
    if category in counts:
      counts[category]+=1
    else:
      counts["Unknown Error"]+=1

  total=len(results_log)

  print("\nSummary:")
  print(f"Total URL processed: {total}")
  print(f"Working (2xx) : {counts['Working']}")
  print(f"Redirected (3xx) : {counts['Redirected']}")
  print(f"Client Error (4xx) : {counts['Client Error']}")
  print(f"Server Error (5xx) : {counts['Server Error']}")
  print(f"Timeout : {counts['Timeout']}")
  print(f"Connection Error : {counts['Connection Error']}")
  print(f"Domain not found : {counts['Domain not found']}")
  print(f"Unknown Error : {counts['Unknown Error']}")


# Save results
def save_results():
  try:
    with open(output_CSV,"w",newline="",encoding="utf-8") as f:
      writer=csv.DictWriter(f,fieldnames=["status_code","url","category"])
      writer.writeheader()
      writer.writerows(results_log)
    print(f"Results saved: {output_CSV}")
  except Exception as e:
    print(f"Could not save CSV:{e}")

#functions to handle edge cases
# Internet Connection
# Check random url to check the Internet, true if connected, false otherwise
def check_internet():
  try:
    requests.get("https://www.google.com",timeout=5,headers=request_header)
    return True
  except Exception:
    return False

# Wait for internet restoration when drops during execution
# Retries upto max_internet_retries, if internet doesn't restore, exits script
def wait_for_internet(failedURL):
  print(f"Internet Connection Lost")
  print("Rechecking")
  wait_time=initial_wait
  attempt=1
  while attempt<=max_internet_retries:
    time.sleep(wait_time)
    if(check_internet()):
      print(f"\n Internet restored after {attempt} attempt(s)\n")
      return True
    wait_time=min(wait_time*2,max_wait)
    attempt+=1

  print(Fore.RED+f"No Internet")
  sys.exit()

# Handle URL based test cases

# Check whether URL is valid or just a random text(invald)
def is_valid(url):
  if not url.startswith("http"):
    return False
  if "." not in url:
    return False
  return True

# Check if url is a localhost url
def is_local_url(url):
  local_patterns=["localhost","127.0.0.1","192.168","10.0"]
  return any(pattern in url for pattern in local_patterns)

#Check if URL uses a raw IP address instead of domain
def is_IP_url(url):
  ip_pattern=r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
  return bool(re.search(ip_pattern,url))

# Normalize url for duplicate detection, removing http/https, www or slashes
def normalize(url):
  url=url.strip();
  url=url.replace("https://","").replace("http://","")
  url=url.replace("www.","")
  url=url.rstrip("/")
  return url.lower()

# Adding protocol prefix if missing
def fix_missing(url):
  if not url.startswith("http://") and not url.startswith("https://"):
    url="https://"+url
  return url

# Check if url has special characters
def clean_encoding(url):
  try:
    parsed=urlparse(url)
    clean=parsed._replace(path=quote(parsed.path, safe="/:@!$&'()*+,;="))
    return clean.geturl()
  # if cleaning fails, return original
  except Exception:
    return url

# Search all rows for URL
def find_url(row):
  for cell in row:
    if cell.strip().startswith("http"):
      return cell.strip()
  return None

# Final url check (also handles timeouts, redirects)
def check_url(url, current, total):
  for attempt in range(1,max_url_retries+1):
    try:
      response=requests.get(url,timeout=time_out,allow_redirects=True,headers=request_header)
      print_result(response.status_code,url,current,total)
      return

    # print exceptions
    except requests.exceptions.MissingSchema:
      print_result("Invalid URL", url, current, total)
      return
    except requests.exceptions.InvalidURL:
      print_result("Invalid URL", url, current, total)
      return
    except requests.exceptions.SSLError:
      print_result("SSL Error", url, current, total)
      return
    except requests.exceptions.TooManyRedirects:
      print_result("Too Many Redirects", url, current, total)
      return
    except requests.exceptions.Timeout:
      print_result("Timeout", url, current, total)
      return
    except requests.exceptions.ConnectionError as e:
      if not check_internet():
        restored=wait_for_internet(url)
        if attempt<max_url_retries:
          continue
        else:
          print(Fore.RED + f"(No Internet Connection - Maximum Retries Reached) {url}")
          return
      else:
        if "NameResolutionError" in str(e) or "Failed to resolve" in str(e):
          print_result("Domain not found", url, current, total)
          return
        else:
          print_result("Connection Error", url, current, total)
          return
    except Exception as e:
      print_result(f"Unknown Error", url, current, total)
      return

def main():

  if not check_internet():
    wait_for_internet("Startup")
    print("Internet connection confirmed")

  try:
    file=open("Task 2 - Intern.csv","r",encoding="utf-8-sig")
  except FileNotFoundError:
    print(" File Not Found")
    sys.exit()

  reader=csv.reader(file)
  try:
    # Skip header row if does not contain a URL
    header=next(reader)
    if header and header[0].strip().startswith("http"):
      rows_to_process=[header]
    else:
      rows_to_process=[]
  except StopIteration:
    print("No URLs found")
    file.close()
    sys.exit()

  rows_to_process+=list(reader)
  file.close()

  # If file contain only header
  if not rows_to_process:
    print("Only header found. No URLs found")
    sys.exit()

  total=len(rows_to_process)
  current=0;
  visited_urls=set()

  for row in rows_to_process:
    current+=1
    # Skip empty row
    if not row:
      continue

    url=find_url(row)
    if url is None:
      if row[0].strip()=="":
        continue
    # Remove whitespaces
    url=url.strip()

    if not url:
      continue
    if not url.startswith("http") and "." not in url:
      continue

    # Add protocol prefix
    url=fix_missing(url)

    if len(url)>max_url_length:
      print("Very Long URL")
    if is_local_url(url):
      print("Local/Internal URL")
    if is_IP_url(url):
      print("IP based URL")
    if not is_valid(url):
      print("Invalid URL")

    # Remove special characters
    url=clean_encoding(url)
    # Check for duplicates
    normalized=normalize(url)
    if normalized in visited_urls:
      continue
    visited_urls.add(normalized)

    # Visit URLs
    check_url(url,current,total)
    time.sleep(2) # For rate limiting and to avoid overwhelming servers 

  print_summary()
  save_results()

if __name__=="__main__":
  main()
