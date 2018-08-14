import os
import re
import sys
import csv
import math
import json
import time
import signal
import shutil
import zipfile
import urllib2
import datetime
import requests
import urlparse
import platform
import mysql.connector
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
curr_fld = os.path.dirname(os.path.abspath(__file__))

driver = "chromedriver"
gdriver = curr_fld+"/"+driver
gdata = curr_fld+"/data"
ghost="pixel.mynaworks.com"
guser="dev"
gpasswd="dev"
gdatabase="sampleDB"
gport="8989"
gtable_data = 'product_data'
gtable_detail = 'product_detail'
gurl = 'https://tokopedia.com/gadzilastore'
mac='https://chromedriver.storage.googleapis.com/2.41/chromedriver_mac64.zip'
win='https://chromedriver.storage.googleapis.com/2.41/chromedriver_win32.zip'
linux='https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip'

gmydb=mysql.connector.connect(
	host=ghost,
	user=guser,
	passwd=gpasswd,
	database=gdatabase,
	port=gport)

def check_internet():
	try:
		webUrl = urllib2.urlopen("https://www.youtube.com/watch?v=LpCSeB7mF7Y")
		return webUrl.getcode()
	except Exception as e:
		# print e
		return False

def printo(text, algn='left',fill=False):
	if algn == 'left':
		print "|{:<50}|".format(text)
	elif algn == 'center':
		if fill == True:
			print "|{:-^50}|".format(text)
		else:
			print "|{:^50}|".format(text)

def linux_distribution():
	  try:
		return platform.linux_distribution()
	  except:
		return "N/A"

def info_OS():
	printo('','center',True)
	printo('INFO ({})'.format(os.name),'center',True)
	print("[+]	Python version: %s"%sys.version.split('\n'))
	print("[+]	dist: %s"%str(platform.dist()))
	print("[+]	linux_distribution: %s"%str(linux_distribution()))
	print("[+]	system: %s"%platform.system())
	print("[+]	machine: %s"%platform.machine())
	print("[+]	platform: %s"%platform.platform())
	print("[+]	uname: %s"%str(platform.uname()))
	print("[+]	version: %s"%platform.version())
	print("[+]	mac_ver: %s"% str(platform.mac_ver()))
	printo('','center',True)

def extract_file( zf, info, extract_dir ):
	zf.extract( info.filename, path=extract_dir )
	out_path = os.path.join( extract_dir, info.filename )
	perm = info.external_attr >> 16L
	os.chmod( out_path, perm )

def unzip_file(filename,outfolder):
	print('[+] Unpacking driver')
	with zipfile.ZipFile(filename, 'r') as zf:
		for info in zf.infolist():
			extract_file( zf, info, outfolder )

def prepare_driver(name,url):
	if not (os.path.isfile(name)):
		print('[+] Checking driver')
		if not (os.path.isfile('chromedriver.zip')):
			print('[+] Downloading driver')
			r = requests.get(url, allow_redirects=True)
			open('chromedriver.zip', 'wb').write(r.content)
		#UNZIP
		chromedriver_name = './chromedriver.zip'
		unzip_file(chromedriver_name,'./')
		os.remove(chromedriver_name)


def initialization():
	printo('HI.','center',False)
	printo('INIZIALIZATION','center',True)
	resp = check_internet()
	if not resp == 200 :
		print "[-] Check Your internet Connection"
		return False

	if (os.name == "posix"):
		url = mac
		driver = 'chromedriver'
	elif (os.name == 'linux' ):
		url = linux
		driver = 'chromedriver'
	elif (os.name == "nt"):
		url = win
		driver = 'chromedriver.exe'
	else:
		print "[-] Initialization Failed"
		return False
	prepare_driver(driver,url)
	print("[+] Initialization OK")
	return True
	
	

def init_browser(headless=True):
	print('[+] Init Browser')
	options = webdriver.ChromeOptions()
	if headless == True:
		options.add_argument("headless")
	options.add_argument('user-data-dir={}'.format(gdata)) #Your google chrome data
	browser = webdriver.Chrome(gdriver,chrome_options=options)
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
