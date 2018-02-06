from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from helperFuncs import timeObject
import re


#Program only returns a single song name
#just proof of concept for webscraping from JPR's website

songList = list()


#time1 = timeObject()
#time1.stringToTime('12:33AM')
#print(time1.toString())
	

def getTrackData(trackElement):
	return trackElement.find_element_by_class_name('track_field_data')

def parseData(trackElements, startTime, endTime):
	for element in trackElements:
		endTimeO = timeObject()
		endTimeO.hour = endTime
		startTimeO = timeObject()
		startTimeO.hour = startTime

		nameEle = element.find_element_by_class_name("track_info")
		timeEle = element.find_element_by_class_name("track_start_time")
		dateEle = element.find_element_by_class_name("track_date")
		#nameEles = nameEle.find_element_by_class_name("track_name clearfix")
		#artistEle = trackInfoEle.find_element_by_class_name('artist track_field clearfix')
		#albumEle = trackInfoEle.find_element_by_class_name('album track_field clearfix')
		nameText = nameEle.get_attribute('textContent')
		dateText = dateEle.get_attribute('textContent')
		timeText = timeEle.get_attribute('textContent')

		songTime = timeObject()
		songTime.stringToTime(timeText)
		if(timeObject.afterTime(songTime, endTimeO)):
			break
		elif(timeObject.beforeTime(songTime, startTimeO)):
			continue

		nameText = re.sub( '\s+', ' ', nameText ).strip()
		timeText = timeText.replace(" ", "")
		timeText = timeText.replace("\n", "")
		dateText = dateText.replace(" ", "")
		dateText = dateText.replace("\n", "")
		#print(getTrackData(artistEle).get_attribute('textContent'))
		#print(getTrackData(albumEle).get_attribute('textContent'))
		#print(timeText + dateText + nameText + '\n')    

		nameTokens = nameText.split(':')
		nameTokens[0] = nameTokens[0].replace("ARTIST", "").strip()
		nameTokens[1] = nameTokens[1].replace("ALBUM", "").strip()
		fullString = (timeText + " " + dateText 
		+ " Song Name: " + nameTokens[0] + " Artist: " + nameTokens[1] + '\n')

		if fullString not in songList:
			songList.append(fullString)



driver = webdriver.PhantomJS()
driver.set_window_size(1366,768)
driver.get('http://composer.nprstations.org/widgets/iframe/searchlist.html?station=520a4969e1c85ef575dd2484')

#p_element = driver.find_element_by_class_name('track_name')
#p_element = driver.find_element_by_xpath('//div[@id="episodes_container"]//div[@id="episodes_container_content"]//div[@class="episode"]')
#p_elementList = driver.find_element_by_class_name('episode_name clearfix')

try:
	p_elements = WebDriverWait(driver, 10).until(
	EC.presence_of_all_elements_located((By.XPATH, '//div[@class="episode"]'))
	)


	#driver.execute_script("window.scrollTo(0, 0);")

	p_elements = WebDriverWait(driver, 10).until(
	EC.presence_of_all_elements_located((By.XPATH, '//div[@class="episode"]'))
	)
	element = driver.find_element_by_xpath('//div[@id="episodes_container"]')
	driver.execute_script("window.scrollTo(500, 500);")

	#select = Select(driver.find_element_by_id('timepicker-button'))
	#select.select_by_visible_text('12:00 AM')
	driver.find_element_by_id('datepicker').click()
	date = driver.find_element_by_xpath("//a[text() = '4']")
	date.click()

	startTime = 2
	endTime = 14

    	#ele = driver.find_element_by_id('timepicker-button')
	#ele.click()
        #select = driver.find_element_by_id('timepicker')
	#ele.send_keys(Keys.ARROW_DOWN)
	#ele.send_keys(Keys.ARROW_DOWN)
	#ele.send_keys(Keys.ENTER)
	#driver.find_element_by_id('search_button').click()
	#driver.find_element_by_id('widget_container').click()
	#time.sleep(1)
	#p_element = WebDriverWait(driver, 10).until(
        #EC.presence_of_all_elements_located((By.XPATH, '//div[@class="clearfix episode_track    "]')))

    	#parseData(p_element, endTime)
	
	ele = driver.find_element_by_id('timepicker-button')
	ele.click()
	select = driver.find_element_by_id('timepicker')
	ele.send_keys(Keys.ARROW_DOWN)

	for i in range(0, startTime):
		ele.send_keys(Keys.ARROW_DOWN)
		ele.send_keys(Keys.ARROW_DOWN)

	ele.send_keys(Keys.ENTER)
	driver.find_element_by_id('search_button').click()
	driver.find_element_by_id('widget_container').click()
	time.sleep(.5)
	p_element = WebDriverWait(driver, 10).until(
	EC.presence_of_all_elements_located((By.XPATH, '//div[@class="clearfix episode_track    "]')))

	parseData(p_element, startTime, endTime)

	for i in range(0, (endTime - startTime) / 3 + 1):
		print("Reading episode" + str(i) + "\n")
		ele = driver.find_element_by_id('timepicker-button')
		ele.click()
		select = driver.find_element_by_id('timepicker')
		ele.send_keys(Keys.ARROW_DOWN)
		ele.send_keys(Keys.ARROW_DOWN)
		ele.send_keys(Keys.ARROW_DOWN)
		ele.send_keys(Keys.ARROW_DOWN)
		ele.send_keys(Keys.ARROW_DOWN)
		ele.send_keys(Keys.ARROW_DOWN)
		ele.send_keys(Keys.ENTER)
		driver.find_element_by_id('search_button').click()
		driver.find_element_by_id('widget_container').click()
		time.sleep(.5)
		try:
			p_element = WebDriverWait(driver, 2).until(
			EC.presence_of_all_elements_located((By.XPATH, '//div[@class="clearfix episode_track    "]')))
			parseData(p_element, startTime, endTime)
		except:
			print("No Songs found at time\n")


	#p_elements = WebDriverWait(driver, 10).until(
	#EC.presence_of_all_elements_located((By.XPATH, '//div[@class="episode"]')))

	#p_element = WebDriverWait(driver, 10).until(
	#EC.presence_of_all_elements_located((By.XPATH, '//div[@class="clearfix episode_track    "]')))

	#parseData(p_element)

    	#print(len(p_elements))

	for songs in songList:
		print songs.encode('utf-8')
finally:
    
	driver.save_screenshot('screen.png')
	driver.quit()




#print(p_elementList)
#print(p_element.tag_name)
#print(p_element.get_attribute('div'))
