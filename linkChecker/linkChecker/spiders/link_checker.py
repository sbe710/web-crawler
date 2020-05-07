# -*- coding: utf-8 -*-
import scrapy
import requests
import uuid
import os

class LinkCheckerSpider(scrapy.Spider):
    name = 'aliexpress_tablets'
    allowed_domains = ['caniuse.com']
    start_urls = ['https://caniuse.com']

    def parse(self, response):
        # extract content
        imgArray = response.xpath('//img/@src').extract()
        videoArray = response.xpath('//video/@src').extract()
        textArray = response.css("::text").extract()
        self.saveData(imgArray, "image", response)
        self.saveData(videoArray, "video", response)
        text_file = open("sample.txt", "w")
        n = text_file.write("".join(textArray).strip().replace("\t", "").replace("\n", ""))
        text_file.close()

    def saveData(self, array, type, response):
        for contentUrl in array:
            filename, file_extension = os.path.splitext(contentUrl)
            print("filename ", file_extension)
            contentData = requests.get(response.url + contentUrl).content
            unique_filename = str(uuid.uuid4().hex)
            with open(unique_filename + file_extension, 'wb') as handler:
                handler.write(contentData)