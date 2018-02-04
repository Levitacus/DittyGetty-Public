from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC



#Program only returns a single song name

#just proof of concept for webscraping from JPR's website



driver = webdriver.PhantomJS()

driver.get('http://composer.nprstations.org/widgets/iframe/searchlist.html?station=520a4969e1c85ef575dd2484')



#p_element = driver.find_element_by_class_name('track_name')

#p_element = driver.find_element_by_xpath('//div[@id="episodes_container"]//div[@id="episodes_container_content"]//div[@class="episode"]')

#p_elementList = driver.find_element_by_class_name('episode_name clearfix')



try:

    #p_element = WebDriverWait(driver, 10).until(

       #EC.presence_of_element_located((By.XPATH, '//div[@class="episode"]'))

    #)



    p_element = WebDriverWait(driver, 10).until(

        EC.presence_of_element_located((By.XPATH, '//div[@class="track_name clearfix"]'))

    )

    #track_ele = p_element.find_element_by_class_name('track_name clearfix')

    print(p_element.get_attribute("textContent"))

finally:

    driver.quit()





#print(p_elementList)

#print(p_element.tag_name)

#print(p_element.get_attribute('div'))