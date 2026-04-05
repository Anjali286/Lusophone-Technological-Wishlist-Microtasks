# Lusophone-Technological-Wishlist-Microtasks

## Task 2
A Python script that reads a list of URLs from a CSV file, visits each one, and reports its HTTP status code, with color-coded output, detailed error classification, automatic internet recovery, duplicate detection, and a filterable CSV report.

---

### What it does
- Reads URLs from `Task 2 - Intern.csv`
- Visits each URL and fetch its status code
- Prints the result in the required format: `(Status Code) URL`
- Color-coded output for each status code based on what went wrong (or right)
- Classifies errors specifically (Timeout, Connection Error, Domain not found, etc)
- Detects and skips duplicate URLs automatically
- If internet connection is interrupted, waits for it to come back and resumes from where it left off
- Saves all results to a timestamped CSV file that can be opened and filtered in any spreadsheet tool.
- Prints a full summary at the end
 
---

### How to run 
**Step 1 - Install dependencies**
```
pip install -r requirements.txt
```
**Step 2 - Place files in the same folder**
```
task_2.py
Task 2 - Intern.csv
requirements.txt
```
**Step 3 - Run the script**
```
python task_2.py
```
 
---

### Output Format
Each URL is printed like:

<img width="1235" height="302" alt="image" src="https://github.com/user-attachments/assets/c9edcfc5-b54c-4b3a-8909-547bb3f61e5c" />

The `[current/total]` counter tracks the progress.

---

### Color-coded output
Every line is printed in a color that tells you exactly what happened at a glance.
| Color | Status | What it means |
|---|---|---|
| **Green** | 2xx | Successful Response |
| **Yellow** | 3xx | Redirection Message |
| **Orange** | 4xx | Client error response |
| **Red** | 5xx | Server error response |
| **Magenta** | Timeout / Connection Error / SSL Error | Network failure |
| **Dark Grey** | Domain not found | The domain does not exist at all |
| **Yellow** | Invalid URL / Skipped | Incorrect web address |

---

### Specific error classification
| Error printed | What it means | What the script does |
|---|---|---|
| `(200)` | URL is working fine | Working, prints in green |
| `(301)` / `(302)` | URL has moved to a new address | Follows the redirect automatically, logs final status |
| `(403)` | Server blocked the request | Logs as Client Error, moves to next URL |
| `(404)` | Page not found | Logs as Client Error, moves to next URL |
| `(503)` | Server temporarily unavailable | Logs as Server Error, moves to next URL |
| `(Timeout)` | Server did not respond in 10 seconds | Logs as Timeout, moves to next URL |
| `(Connection Error)` | Could not connect to the server | Checks if internet is down, if yes, waits and retries, otherwise, logs and moves on |
| `(Domain not found)` | Domain does not exist anymore | Logs as Domain not found, moves to next URL |
| `(SSL Error)` | Invalid security certificate | Logs as SSL Error, moves to next URL |
| `(Too many Redirects)` | Website is stuck in a redirect loop | Logs as Too Many Redirects, moves to next URL|
| `(Invalid URL)` | URL is malformed or missing a protocol | Logs as Invalid URL, moves to next URL |

---

### Duplicate detection
Before visiting a URL, the script normalizes it by:
- Removing `http://` and `https://`
- Removing `www.`
- Removing trailing slashes
- Converting to lowercase
This means `http://google.com`, `https://google.com`, `https://www.google.com/` are all treated as the same URL and checked only once.
 
---

### Summary printed at the end
After all URLs are checked, some stats are being printed:

<img width="578" height="281" alt="image" src="https://github.com/user-attachments/assets/8a494e87-7ff9-4d69-b612-a2ce183e9e30" />

---

### CSV output file with filters
All results are saved to a CSV file named with a timestamp.
The file has three columns, status_code, url, and category. Results can be filtered by any column to easily find working links, broken links, dead domains, or any group in spreadsheet tools.

---

### Dependencies
- Requires Python 3.7+
- Requires two libraries
```
requests — visits URLs and gets HTTP status codes
colorama — adds color to the output
```
All other libraries used (`csv`, `sys`, `re`, `time`, `urllib`) are built into Python, hence require no installation.
