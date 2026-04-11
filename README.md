# Addressing the Lusophone Technological Wishlist Proposals

## Task 1
An HTML file that reads a JSON array of Wikipedia articles and displays each article in a formatted sentence with live search, bold highlighting of matched text, any-key-to-search, accent aware search, sort controls, clickable Wikipedia links, duplicate detection, XSS protection, and statistics table. 

---

### What it does
- Reads 12 Wikipedia articles from the `data` variable
- Formats each one into the required sentence and displays it inside `#results`
- Numbers each article (1, 2, 3...)
- Makes each article title a `clickable link` to its Portuguese Wikipedia page
- Handles null data, empty arrays, and missing fields, so the display never crashes or shows raw null values
- Live search, sort controls, duplicate detection, statistics table

---

### How to run
No installation. No libraries.  
```
Open task_1.html in any modern browser.
```
---

### Output Format
- Styled to match Wikipedia's visual language so the output feels native to the Wikimedia ecosystem
- Displays each article in a formatted sentence:

https://github.com/user-attachments/assets/43dc7fac-aacf-4d88-9954-b53ef1ca3367


---

### Search
- Filters articles in real time as being typed
- Searches across title, page ID, and date, so the user can find an article even without knowing its exact title
- Normalizes accents so typing `Andre` finds `André`, essential for Portuguese content where accented characters are frequent
- Bolds the matched text inside each sentence, so the user can immediately see where in the result the search term was found
- Any key press on the page automatically goes to the search box, reducing friction without needing to click first
- Shows "No articles found matching..." when nothing matches
- Shows "Showing X of 12 articles" count while filtering, so the user always knows how many results the current search returned
<img width="416" height="56" alt="image" src="https://github.com/user-attachments/assets/dce74033-f8e2-49b6-8395-80c550af1801" />

---

### Sort
- Sort A-Z by title
- Sort by oldest article first
- Sort by latest article first
- Highlights the active sort button with a blue underline, so the user always knows which order is currently applied
- Sort and search work together at the same time, so filtering a search term and then sorting re-orders only the visible results
<img width="371" height="52" alt="image" src="https://github.com/user-attachments/assets/3d9cc205-662f-4c6b-b2d2-87952e0a3b88" />

---

### Statistics table
- Shows total number of articles
- Shows earliest article with its date and title
- Shows latest article with its date and title
- Shows the time span between earliest and latest years, giving the user a quick sense of how far back the dataset reaches
<img width="898" height="250" alt="image" src="https://github.com/user-attachments/assets/fe766c36-4cff-4387-b476-8241bf2e1927" />

---

### Date handling
- Converts `"2021-09-13"` to `"September 13, 2021"` by string splitting
- Avoids Date object entirely as it silently shifts dates based on the user's locale, which breaks for international Wikimedia contributors
- Validates month is between 1 and 12
- Validates day against actual max days for that specific month
- Checks leap year correctly for February
- Returns `"Unknown Date"` for any invalid or missing date, so the display never crashes or shows raw null values

---

### Duplicate handling
- Checks for duplicate articles by `page_id` before rendering
- If the same article appears more than once in the data, only the first occurrence is shown
- The list is deduplicated silently, no error, no warning, duplicates simply never reach the screen
  
---

### Wikipedia Links
- Every article title is a clickable link that opens the actual Portuguese Wikipedia page related to the article in a new tab, so the user can instantly read the full article without leaving the tool.
- Links are built using the article title with `encodeURIComponent` to correctly handle accented Portuguese characters like `ã`, `é`, and `ô`

---

### Security
- Escapes all strings before inserting into `innerHTML`, preventing XSS injection from malformed article titles or page IDs in the data source
- This converts dangerous characters into safe HTML entities:
    -  `&` → `&amp;`
    -  `<` → `&lt;`
    -  `>` → `&gt;`
    -  `"` → `&quot;`
    -  `'` → `&#x27;`
- Wikipedia links use `rel="noopener noreferrer"` for security

---

## Task 2
A Python script that reads a list of URLs from a CSV file, visits each one, and reports its HTTP status code, with color-coded output, detailed error classification, automatic internet recovery, duplicate detection, and a filterable CSV report.

---

### What it does
- Reads URLs from `Task 2 - Intern.csv`
- Visits each URL and fetches its status code
- Prints the result in the required format: `(Status Code) URL`
- Color-coded output for each status code, so the user can scan results at a glance without reading every status code individually
- Classifies each error specifically (Timeout, Connection Error, Domain not found, etc), so the user know exactly what went wrong
- Detects and skips duplicate URLs automatically, so no URL is checked twice and results stay clean
- If internet connection is interrupted, waits and retries up to 5 times rather than crashing, and resumes from where it left off.
- Saves all results to a timestamped CSV file, so the user can filter and categorize results by status, error type, or URL to track link health over time
- Prints a full summary at the end
 
---

### How to run 
**Step 1 - Install dependencies**
```
pip install -r requirements.txt
```
**Step 2 - Place these files in the same folder**
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
This means `http://google.com`, `https://google.com`, `https://www.google.com/` are all treated as the same URL and checked only once, so that differently written URLs pointing to the same source are not checked multiple times.
 
---

### Summary printed at the end
After all URLs are checked, the following stats are printed:

<img width="578" height="281" alt="image" src="https://github.com/user-attachments/assets/8a494e87-7ff9-4d69-b612-a2ce183e9e30" />

---

### CSV output file with filters
All results are saved to a CSV file named with a timestamp.
The file has three columns, status_code, url, and category, so the user can filter the results by any column to easily find working links, broken links, dead domains, or any group in spreadsheet tools.

---

### Dependencies
- Requires Python 3.7+
- Requires two libraries
```
requests — visits URLs and gets HTTP status codes
colorama — adds color to the output
```
All other libraries used (`csv`, `sys`, `re`, `time`, `urllib`) are built into Python, hence require no installation.
