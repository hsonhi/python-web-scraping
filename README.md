## Web scraping with Python, Selenium, and Pandas

Scrape and extract job data from a job listing website using Selenium and store in Excel using Pandas DataFrame.

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed on your system
- VS Code with Python extension

### Installation & Setup

1. **Install Python**
   - Download and install from [python.org](https://www.python.org)
   - Ensure "Add Python to PATH" is checked during installation

2. **Install VS Code Python Extension**
   - Open VS Code
   - Go to Extensions (Ctrl + Shift + X)
   - Search and install "Python" by Microsoft

3. **Select Python Interpreter**
   - Press `Ctrl + Shift + P`
   - Type "Python: Select Interpreter"
   - Choose your Python installation

4. **Create Virtual Environment**
   - Press `Ctrl + Shift + P`
   - Type "Python: Create Environment"
   - Select `Venv`
   - Choose the latest available Python version

5. **Install Required Packages**
   - Run the following command in the terminal:
   ```bash
   pip install -r requirements.txt
   ```
   - This installs: Selenium, Pandas, and other dependencies

6. **Verify ChromeDriver Compatibility**
   - Selenium will automatically download the correct ChromeDriver
   - Ensure Google Chrome is up to date on your system

### Running the Application

1. Press **F5** in VS Code to start the scraper
2. The app will:
   - Open a Chrome browser window
   - Navigate to the job listing website
   - Scrape job listings
   - Save results to `joblist.xlsx`

### Output

- **File**: `joblist.xlsx`
- **Columns**: Logo, Role, Company
- **Default**: Scrapes 2 job listings (configurable in main.py)

### Configuration

Edit these variables in `main.py` to customize the scraper:

```python
URL = "https://angoemprego.com/vagas-de-emprego/"  # Target website
OUTPUT_FILE = "joblist.xlsx"              # Output filename
JOBS_TO_SCRAPE = 2                                 # Number of jobs to scrape
SCROLL_PAUSE_TIME = 0.2                            # Delay between scrolls
WAIT_TIMEOUT = 10                                  # Max wait time for elements
```

### Troubleshooting

- **ChromeDriver issues**: Update Google Chrome to the latest version
- **Timeout errors**: Increase `WAIT_TIMEOUT` value
- **Missing data**: Check the XPath selectors in the `XPATHS` dictionary if website structure changes