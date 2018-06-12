import time
from helperFuncs import timeObject
from songInfo import SongInfo
import re
import urllib2
from bs4 import BeautifulSoup

class Scraper(object):
	
	def __init__(self):
		self._page = ""
		self._page_scraper = BeautifulSoup(self._page, 'lxml')


	def get_page(self):
		return self._page
	
	def set_page(self, new_page):
		self._page = new_page

	def generate_page_scraper(self):
		opened_page = urllib2.urlopen(self._page)
		self._page_scraper = BeautifulSoup(opened_page, 'lxml')

	#full list of functions and code for parsing any npr station's schedule
	@classmethod
	def parseListLabel(cls, listName, label):
		parsedList = list()
		for element in listName:
			if label in element:
				parsedList.append(element.replace(label, ''))

		return parsedList

	def findElementClassText(self, elementTag, className, new_separator="", driver=None):
		if not driver:
			driver = self._page_scraper
		elements = driver.find_all(elementTag,  {'class':className})
		content = list()
		for element in elements:
			#need to encode to utf-8 to fix the problem
			content.append(element.get_text(separator=new_separator))

		return content

	def findElementClassTokens(self, elementTag, className, new_separator, driver=None):
		found_text_list = self.findElementClassText(elementTag, className, new_separator, driver)
		text_tokens_list = list()

		for found_text in found_text_list:
			text_tokens_list.append(found_text.split(new_separator))

		return text_tokens_list

	def findElementClass(self, elementTag, className, driver=None):
		if not driver:
			driver = self._page_scraper
		#print className
		elements = driver.find_all(elementTag,  {'class':className})

		return elements


	def getElementField(elementTag, className):

		element = driver.find_element_by_xpath("//%s[@class='%s']" % (elementTag, className))

		return element.get_attribute('innerHTML')



	def getElementsField(elementTag, className):

		elements = driver.find_elements_by_xpath("//%s[@class='%s']" % (elementTag, className))

		attributeList = list()

		for element in elements:

			attributeList.append(element.get_attribute('innerHTML'))



		return attributeList


	@classmethod
	def trimListTime(cls, scrapedSongList, beginTime, endTime):

		beginTimeObject = timeObject()

		endTimeObject = timeObject()

		beginTimeObject.stringToTime(beginTime)

		endTimeObject.stringToTime(endTime)



		trimmedScrapedSongList = list()



		for song in scrapedSongList:

			songTimeObject = timeObject()

			songTimeObject.stringToTime(song.songTime)

		

			if( not timeObject.beforeTime(songTimeObject, beginTimeObject) and not timeObject.afterTime(songTimeObject, endTimeObject)):

				trimmedScrapedSongList.append(song)



		return trimmedScrapedSongList



	def scrape_run(self):
		pass

