# webcrawler_morningbrew_article
#This is still in progress, I "just" want to: 
1. Store the data in a database, sorted by: 'read', 'favorite', etc, with links, to store data with links next to it so i wouldn't need to load all articles every time.
2. finish learning NLP before implementing the last step which utilizes an ML model i'll build to filter out content for me

Libraries utilized(make sure you have them installed before running the code): 
-concurrent
-playwright_stealth
-pytest-playwright
-multiprocessing
-time(needed for testing, won't need eventually down the road)
-sys

***Note: this code snippet: launch(executable_path="C:/Users/avivo/AppData/Local/ms-playwright/webkit-1992/playwright.exe", headless=HEADLESS_VALUE)
uses an executable path which is local and specific to my computer, you can drop the executable_path and try running gather_website_links without it, it should work,
my solution was temporary as my pytest-playwright went weird and I wasn't gonna spend a few days on finding a non very imporant solution to a not very interesting problem I faced.

***Installation note: to make sure you can use the library_install.bat file, you need to make sure your pip & python Path environment system variables are "correlated". or install them manually, but it's not as fun.
