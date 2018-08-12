import os
import getList as mod1
import getDetail as mod2

def doUpload(mode):
	print("comming soon")

def main():
	root = False
	input = ''
	while(True):
		os.system('clear')
		print("===================Menu======================")
		print("| 1. Get List ")
		print("| 2. Get Detail ")
		print("| 3. Upload ")
		print("| 0. Exit ")
		print("=============================================")
		input = raw_input(">")
		os.system('clear')
		if( input == '1' ):
			mod1.run(root)
		elif( input == '2'):
			mod2.run(root)
		elif( input == '3'):
			doUpload(root)
		elif( input == '0'):
			print('Bye..')
			break
		else:
			print('No Match')

if __name__ == '__main__':
	main()
