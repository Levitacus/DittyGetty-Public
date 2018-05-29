import time
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

		

		
	def scrape_run(self):
		

		self.set_page('http://dailyplaylists.com/%s/' % (self._playlist_name))
		self.generate_page_scraper()
		#find page for widget to load
		widget_page = self._page_scraper.find('iframe')['src']

		self.set_page(widget_page)
		self.generate_page_scraper()

		#print(self._page_scraper())

		song_data_list = self.findElementClassTokens('div', 'track-row-info ', "||")


		scraped_song_list = list()

		for song_data in song_data_list:
			scraped_song_list.append(SongInfo(song_data[0].strip().encode('ascii', 'ignore'), song_data[1].strip().encode('ascii', 'ignore'), ""))

	
		return scraped_song_list;

if __name__ == "__main__":
	jpr = DailyPlaylist("bassrush")
	print("test")
	for song in jpr.scrape_run():
		print song.toString()
		pass

