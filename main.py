import os
from helper import init_driver
from helper import printo
from helper import info_OS
from helper import init_browser
from helper import check_internet
import getList as mod1
import getDetail as mod2
import pushData as mod3
#Are You USER ?
root = True

def commingSoon():
	print("Comming soon..")
	
def menu():
	printo('','center',True)
	printo(' Welcome To SnowFlakes APP ','center',True)
	printo('','center',True)
	printo('Menu','center',False)
	printo('','center',True)
	printo(" 1. Get List")
	printo(" 2. Get Detail")
	printo(" 3. Upload")
	printo(" 4. Update")
	printo(" 9. Automated")
	printo(" 0. Exit")
	printo('','center',True)

def initializaion():
	printo('INIZIALIZATION','center',True)
	info_OS()
	check_internet()
	os.system('clear')
	printo('FINISH INIZIALIZATION','center',True)

def clear():
	for i in range(10):
		print('\n')

def automated():
	mod1.run()
	mod2.run()

def main():
	printo('HI. THERE !','center',False) #True headless | false not headless
	initializaion()
	clear()
	while(True):
		menu()
		vinput = raw_input("> ")
		clear()
		if  ( vinput == '1'):
			mod1.run()
		elif( vinput == '2'):
			mod2.run()
		elif( vinput == '3'):
			mod3.run()
		elif( vinput == '4'):
			commingSoon()
		elif( vinput == '9'):
			automated()
		elif( vinput == '0'):
			print('Bye..')
			break
		print('last run : {}'.format(vinput))
if __name__ == '__main__':
	main()
