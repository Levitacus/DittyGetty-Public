#from selenium import webdriver

#from selenium.webdriver.common.by import By

#from selenium.webdriver.support.ui import WebDriverWait

#from selenium.webdriver.support import expected_conditions as EC

#from selenium.webdriver.common.keys import Keys

import time

from helperFuncs import timeObject

#This is unnecessary for now
#from songInfo import scrapedSongInfo
from songInfo import SongInfo

import re
import urllib2
from bs4 import BeautifulSoup





#full list of functions and code for parsing any npr station's schedule


def parseListLabel(listName, label):
	parsedList = list()
	for element in listName:
		if label in element:
			parsedList.append(element.replace(label, ''))

	return parsedList

def findElementClass(elementTag, className, soup):
	print className
	elements = soup.find_all(elementTag,  {'class':className})
	content = list()
	for element in elements:
		#need to encode to utf-8 to fix the problem
		content.append(element.text.encode("utf-8"))

	return content


def getElementField(elementTag, className):

	element = driver.find_element_by_xpath("//%s[@class='%s']" % (elementTag, className))

	return element.get_attribute('innerHTML')



def getElementsField(elementTag, className):

	elements = driver.find_elements_by_xpath("//%s[@class='%s']" % (elementTag, className))

	attributeList = list()

	for element in elements:

		attributeList.append(element.get_attribute('innerHTML'))



	return attributeList



def trimListTime(scrapedSongList, beginTime, endTime):

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





def nprByTime(beginTime, endTime, soup):

	songTimeList =  findElementClass('li', '\\"whatson-startTime\\"', soup)

	songDataList = findElementClass('div', '\\"label\\"', soup)

	songArtistList = parseListLabel(songDataList, 'ARTIST:')
	songNameList = parseListLabel(songDataList, 'TITLE:')

	#get rid of weird error, talk showing up in titles but is not in html
	songNameList[:] = [x for x in songNameList if x != "Talk"]

	scrapedSongList = list()



	i = 0

	for times in songArtistList:

		song = SongInfo(songNameList[i], songArtistList[i], songTimeList[i])

		scrapedSongList.append(song)

		i += 1



	scrapedSongList = trimListTime(scrapedSongList, beginTime, endTime)

	

	# for song in scrapedSongList:

		# print(song.toString())
		
	return scrapedSongList
		
def getList(month, day, year, start, end):
	
	# startTime = "2:00"
	# endTime = "14:00"


	site = ('https://api.composer.nprstations.org/v1/widget/520a4969e1c85ef575dd2484/day?date=%d-%02d-%02d&callback=jQuery17205943383084192947_1518308649099&format=jsonp&_=1518310998172' % (year, month, day))

	print site

	page = urllib2.urlopen(site)

	soup = BeautifulSoup(page, 'lxml')

	scrapedSongList = nprByTime(start, end, soup)
	
	# finalList = list()
	
	# i = 0
	
	# for times in scrapedSongList:
		# song = SongInfo(scrapedSongList[i].songName, scrapedSongList[i].songArtist)
		# finalList.append(song)
		# i += 1
		
	
	return scrapedSongList;

