from helper import *

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

def add_dbProduct(datas,database_table,mydb):
	mycursor = mydb.cursor()
	sql_header = "INSERT INTO `{}` (`shop_name`,`date`,`data_pid`, `data_cid`, `name`, `url`, `image`, `price`) VALUES ".format(database_table)
	mysql_rows = []
	date = (datetime.datetime.now().strftime("%Y-%m-%d"))
	for row in datas:
		shop_name,data_pid,data_cid,name,price,url,image = row
		mysql_rows.append("('{}','{}','{}','{}','{}','{}','{}','{}')".format(shop_name,date,data_pid,data_cid,name,url,image,price))
	sql_footer = " ON DUPLICATE KEY UPDATE `name`=VALUES(`name`),`data_cid`=VALUES(`data_cid`),`url`=VALUES(`url`),`price`=VALUES(`price`)"
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
			time.sleep(10)
			print('[/] Waiting Page Loaded | Wait Product Loaded : {}'.format(product_count))
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

def run(root):
	#INITIALIZING
	print('=====INITIALIZING====')
	host="pixel.mynaworks.com"
	user="dev"
	passwd="dev"
	database="sampleDB"
	port="8989"
	database_table = 'product_data'
	url = 'https://tokopedia.com/gadzilastore'
	mydb=mysql.connector.connect(
		host=host,
		user=user,
		passwd=passwd,
		database=database,
		port=port)

	browser = init_browser(root)
	print('[+] OK')
	print('======STARTING=====')
	try:
		goto_URL(browser,url)
		while(True):
			product_list = get_product_list(browser)
			add_dbProduct(product_list,database_table,mydb)
			resp = do_pagination(browser,'next')
			print("[+] Next Page : {}".format(resp))
			if resp in ['ERROR','NONE']:
				print('[-] PROGRAM STOP')
				break
	except Exception as e:
		print e
	browser.quit()
	print("=====FINISH====")
	x = raw_input('Press any key to continue')

def main():
	boot = False
	run(boot)


if __name__ == '__main__':
	main()