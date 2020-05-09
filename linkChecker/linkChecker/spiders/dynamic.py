from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
import uuid
import requests


URL = "https://pikabu.ru/"
domain = "https://pikabu.ru/"
# Start the WebDriver and load the page
wd = webdriver.Chrome(executable_path="/Users/alep/Downloads/chromedriver")
wd.get(URL)

SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = wd.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = wd.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# And grab the page HTML source
html_page = wd.page_source
print(html_page)
wd.quit()

soup = BeautifulSoup(html_page, 'html.parser')

textArray = []
for element in soup.find_all('div'):
    # print(element.text)
    textArray.append(element.text)
text_file = open("sample.txt", "w")
n = text_file.write("".join(textArray).strip().replace("\t", "").replace("\n", ""))
text_file.close()

images = soup.findAll('img')
for image in images:
    #print image source
    # print('Image:     ' + image['src'])
    filename, file_extension = os.path.splitext(image['src'])
    # print("filename ", file_extension)
    contentData = requests.get(domain + image['src']).content
    unique_filename = str(uuid.uuid4().hex)
    with open(unique_filename + file_extension, 'wb') as handler:
        handler.write(contentData)


videos = soup.findAll('video')
for video in videos:
    #print video source
    print('Image:     ' + video['src'])
    filename, file_extension = os.path.splitext(video['src'])
    print("filename ", file_extension)
    contentData = requests.get(domain + video['src']).content
    unique_filename = str(uuid.uuid4().hex)
    with open(unique_filename + file_extension, 'wb') as handler:
        handler.write(contentData)