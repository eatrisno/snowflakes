import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import signal
import csv
from selenium.webdriver.common.by import By
import os,sys, time, inspect,datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from random import randint
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
import shutil
from tempfile import NamedTemporaryFile
import mysql.connector
import json
import re
import math

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
		print('[+] goto :{} | gotoURL'.format(url))
		browser.get(url)
	else:
		print('[-] goto skip | gotoURL')
	time.sleep(5)
	new_url = browser.current_url
	print('[-] youre at this url :{} | before :{} | gotoURL'.format(new_url,curr_url))

def do_pagination(browser,direction):
	err = 0
	pagination_count = 0
	while(True):
		try:
			html = BeautifulSoup(browser.page_source,'html.parser')
			pagination_obj = html.find(class_='pagination')
			pagination = pagination_obj.find_all('a')
			pagination_count = len(pagination)
		except Exception as e:
			err +=1
			print('[-] Try Again | {} | ErT :{} | pagination()'.format(err,e))
		if (pagination_count > 0 or err >= 3) :
			break
		else:
			time.sleep(10)
			print('[/] Wait page loaded.')
	if pagination_count > 0:
		for page in pagination:
			icon = ord(page.string)
			if (icon == 171):
				curr = 'prev'
			elif(icon == 187):
				curr = 'next'
			if curr == direction.lower():
				url = page.get('href')
				goto_URL(browser,url)
				return 'OK'
		return 'NONE'
	else:
		return 'ERROR'

def add_dbProduct(datas,cHostname,cUsername,cPassword,cDatabase,cPort="3306"):
	mydb=mysql.connector.connect(
	host=cHostname,
	user=cUsername,
	passwd=cPassword,
	database=cDatabase,
	port=cPort
	)
	mycursor = mydb.cursor()
	sql_header = "INSERT INTO `product_data` (`shop_name`,`data-pid`, `data-cid`, `name`, `url`, `image`, `price`, `status`) VALUES "
	mysql_rows = []
	for row in datas:
		status = 0
		shop_name,data_pid,data_cid,name,price,url,image = row
		mysql_rows.append("('{}','{}','{}','{}','{}','{}','{}','{}')".format(shop_name,data_pid,data_cid,name,url,image,price,status))
	sql_footer = " ON DUPLICATE KEY UPDATE `name`=VALUES(`name`),`data-cid`=VALUES(`data-cid`),`url`=VALUES(`url`),`price`=VALUES(`price`)"
	sql_body=','.join(mysql_rows)
	sql = sql_header+sql_body+sql_footer
	mycursor.execute(sql)
	mydb.commit()
	print("[+] DATA {} record inserted.".format(mycursor.rowcount))
	
def get_product_list(browser):
	resp = []
	print('[+] Load Page | {}'.format(browser.current_url))
	while(True):
		html = BeautifulSoup(browser.page_source, 'html.parser')
		product_list = html.find_all(itemprop="itemListElement")
		product_count = len(product_list)
		if(product_count > 0):
			break
		else:
			time.sleep(5)
			print('[/] Waiting Page Loaded | item count :{}'.format(product_count))
	shop_name= html.find(id='shop_name').get('value')
	for i, product in enumerate(product_list):
		url_str= product.find('a').get('href')
		o = urlparse.urlparse(url_str)
		url = o.scheme + "://" + o.netloc + o.path
		data_pid= product.get('data-pid')
		data_cid= product.get('data-cid')
		image= product.find(itemprop="image").get('src')
		name= product.find(class_='name').string.strip()
		price_str= product.find(class_='price').string.strip()
		price=int(filter(str.isdigit,str(price_str)))
		resp.append([shop_name,data_pid,data_cid,name,price,url,image])
	print('[+] Jumlah Produk {} | {} Produk Berhasil diambil.'.format(len(product_list),len(resp)))
	return resp

def get_product():
	#INITIALIZING
	host="pixel.mynaworks.com"
	user="dev"
	passwd="dev"
	database="tkpd"
	port="8989"
	url = 'https://tokopedia.com/gadzilastore'
	#STARTING PROGRAM
	try:
		browser = init_browser()
		print('=====INITIALIZING====')
		goto_URL(browser,url)
		while(True):
			product_list = get_product_list(browser)
			add_dbProduct(product_list,host,user,passwd,database,port)
			resp = do_pagination(browser,'next')
			print("[+] Next Page : {}".format(resp))
			if resp in ['ERROR','NONE']:
				print('[-] PROGRAM STOP')
				break
		browser.quit()
	except Exception as e:
		browser.quit()

if __name__ == '__main__':
	get_product()