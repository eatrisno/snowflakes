#EKO APRILI TRISNO
#EKO APRILITRISNO
#EAPRILITRISNO@gmail.com

import os
import re
import sys
import csv
import math
import json
import time
import urllib
import signal
import shutil
import random
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

def check_internet():
	while(True):
		try:
			webUrl = urllib2.urlopen("https://www.youtube.com/watch?v=LpCSeB7mF7Y")
			
			if(webUrl.getcode()==200):
				print('[+] Checking Connection | OK')
				break
			else:
				print('[-] Retry Check your internet.')
				delay()	
		except Exception as e:
			print('[E] Error check internet: {}'.format(e))

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
	printo('INFO ({})'.format(platform.system()),'center',True)
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


def unzip_file(filename,outfolder):
	print('[+] Unpacking driver')
	with zipfile.ZipFile(filename, 'r') as zf:
		for info in zf.infolist():
			zf.extract( info.filename, path=outfolder )
			out_path = os.path.join( outfolder, info.filename )
			perm = info.external_attr >> 16L
			os.chmod( out_path, perm )

def check_driver(name,url):
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
	else:
		print('[+] Driver | OK')

	

def init_browser(headless=True):
	try:
		options = webdriver.ChromeOptions()
		if headless == True:
			options.add_argument("headless")
		options.add_argument('user-data-dir={}'.format(gdata)) #Your google chrome data
		browser = webdriver.Chrome(gdriver,chrome_options=options)
		browser.implicitly_wait(20)
		print('[+] Initialization Browser OK')
		return browser
	except Exception as e:
		print('[-] Initialization Browser Failed | E: {}'.format(e))
		return False

def delay(delay=0):
	extraTime = randint(0,5)
	newDelay = extraTime + delay
	strDelay= str(datetime.timedelta(seconds=newDelay))
	print('[@] Sleep - {}'.format(strDelay))
	time.sleep(newDelay)


def goto_URL(browser,url):
	print('[+] Open : {}'.format(url))
	curr_url = browser.current_url
	if curr_url != url:
		browser.get(url)
	else:
		browser.refresh()
	new_url = browser.current_url
	# print('[+] NOW : {}'.format(new_url))


def run_sql(sql,t='put'):
	gmydb=mysql.connector.connect(
		host=ghost,
		user=guser,
		passwd=gpasswd,
		database=gdatabase,
		port=gport)
	mycursor = gmydb.cursor()
	try:
		mycursor.execute(sql)
		if t == 'get':
			return mycursor.fetchall()
		elif t == 'put':
			gmydb.commit()
		print("[+] {} Row affected.".format(mycursor.rowcount))
	except Exception as e:
		print("[-] Error : {}".format(e))
		print("[-] Mysql : {}".format(sql))
	gmydb.close()
	
	
