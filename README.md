# job-scraper
### Scraping jobs from Indeed or CV jobs

The module job-scraper.py enables you to web scrape job postings from Indeed.co.uk or CWjobs.co.uk.

Both require the package Beautiful Soup. For CWjobs, the Selenium web driver is also required. These can be installed as follows:

```bash
$ pip install beautifulsoup4
$ pip install selenium
```

To use this module, import the job_scraper.py file and call the funciton "find_jobs_from()", which takes in several arguments. For an explanation and demonstration of the required arguments, see Demo.ipynb.

## Using the selenium web driver
At present, the default browser is set as Google Chrome. This can be modified within job_scraper.py.

In order to extract jobs from CWjobs using Selenium, the appropriate driver must be installed. See [this link](https://sites.google.com/a/chromium.org/chromedriver/downloads) to download the appropriate driver for the Google Chrome browser and place it in the same directory as the job-scraper.py function.

(IN PROGRESS)
