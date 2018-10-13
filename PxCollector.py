import time
import requests
from bs4 import BeautifulSoup
import zipfile
import os

print('\tWelcome In ZuCollector [ Smarter Proxies Grabber ]')
print('\tCoded By: Mostafa M. Mead')
print('\tCoded With: Python-3')

input('\nPlease Press Enter To Start Grabbing ')

session = requests.Session()
session.headers.update({
	'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:39.0) Gecko/20100101 Firefox/39.0'
})

proxies_list = []

def start_grab(site):
	count = 0
	grab_req = session.get(site)
	grab_src = grab_req.content
	soup = BeautifulSoup(grab_src , 'lxml')
	for h3 in soup.find_all('h3'):
		count += 1
		grab_url = h3.a['href']
		grab_req = session.get(grab_url)
		grab_src = grab_req.content
		soup = BeautifulSoup(grab_src , 'lxml')
		try:
			proxies_span = soup.find_all('span' , {'style':'font-weight: bold;'})[2].text
		except:
			try:
				main_div = soup.find('div' , {'itemprop':'description articleBody'})
			except:
				pass
			else:
				file_url = main_div.find_all('a')[1]['href']
				file_name = 'proxy{}.zip'.format(count)
				with open(file_name , 'wb') as f:
					download_req = requests.get(file_url , stream=True)
					for chunk in download_req.iter_content(8192):
						f.write(chunk)
				zip_ref = zipfile.ZipFile(file_name, 'r')
				zip_contents = zip_ref.namelist()
				zip_ref.extractall()
				for zip_content in zip_contents:
					if '.txt' in zip_content:
						with open(zip_content) as f:
							lines = f.read().split('\n')
						for line in lines:
							print(line)
							proxies_list.append(line)
					os.remove(zip_content)
				zip_ref.close()
				os.remove(file_name)
		else:
			proxies_list.append(proxies_span)
			print(proxies_span)

def main():
	start_grab('http://www.freshnewproxies24.top/')
	for proxy in proxies_list:
		proxies_file = open('proxies_file.txt' , 'a+')
		proxies_file.write(proxy + "\n")
		proxies_file.close()

if __name__ == '__main__':
	try:
		main()
	except Exception as e:
		print(e);time.sleep(1000)
	else:
		print('Collecting Proxies Done Succesfully');time.sleep(1000)