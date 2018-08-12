import os
import re
import sys
import csv
import math
import json
import time
import datetime
import signal
import shutil
import requests
import urlparse
import mysql.connector
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def init_browser(headless=True):
	print('+ Init Browser')
	options = webdriver.ChromeOptions()
	if headless == True:
		options.add_argument("headless")
	options.add_argument('user-data-dir=./data') #Your google chrome data
	browser = webdriver.Chrome("./driver/chromedriver",chrome_options=options)
	browser.implicitly_wait(20)
	return browser


def goto_URL(browser,url):
	curr_url = browser.current_url
	if curr_url != url:
		browser.get(url)
	else:
		browser.refresh()
	time.sleep(3)
	new_url = browser.current_url
	print('[+] NOW :{}'.format(new_url))