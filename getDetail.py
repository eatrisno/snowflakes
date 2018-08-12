from helper import *

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

def get_variant(browser):
	variant_data = browser.execute_script('return product_variant')
	resp={}
	for x in variant_data['children']:
		stock = x['stock']
		price = x['price']
		img = x['picture']['original']
		id = x['option_ids'][0]
		resp[id]={'stock':stock,'price':price,'img':img}
	variant_dt = variant_data['variant']
	if len(variant_dt) > 0 :
		for x in variant_dt[0]['option']:
			id = x['id']
			value = x['value']
			resp[id]['value']=value
	return resp
def get_video(html):
	video_tmp = html.find_all(class_='rvm-video-display--item')
	resp = []
	for x in video_tmp:
		resp.append(x.find('iframe').get('src'))
	return '###'.join(resp)

def get_page_detail(browser):
	html = BeautifulSoup(browser.page_source,'html.parser')
	shop_id = html.find(id='shop-id').get('value').strip()
	product_id = html.find(id='product-id').get('value').strip()
	product_name = html.find(id='product-name').get('value').strip()
	product_menu = html.find(id='menu-name').get('value').strip()
	product_price = html.find(id='product_price_int').get('value').strip()
	product_weight = html.find(id='product-weight-kg').get('value').strip()
	product_min_buy = html.find(id='min-order').get('value').strip()
	product_description = html.find(itemprop='description').text.strip().replace('\'','\\\'')
	product_img_str = html.find_all("div", {"class": re.compile("^content-img slick-slide")})
	product_img = '###'.join([img.find('img').get('src') for img in product_img_str])
	variant = str(get_variant(browser)).replace('\'','\\\'')
	video = get_video(html)
	return product_id,product_img,product_name,product_menu,product_min_buy,product_price,product_description,video,variant,product_weight

def add_dbProduct(data,database_table,cHostname,cUsername,cPassword,cDatabase,cPort="3306"):
	mydb=mysql.connector.connect(
	host=cHostname,
	user=cUsername,
	passwd=cPassword,
	database=cDatabase,
	port=cPort
	)
	mycursor = mydb.cursor()
	sql_header = """INSERT INTO `{}` (
	`data_pid`, 
	`image`, 
	`name`, 
	`etalase`, 
	`min_buy`, 
	`price`, 
	`description`, 
	`video`, 
	`variant`, 
	`weight`) VALUES """.format(database_table)
	mysql_rows = []
	product_id,product_img,product_name,product_menu,product_min_buy,product_price,product_description,product_video,product_variant,product_weight = data
	mysql_rows.append("('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(product_id,product_img,product_name,product_menu,product_min_buy,product_price,product_description,product_video,product_variant,product_weight))
	sql_footer = """ ON DUPLICATE KEY UPDATE
	`data_pid`=VALUES(`data_pid`), 
	`image`=VALUES(`image`), 
	`name`=VALUES(`name`), 
	`etalase`=VALUES(`etalase`), 
	`min_buy`=VALUES(`min_buy`), 
	`price`=VALUES(`price`), 
	`description`=VALUES(`description`), 
	`video`=VALUES(`video`), 
	`variant`=VALUES(`variant`), 
	`weight`=VALUES(`weight`)"""
	sql_body=','.join(mysql_rows)
	sql = sql_header+sql_body+sql_footer
	mycursor.execute(sql)
	mydb.commit()
	print("[+] DATA {} record inserted.".format(mycursor.rowcount))
	#UPDATE STATUS # 0 not uploaded # 1 uploaded # -1 removed
	updated_status='1'
	sql_update = ("UPDATE %s SET `status`='%s' WHERE `data_pid`='%s'"%(database_table,updated_status,product_id))
	mycursor.execute(sql_update)
	mydb.commit()
	print("[+] Status Updated | {}.".format(mycursor.rowcount))

def get_product_list(database_table,cHostname,cUsername,cPassword,cDatabase,cPort="3306"):
	mydb=mysql.connector.connect(
	host=cHostname,
	user=cUsername,
	passwd=cPassword,
	database=cDatabase,
	port=cPort
	)
	mycursor = mydb.cursor()
	date = (datetime.datetime.now().strftime("%Y-%m-%d"))
	sql = "select `date`,`data_pid`,`shop_name`,`url`,`name` from {} where `status` = '0' and date = '{}'".format(database_table,date)
	#select `date`,`data_pid`,`shop_name`,`url`,`name`,`` from product_detail where status = '0' and date = '{}'
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	return myresult

def run(root):
	try:
		browser = init_browser(root)
		host="pixel.mynaworks.com"
		user="dev"
		passwd="dev"
		database="sampleDB"
		port="8989"
		datas = get_product_list('product_data',host,user,passwd,database,port)
		for row in datas:
			date,data_pid,shop_name,url,name = row
			print('[+] {}-{} | {}'.format(data_pid,name,url))
			goto_URL(browser,url)
			resp = get_page_detail(browser)
			add_dbProduct(resp,'product_detail',host,user,passwd,database,port)
	except Exception as e:
		print e
	browser.quit()
	
def main():
	browser = init_browser(False)
	host="pixel.mynaworks.com"
	user="dev"
	passwd="dev"
	database="sampleDB"
	port="8989"
	datas = get_product_list('product_data',host,user,passwd,database,port)
	for row in datas:
		date,data_pid,shop_name,url,name = row
		print('[+] {}-{} | {}'.format(data_pid,name,url))
		goto_URL(browser,url)
		resp = get_page_detail(browser)
		add_dbProduct(resp,'product_detail',host,user,passwd,database,port)
	browser.quit()

if __name__ == '__main__':
	name()
