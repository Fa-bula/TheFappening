#!/usr/bin/python
import urllib3
from bs4 import BeautifulSoup

headers = {'user_agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
forbidden_words = ['.mkv', '.wmv', 'gay', '.flv', '.avi', '.mov', 'zoo', 'transsexual', 'shemale', 'grand']
HOSTNAME = 'http://leporno.org/'
#free disk space in GB
SPACE_LEFT = 0.0

def get_good_links(manager):
	req = manager.request('GET', 'http://leporno.org/', headers=headers)
	soup = BeautifulSoup(req.data)
	all_hrefs = []
	for link in soup.find_all('a'):
        	if 'class' in link.attrs:
                	if 'copylp' in link['class']:
                        	all_hrefs.append('http://leporno.org/' + link.get('href'))
	return [all_hrefs[i] for i in range(1, 11)]

def get_size_of_torrent(soup):
	for table in soup.find_all('table'):
		if 'attach' in table.get('class', []):
			for child in table.descendants:
				if child.string and ('MB' in child.string or 'GB' in child.string):
					if 'MB' in child.string:
						return float(child.string[:-3]) / 1024.0
					else:
						return float(child.string[:-3])

def download_torrent_file(manager, link_to_seek):
	global SPACE_LEFT
	print 'trying to download ' + link_to_seek
	req = manager.request('GET', link_to_seek, headers=headers)
	soup = BeautifulSoup(req.data)
	torrent_size = get_size_of_torrent(soup)
	if torrent_size > SPACE_LEFT:
		return 'torrent too big'
	
	for word in forbidden_words:
		if word in soup.get_text():
			return 'torrent have forbidden word: ' + word
	
	for link in soup.find_all('a'):
		if 'seedmed' in link.get('class', []) or 'genmed' in link.get('class', []):
			with open('/home/user/The_Fappening/.temp/' + soup.title.string[:10] + '.torrent', 'wb') as write_file:
				#http = urllib3.PoolManager()
				download = manager.request('GET', HOSTNAME + link.get('href'))
				data = download.data
				write_file.write(data)
				download.release_conn()
				SPACE_LEFT -= torrent_size
				return 'torrent downloaded'

if  __name__ ==  "__main__" :
	with open('/home/user/The_Fappening/.temp/free_space', 'r') as read_file:
		SPACE_LEFT = float(read_file.read())
	
	manager = urllib3.PoolManager()
	good_links = get_good_links(manager)
	for link in good_links:
		print download_torrent_file(manager, link), '\n'
	
	with open('/home/user/The_Fappening/.temp/free_space', 'w') as write_file:
		write_file.write(str(SPACE_LEFT))
