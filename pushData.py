from helper import *

def get_product_list():
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
	print sql
	myresult = run_sql(sql,'get')
	return myresult

def run():
	#INITIALIZING
	browser = init_browser(root)
	printo('STARTING','center',True)
	try:
		var = get_product_list()
		print var
	except Exception as e:
		print e
	browser.quit()
	printo('FINISH','center',True)

def main():
	run()

if __name__ == '__main__':
	main()