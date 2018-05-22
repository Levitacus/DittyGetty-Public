import time
from helperFuncs import timeObject
from songInfo import SongInfo
import re
import urllib2
from bs4 import BeautifulSoup
from scraper import Scraper

class NPR(Scraper):

	def __init__(self, station_code):
		super(NPR, self).__init__()
		self._station_code = station_code
		

	#full list of functions and code for parsing any npr station's schedule

	#returns a list of song objects
	def parse_song_data(self, song_data):
		song_time = song_data[0]


		if song_data.index("COMPOSER:") if "COMPOSER:" in song_data else None:
			song_artist = song_data[song_data.index("COMPOSER:") + 1] 

		elif song_data.index("ARTIST:") if "ARTIST:" in song_data else None:
			song_artist = song_data[song_data.index("ARTIST:") + 1] 
		else:
			song_artist = ""

		if song_data.index("TITLE:") if "TITLE:" in song_data else None:
			song_title = song_data[song_data.index("TITLE:") + 1] 
		else:
			song_title = ""
		

		song = SongInfo(song_title.encode('ascii', 'ignore'), song_artist.encode('ascii', 'ignore'), song_time.encode('ascii', 'ignore'))
		
		return song

		

	def nprByTime(self, beginTime, endTime):


		song_data_list = self.findElementClassTokens('div', '\\"single-song\\"', "||")

		scraped_song_list = list()

		for song_data in song_data_list:
			scraped_song_list.append(self.parse_song_data(song_data))



		scraped_song_list = Scraper.trimListTime(scraped_song_list, beginTime, endTime)

		return scraped_song_list

		
	def scrape_run(self, month=1, day=1, year=2018, start="00:00", end="23:59"):
	

		self.set_page('https://api.composer.nprstations.org/v1/widget/%s/day?date=%d-%02d-%02d&callback=jQuery17205943383084192947_1518308649099&format=jsonp&_=1518310998172' % (self._station_code, year, month, day))
		self.generate_page_scraper()


		scraped_song_list = self.nprByTime(start, end)
	
		return scraped_song_list;

if __name__ == "__main__":
	jpr = NPR("520a4969e1c85ef575dd2484")
	nspr = NPR("51c0a723e1c84725df134f87")
	print("test")
	for song in jpr.scrape_run(12, 01, 2017):
		print song.toString()
		pass

