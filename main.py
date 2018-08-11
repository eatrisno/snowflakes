import download_tokopedia as download

def doUpload():
	print("comming soon")

def main():
	input = ''
	while(input.lower() != 'exit'):
		print("===================Menu======================")
		print("| 1. Download ")
		print("| 2. Upload ")
		print("=============================================")
		input = raw_input(">")
		if( input == '1' ):
			download.get_product()
		elif( input == '2'):
			upload()
		else:
			print('No Match')

if __name__ == '__main__':
	main()
