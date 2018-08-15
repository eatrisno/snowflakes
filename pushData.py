from helper import *

def run():
	#INITIALIZING
	browser = init_browser(root)
	printo('STARTING','center',True)
	try:
		print('yeay')
	except Exception as e:
		print e
	browser.quit()
	printo('FINISH','center',True)

def main():
	run()

if __name__ == '__main__':
	main()