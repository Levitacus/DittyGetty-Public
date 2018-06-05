import time
import json
import pprint
from helperFuncs import timeObject
from songInfo import SongInfo
import re
import urllib2
from bs4 import BeautifulSoup
from scraper import Scraper

class DailyPlaylist(Scraper):

	def __init__(self, playlist_name):
		super(DailyPlaylist, self).__init__()
		self._playlist_name = playlist_name

		

	def scrape_body(self):
		self.set_page('http://dailyplaylists.com/%s/' % (self._playlist_name))
		self.generate_page_scraper()
		#print(self._page_scraper)
		#find page for widget to load
		widget_page = self._page_scraper.find('iframe')['src']
		#print(widget_page)
		#widget_page = "http://composer.nprstations.org/widgets/iframe/daily.html?station=520a4969e1c85ef575dd2484"
		self.set_page(widget_page)
		self.generate_page_scraper()



		time.sleep(3)

		#print(self._page_scraper)

		#song_data_list = self.findElementClassTokens('div', 'a b c d e f g h i j k l', "||")

		json_text = self._page_scraper.find('script',  {'id':'resource'}).get_text()

		scraped_dict = json.loads(json_text)

		#pprint.pprint(scraped_dict['tracks']['items'][0])

		#print(scraped_dict['tracks']['items'][0]['track']['name'])
		#print(scraped_dict['tracks']['items'][0]['track']['artists'][0]['name'])

		


		scraped_song_list = list()

		for song_data in scraped_dict['tracks']['items']:
			scraped_song_list.append(SongInfo(song_data['track']['name'].strip().encode('ascii', 'ignore'), song_data['track']['artists'][0]['name'].strip().encode('ascii', 'ignore'), ""))

	
		return scraped_song_list;		

	def scrape_run(self):
		
		new_playlist = self.scrape_body()

		if not new_playlist:
			new_playlist = self.scrape_body()

		return new_playlist

if __name__ == "__main__":
	jpr = DailyPlaylist("crack-in-the-road")
	print("test")
	for song in jpr.scrape_run():
		print song.toString()
		pass

