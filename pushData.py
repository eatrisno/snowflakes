from helper import *

def update_status():
	#not used yet
	#UPDATE STATUS # 0 not uploaded # 1 uploaded # -1 removed
	updated_status='1'
	sql_update = ("""
		UPDATE %s SET `status`='%s' WHERE `data_pid`='%s'
		"""%(gtable_detail,updated_status,product_id))
	run_sql(sql_update)

def clean(text):
	word1 = " ".join(re.findall("[a-zA-Z]+", text))
	return word1.strip().lower()

def screenCenter(browser,element):
	browser.execute_script("return arguments[0].scrollIntoView();", element)
	browser.execute_script("window.scrollBy(0, -150);")
	
def inputById(browser,elementId,value,iType='text'):
	try:
		form = browser.find_element_by_id(elementId)
		screenCenter(browser,form)
		value = str(value)
		if iType == 'text':
			form.clear()
		form.send_keys(value)
	except ElementNotVisibleException as e:
		print e

def selectEtalase(browser,elementId,etalaseName):
	try:
		print('get Element options')
		select = browser.find_element_by_id(elementId)
		selected = 'string:new'
		for x in select.find_elements_by_tag_name('option'):
			etalase,etalaseVal = x.get_attribute("label"),x.get_attribute("value")
			if(clean(etalase) == clean(etalaseName)):
				print etalase,etalaseVal
				selected = etalaseVal
				break
		#trigger etalase
		print('Triger Element Option')
		screen = browser.find_element_by_id("s-etalase")
		screenCenter(browser,screen)
		option = browser.find_element_by_link_text("Pilih Etalase")
		option.click()
		
		#select etalase
		tryCount = 0
		while(tryCount < 3):
			print('Try (%s) to select'%str(tryCount+1))
			try:
				print('Select Option')
				resp = browser.find_element_by_xpath("//li//a[@rel='%s']" % selected)
				browser.execute_script("return arguments[0].scrollIntoView();", resp)
				browser.execute_script("window.scrollBy(0, -150);")
				resp.click()
				break
			except ElementNotVisibleException as e:
				tryCount+=1
				print e
				delay(10)
		#IF ADD NEW ETALASE
		if(selected == 'string:new'):
			resp = browser.find_element_by_id("p-menu-name")
			resp.clear()
			resp.send_keys(etalaseName)
			
	except ElementNotVisibleException as e:
		print e

				   
def get_product_list():
	date = (datetime.datetime.now().strftime("%Y-%m-%d"))
	sql = """
	select `data_pid`,`name`,`image`,`etalase`,`min_buy`,`price`,`condition`,`description`,`video`,`variant`,`weight`,`insurance`
	from {1} 
	where data_pid 
	in ( select data_pid from {1} where data_pid in (select data_pid from {0} where date = '{2}')
	) and
	`upload_status` = '0'
	ORDER BY RAND() LIMIT 1
	""".format(gtable_data,gtable_detail,date)
	myresult = run_sql(sql,'get')
	return myresult

def download(fld,url,name=None):
	if name == None:
		name = url.rsplit('/',1)[-1]
	if not os.path.exists(fld):
		os.makedirs(fld)
	if name.split('.')[-1] in ['png','jpg','jpeg']:
		path=fld+'/'+name
	else:
		name=name+'.jpg'
	path=fld+'/'+name
	if not os.path.exists(path):
		print('[*] download image to : %s'% path)
		urllib.urlretrieve(url,path)
	else:
		print('[-] image already exsists : %s'% path)
	return path

def downloadImage(path,lists):
	for url in lists:
		yield download(path,url)

def doInputProduct(browser,datas):
	iname,iimage,ietalase,imin_buy,iprice,icondition,idescription,ivideo,ivariant,iweight,iinsurance = datas
	if(browser.title != 'Tambah Produk | Tokopedia'):
		browser.get('https://www.tokopedia.com/product-add-v2.pl')
	#image
	for row in iimage: 
		inputById(browser,'ngf-pickfiles-nav1',row,'image') 
	inputById(browser,'p-name',iname) 
	selectEtalase(browser,'p-menu-id',ietalase) 
	inputById(browser,'p-min-order',imin_buy) 
	inputById(browser,'p-price',iprice)
	inputById(browser,'p-description',idescription)
	inputById(browser,'p-weight',iweight) 
	pRecommendation = browser.find_elements_by_xpath("//span[@ng-repeat='cat_recomm in category_recommendation_list']")
	screenCenter(browser,pRecommendation[0])
	pRecommendation[0].click()
	#SUBMIT
	delay(10)
	print('[+] Submit Upload Product')
	resp = browser.find_element_by_id('s-save-prod')
	screenCenter(browser,resp)
	resp.click()
	#WAIT UNTIL UPLOADED
	while(True):
		try:
			if browser.title != 'Tambah Produk | Tokopedia':
				resp = browser.find_element_by_id('message-div')
				print('[+] message : %s'%resp.text)
				break
			else:
				print('[-] Except @Tambah Produk | %s'%browser.title)
				delay(10)
		except ElementNotVisibleException as e:
			print e

def prepare_input(datas):
	data_pid,name,image,etalase,min_buy,price,condition,description,video,variant,weight,insurance = datas
	print('[+] {} - {}'.format(data_pid,name))
	iimage = [img for img in downloadImage(os.getcwd()+'/images',image.split('\n'))]
	iname = name
	ietalase = etalase
	imin_buy = min_buy
	iprice = price
	icondition = condition
	idescription = description
	ivideo = video.split('\n')
	ivariant = variant
	iweight = weight
	iinsurance = insurance
	return [iname,iimage,ietalase,imin_buy,iprice,icondition,idescription,ivideo,ivariant,iweight,iinsurance]


def doUpdateStatus(datas):
	status = '1'
	data_pid,name,image,etalase,min_buy,price,condition,description,video,variant,weight,insurance = datas
	sql = """
	UPDATE {0} SET upload_status='{1}' where `data_pid`={2}
	""".format(gtable_detail,status,data_pid)
	run_sql(sql,'put')

def run():
	#INITIALIZING
	browser = init_browser(root)
	printo('STARTING','center',True)
	print('[+] Get product list')
	while(True):
		datas = get_product_list()[0]
		if(len(datas) > 0): 
			resp = prepare_input(datas)
			doInputProduct(browser,resp)
			doUpdateStatus(datas)
		else:
			print('[-] No data to get detail | get data list first.')
			break
	browser.quit()
	printo('FINISH','center',True) 

def main():
	run()
	
if __name__ == '__main__':
	main()