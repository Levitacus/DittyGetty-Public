from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys

import time

from helperFuncs import timeObject

from songInfo import scrapedSongInfo

import re





#Program only returns a single song name

#just proof of concept for webscraping from JPR's website



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

		

		if( not timeObject.beforeTime(songTimeObject, beginTimeObject)):

			scrapedSongList.append(song)



	#songTimeObject = timeObject()

	#songTimeObject.stringToTime(scrapedSongList[0].songTime)

	#if(timeObject.beforeTime(songTimeObject, beginTimeObject)):

		#scrapedSongList.remove(scrapedSongList[0])

		#print "test"



def nprByDateTime(scrapeDate, beginTime, endTime):

	print "test"


driver = webdriver.PhantomJS()

driver.get('http://composer.nprstations.org/widgets/iframe/daily.html?station=520a4969e1c85ef575dd2484')

driver.save_screenshot('screen.png')





time.sleep(3)

songTimeList =  getElementsField('li', 'whatson-startTime')

songNameList = getElementsField('div', 'song-data truncate')

songArtistList = getElementsField('div', 'song-data')





scrapedSongList = list()



i = 0

for times in songTimeList:

	song = scrapedSongInfo(songNameList[i], songArtistList[i], songTimeList[i])

	scrapedSongList.append(song)

	i += 1



trimListTime(scrapedSongList, '2:30AM', '9:30PM')

print len(songTimeList)



for song in scrapedSongList:

	print(song.toString())



	





#p_element = driver.find_element_by_id('nprds_widget')

#elem = p_element.find_element_by_xpath("//*")

#html_content = elem.get_attribute("outerHTML")



#print(html_content)

#p_element = driver.find_element_by_xpath('//div[@id="episodes_container"]//div[@id="episodes_container_content"]//div[@class="episode"]')

#p_elementList = driver.find_element_by_class_name('episode_name clearfix')
