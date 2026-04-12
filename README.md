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

https://github.com/user-attachments/assets/8d06a23a-b64a-4a9e-a849-f6fb3ec6777f

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
- Converts "2021-09-13" to "September 13, 2021"​ using Intl.DateTimeFormat with timeZone:      "UTC" to get month names, replacing hardcoded array, spelling mistakes, easy to switch      languages
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

### Improvements made after mentor feedback
- Replaced the hardcoded month names array with Intl.DateTimeFormat . Now the browser         generates month names automatically, which prevents spelling mistakes and makes it easy     to switch to Portuguese or any other language by just changing "en" to "pt"

---

## Task 2
A Python script that reads a list of URLs from a CSV file, visits each one, and reports its HTTP status code, with color-coded output, detailed error classification, automatic internet recovery, duplicate detection, and a filterable CSV report.

---

### What it does
- Reads URLs from `Task 2 - Intern.csv`
- Visits each URL and fetches its status code
- Prints the result in the required format: `(Status Code) URL`
- Classifies each error specifically (Timeout, Connection Error, Domain not found, etc), so the user know exactly what went wrong
- Detects and skips duplicate URLs with a warning automatically, so no URL is checked twice and results stay clean
- **Ensures two urls with different tracking parameters pointing to the same source caught as duplicates**
 
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

<img width="1491" height="354" alt="image" src="https://github.com/user-attachments/assets/6e588ff8-ce03-437c-a4cc-66867b6d2133" />


The `[current/total]` counter tracks the progress.

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
The script detects when two URLs in the CSV point to the same source, even if they look different on the surface.
After studying the CSV carefully, two real cases were found:
- Two ESPN URLs in the CSV point to the exact same article but appear different because of extra parameters appended to them, one has ?fbclid=...   (a Facebook tracking tag) and the other has ?platform=amp (an AMP version flag) and they have the same id (9645295). Same article, different     parameters.
- Two ogol.com.br URLs both have ?id=433300 but different paths (player.php vs player_titles.php). These are genuinely different pages.

If duplicate detection is done based on matching id query parameter values, URLs sharing the same id get correctly detected as duplicates, as in the case of ESPN URLs. However, two URLs with the same id value but different paths point to genuinely different pages and would be incorrectly detected as duplicates as in the case of ogol.com URLs.

The challenge is to design a normalization approach that correctly handles both cases.

Therefore, developed a normalize() function that cleans each URL into a standard form by removing the tracking parameters before comparing. It does this in four steps:
- Parsing: the URL is broken into separate pieces - domain, path, query parameters. Also removes www., trailing slashes, and lowercase everything.
- Filtering: known tracking parameters like fbclid, platform, and utm_* are removed. Functional parameters like id= that identify the actual page   are kept.
- Sorting: remaining parameters are sorted alphabetically so ?a=1&b=2 and ?b=2&a=1 are treated as the same URL.
- Rebuilding: the cleaned pieces are joined back into one comparable string.

This way the ESPN URLs both normalize to the same string and the duplicate is caught and the ogol URLs have different paths so they are correctly treated as different URLs even after normalization. 

When a duplicate is found the script prints:

<img width="1475" height="88" alt="image" src="https://github.com/user-attachments/assets/6061e311-7afe-4858-bdee-f7181e77e39d" />

---

### Dependencies
- Requires Python 3.7+
- Requires one library
```
requests — visits URLs and gets HTTP status codes
```
Other libraries used (`csv` and `sys`) are built into Python, hence require no installation.

### Improvements made after feedback
 - Removed color-coded output feature, retry logic, summary,  and timestamped CSV output as these added complexity without being required by the     task
 - Used with open() for file handling so the file closes automatically even if something goes wrong
 - Refined the duplicate detection logic, ensuring two urls with different tracking parameters pointing to the same source caught as duplicates 
 - Used DictReader instead of reader as the given CSV is small, structured and has a header; DictReader automatically handles the header row
 - Changed visited_urls from a set to a dictionary so the script can show which original URL a duplicate is matched against
