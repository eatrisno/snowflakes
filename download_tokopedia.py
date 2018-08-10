import os
import sys
import csv
import time
import shutil
import signal
import datetime
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

def init_browser(url):
    print('+ Init Browser')
    options = webdriver.ChromeOptions()
	# options.add_argument("headless")
    browser = webdriver.Chrome("./driver/chromedriver",chrome_options=options)
    browser.implicitly_wait(10)
    browser.get(url)
    return browser

def doDownload():
	url = 'https://tokopedia.com/gadzilastore'
	browser = init_browser(url)
	



def main():
	doDownload()

if __name__ == '__main__':
	main()