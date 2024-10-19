from playwright.sync_api import sync_playwright
from morningbrew_article_links_gatherer import gather_website_links, HEADLESS_VALUE, TIMEOUT_LIMIT
import concurrent
from playwright_stealth import stealth_sync
from multiprocessing import cpu_count
import time
#Threads for IO Bound, Processes  for CPU bound
#Can change ProcessPoolExecutor() to ThreadPoolExecutor() and the program will run the same, but utilize threads!

#IDEAS:
#Instead of limiting worker count,
#think of utilizing a mechanism in which, if i get an error, i return the url, create a error list and rerun it/smth
#If I really want to speed the link processing even more, I can think of using multithreading within each process.

WORKER_LIMIT = 3
CHECK_LIMIT_WORKERS = True

def extract_article_data(url):
    print("working on: " + url)
    with sync_playwright() as p:
        browser = None
        # Raise a working browser
        for i in range(4):
            try:
                if i==0:
                    browser = p.webkit.launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/webkit-1992/playwright.exe", headless=HEADLESS_VALUE)
                elif i==1:
                    browser = p.chromium.launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/chromium-1112/chrome-win/chrome.exe", headless=HEADLESS_VALUE)
                elif i==2:
                    browser = p.firefox.launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/firefox-1447/firefox/firefox.exe", headless=HEADLESS_VALUE)

                else:
                    exit("Can't load the website... Darn Anti-Bot verification process!")
                # Set up a new broswer page
                page = browser.new_page()
                # Human-Verification bypass
                stealth_sync(page)
                # parse the new page url
                page.goto(url)
                # Make sure the page has loaded, otherwise try another browser
                page.wait_for_selector('div.kUWhMO', timeout=TIMEOUT_LIMIT)
                break
            except:
                if i <= 2:
                    print(f"Attempt #{i} failed on url: {url}")
                continue
        if browser == None:
            return ["Error - Browser didn't arise."]
        paragraphs = page.query_selector_all('div.kUWhMO p')
        data = []
        for paragraph in paragraphs:
            paragraph_text = paragraph.evaluate('(element) => element.textContent')
            data.append(paragraph_text)
        return data[1:]


def main():

    global ARTICLE_LINKS
    ARTICLE_LINKS = gather_website_links()  # Assuming gather_website_links returns a list of URLs
    #think of using docker

    global WORKER_LIMIT
    print(CHECK_LIMIT_WORKERS)
    if not CHECK_LIMIT_WORKERS:
        WORKER_LIMIT = cpu_count()

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=min(WORKER_LIMIT,cpu_count())) as executor:
        article_data = executor.map(extract_article_data, ARTICLE_LINKS)
    end = time.perf_counter()

    for article in article_data:
        print(article)

    print(f'Seconds To fulfill the data extraction: {end - start}')



if __name__ == "__main__":
    main()

