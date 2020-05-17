import mimetypes
import os
import sqlite3
import time
import uuid
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from import_to_db import image_to_db, text_to_db, video_to_db

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir))

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

dateTimeObj = datetime.now()
currentDate = str(dateTimeObj.day) + "." + str(dateTimeObj.month) + "." + str(dateTimeObj.year)
currentTime = str(dateTimeObj.hour) + "." + str(dateTimeObj.minute)

# URL to specific page
URL = "https://www.reddit.com/r/Pikabu/"
# Site's domain name
domain = "https://www.reddit.com/"

parsed_uri = urlparse(URL)
domainName = '{uri.netloc}'.format(uri=parsed_uri)

if os.name == "posix":
    save_path = ROOT_DIR + "/output/" + domainName + " " + currentDate + " " + currentTime
else:
    save_path = ROOT_DIR + "\output\\" + domainName + " " + currentDate + " " + currentTime

# Create new folder for output
if os.name == "posix":
    if os.path.isdir(ROOT_DIR + "/output") is False:
        os.mkdir(ROOT_DIR + "/output")
else:
    if os.path.isdir(ROOT_DIR + "\output") is False:
        os.mkdir(ROOT_DIR + "\output")

os.mkdir(save_path)

# Start the WebDriver and load the page
wd = webdriver.Chrome(executable_path="/Users/alep/Downloads/chromedriver")
wd.get(URL)

iteration = 0
SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = wd.execute_script("return document.body.scrollHeight")

while True:
    iteration += 1

    # Scroll down to bottom
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = wd.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    if iteration == 5:
        break
    last_height = new_height

# And grab the page HTML source
html_page = wd.page_source
# Close the WebDriver
wd.quit()

soup = BeautifulSoup(html_page, 'html.parser')

# Connect to db
conn = sqlite3.connect("SaTRdatabase.db")
cursor = conn.cursor()
vsourse = 'no_video'

textArray = []

for element in soup.find_all('div'):
    textArray.append(element.text)

textContent = "".join(textArray).strip().replace("\t", "").replace("\n", "")
text_file = open(os.path.join(save_path, "parsed text.txt"), "w", encoding='utf-8')
text_file.write(textContent)
text_file.close()

text_to_db(textContent, save_path, cursor)

conn.commit()
conn.close()

html_file = open(os.path.join(save_path, "parsed html.txt"), "w", encoding='utf-8')
html_file.write(html_page)
html_file.close()

images = soup.findAll('img')

# Create new folder for images
if os.name == "posix":
    if os.path.isdir(save_path + "/images") is False:
        os.mkdir(save_path + "/images")
else:
    if os.path.isdir(save_path + "\images") is False:
        os.mkdir(save_path + "\images")

for image in images:
    print('Image:     ' + image['src'])
    filename, file_extension = os.path.splitext(image['src'])
    response = requests.get(image['src'], headers=HEADERS)
    contentType = response.headers['content-type']
    file_extension_from_header = mimetypes.guess_extension(contentType)
    unique_filename = str(uuid.uuid4().hex)
    if os.name == "posix":
        completeName = os.path.join(save_path + "/images/", unique_filename + file_extension_from_header)
    else:
        completeName = os.path.join(save_path + "\\images\\", unique_filename + file_extension_from_header)
    with open(completeName, 'wb') as handler:
        conn = sqlite3.connect("SaTRdatabase.db")
        cursor = conn.cursor()
        image_to_db(save_path + "/images", vsourse, cursor)
        conn.commit()
        conn.close()
        handler.write(response.content)

videos = soup.findAll('video')

# Create new folder for videos
if os.name == "posix":
    if os.path.isdir(save_path + "/videos") is False:
        os.mkdir(save_path + "/videos")
else:
    if os.path.isdir(save_path + "\\videos") is False:
        os.mkdir(save_path + "\\videos")

for video in videos:
    print('Video:     ' + video['src'])
    filename, file_extension = os.path.splitext(video['src'])
    response = requests.get(video['src'], headers=HEADERS)
    contentType = response.headers['content-type']
    file_extension_from_header = mimetypes.guess_extension(contentType)
    unique_filename = str(uuid.uuid4().hex)
    if os.name == "posix":
        completeName = os.path.join(save_path + "/videos/", unique_filename + file_extension_from_header)
    else:
        completeName = os.path.join(save_path + "\\videos\\", unique_filename + file_extension_from_header)
    with open(completeName, 'wb') as handler:
        conn = sqlite3.connect("SaTRdatabase.db")
        cursor = conn.cursor()
        video_to_db(save_path, vsourse, cursor)
        conn.commit()
        conn.close()
        handler.write(response.content)
