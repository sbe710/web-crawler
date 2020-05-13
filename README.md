# Web Crawler + Parser

This project may help you to parse data from web-sites.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

1) To install all dependencies simply type:
```
$ pip3 install selenium bs4 requests
```

2) Next, you need to download web driver from [Chromium](https://chromedriver.chromium.org/downloads)
3) Update the path to your driver in dynamic.py
```
webdriver.Chrome(executable_path="your_path")
```

4) Navigate to web-crawler/linkChecker/linkChecker/spiders folder and execute script
```
$ python dynamic.py
```
