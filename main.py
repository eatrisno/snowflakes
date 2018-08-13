import os
from helper import initialization
from helper import printo
from helper import info_OS
import getList as mod1
import getDetail as mod2
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
	printo(" 0. Exit")
	printo('','center',True)

def main():
	info_OS()
	while(initialization()):
		os.system('clear')
		menu()
		input = raw_input("> ")
		os.system('clear')
		if( input == '1' ):
			mod1.run(root)
		elif( input == '2'):
			mod2.run(root)
		elif( input == '3'):
			commingSoon()
		elif( input == '4'):
			commingSoon()
		elif( input == '0'):
			print('Bye..')
			break
		else:
			menu()
			print('No Match')
			print('nb: Choose with number.')
		#for hold screen until press any key
		x=raw_input('Press Enter to continue.')

if __name__ == '__main__':
	main()
