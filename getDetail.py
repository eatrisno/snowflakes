from helper import *

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
	return '\n'.join(resp)

def get_var(html,vtype):
	big = html.find(class_='rvm-product-info')
	for row in big.find_all(class_='inline-block va-middle'):
		temp = row.find_all('div')
		if temp[0].text.strip().lower() == vtype.lower():
			return temp[1].text.strip()
			break
	return ''

def get_page_detail(browser):
	html = BeautifulSoup(browser.page_source,'html.parser')
	shop_id = html.find(id='shop-id').get('value').strip()
	product_id = html.find(id='product-id').get('value').strip()
	product_img_obj = html.find_all("div", {"class": re.compile("^content-img slick-slide")})
	product_img = '\n'.join([img.find('img').get('src') for img in product_img_obj])
	product_name = html.find(id='product-name').get('value').strip()
	product_menu = html.find(id='menu-name').get('value').strip()
	product_min_buy = html.find(id='min-order').get('value').strip()
	product_price = html.find(id='product_price_int').get('value').strip()
	product_condition = get_var(html,'Kondisi')
	product_description = browser.find_element_by_id('info').text
	product_video = get_video(html)
	product_variant = json.dumps(get_variant(browser))
	product_weight = html.find(class_='rvm-shipping-content').text.strip()
	product_insurance = get_var(html,'Asuransi')
	return [var.encode('utf8').replace('\'','\\\'') for var in product_id,product_img,product_name,product_menu,product_min_buy,product_price,product_condition,product_description,product_video,product_variant,product_weight,product_insurance]


def update_status():
	#not used yet
	#UPDATE STATUS # 0 not uploaded # 1 uploaded # -1 removed
	updated_status='1'
	sql_update = ("""
		UPDATE %s SET `status`='%s' WHERE `data_pid`='%s'
		"""%(gtable_detail,updated_status,product_id))
	run_sql(sql_update)

def add_dbProduct(data):
	sql_header = """INSERT INTO `{}` (
		`data_pid`,
		`image`,
		`name`,
		`etalase`,
		`min_buy`,
		`price`,
		`condition`,
		`description`,
		`video`,
		`variant`,
		`weight`,
		`insurance`) VALUES """.format(gtable_detail)
	mysql_rows = []
	product_id,product_img,product_name,product_menu,product_min_buy,product_price,product_condition,product_description,product_video,product_variant,product_weight,product_insurance = data
	mysql_rows.append(
		"""('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
		""".format(product_id,product_img,product_name,product_menu,product_min_buy,product_price,product_condition,product_description,product_video,product_variant,product_weight,product_insurance))
	sql_footer = """ ON DUPLICATE KEY UPDATE
		`image`=VALUES(`image`),
		`name`=VALUES(`name`),
		`etalase`=VALUES(`etalase`),
		`min_buy`=VALUES(`min_buy`),
		`price`=VALUES(`price`),
		`condition`=VALUES(`price`),
		`description`=VALUES(`description`),
		`video`=VALUES(`video`),
		`variant`=VALUES(`variant`),
		`weight`=VALUES(`weight`),
		`insurance`=VALUES(`insurance`)
		"""
	sql_body=','.join(mysql_rows)
	sql = sql_header+sql_body+sql_footer
	run_sql(sql)
	

def get_product_listDB():
	date = (datetime.datetime.now().strftime("%Y-%m-%d"))
	sql = """
	select a.`data_pid`,`url`,`name` from 
		(select `data_pid`,`name`,`price`,`url` from {0} where date='{2}') as a,
		(select `data_pid`,`price` from {1} ) as b
	where b.`data_pid`=a.`data_pid`
		and b.`price` != a.`price`
	union
	select `data_pid`,`url`,`name` from {0} where (data_pid) not in (select data_pid from {1}) and date ='{2}'
	""".format(gtable_data,gtable_detail,date)
	myresult = run_sql(sql,'get')
	return myresult

def run():
	#INITIALIZING
	browser = init_browser(root)
	printo('STARTING','center',True)
	print('[+] Get product list')
	while(True):
		datas = get_product_listDB()
		if(len(datas) > 0):
			new_datas = random.sample(datas, len(datas))
			data_pid,url,name = new_datas[0]
			print('[+] {} - {}'.format(data_pid,name))
			print('[+] {}'.format(url))
			goto_URL(browser,url)
			delay()
			resp = get_page_detail(browser)
			add_dbProduct(resp)
		else:
			print('[-] No data to get detail | get data list first.')
			break
	browser.quit()
	printo('FINISH','center',True)

def main():
	run()

if __name__ == '__main__':
	name()
