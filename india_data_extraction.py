from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import os,time
import bs4
from bs4 import BeautifulSoup
#============== here date should be replaced by day==============
import requests
import datetime
import subprocess
import pandas as pd

file=open('start_time.txt','r')
start_time=file.readlines()[0]
file.close()

#Filling non iterating fields in the form.
#changing download properties.
#downloading file to current working directory.
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showhenStarting",False)
fp.set_preference("browser.download.dir",os.getcwd())
fp.set_preference("browser.helperApps.neverAsk.saveToDisk","application/xls;text/csv")#Download file and specifying its $$$ MIME type $$$.
 
web = webdriver.Firefox(firefox_profile = fp)
web.get('https://seismo.gov.in/MIS/riseq/Earthquake/archive')

time.sleep(2)

time_type_selector = web.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul/form/div[5]/div/fieldset/div/div/label[1]')
time_type_selector.click()

custom_area_selection = web.find_element_by_xpath('//*[@id="region"]')
custom_area_selection_object = Select(custom_area_selection)
custom_area_selection_object.select_by_value('C')

north = "60"
minimum = web.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul/form/div[1]/div/fieldset/div/div[2]/div[2]/div/div/div/input')
minimum.send_keys(north)

south = "30"
maxmum = web.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul/form/div[1]/div/fieldset/div/div[2]/div[4]/div/div/div/input')
maxmum.send_keys(south)

east = "150"
minimum = web.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul/form/div[1]/div/fieldset/div/div[2]/div[3]/div[2]/div/div/input')
minimum.send_keys(east)

west = "0"
maxmum = web.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul/form/div[1]/div/fieldset/div/div[2]/div[3]/div[1]/div/div/input')
maxmum.send_keys(west)

custom_magnitude_selection = web.find_element_by_xpath('//*[@id="mag_type"]')
custom_magnitude_selection_object = Select(custom_magnitude_selection)
custom_magnitude_selection_object.select_by_value('MW')

start = web.find_element_by_xpath('//*[@id="start_time"]')
start.click()
start.send_keys(start_time)

# Finding the end time from the info on the website.
html_source = web.page_source
soup= bs4.BeautifulSoup(html_source,'lxml')
list_of_span = soup.find_all(attrs={"data-placement":"top"})
contains_end_time=list_of_span[1]['title']
contains_end_time_list=contains_end_time.split(' ')
end_time=contains_end_time_list[-2]

end = web.find_element_by_xpath('//*[@id="end_time"]')
end.click()
end.send_keys(end_time)

apply_ = web.find_element_by_xpath('/html/body/div[1]/div[1]/div/ul/form/div[6]/div[3]/div/input')
apply_.click()
time.sleep(2)

changing_to_list = web.find_element_by_xpath('//*[@id="maptoggle"]')
changing_to_list.click()
quit()

file1=open('last.csv','a')
file1.write('Date Time|latitude|longitude|depth|magnitude|location|    #magnitude type=[MW] \n')
#writing data into a file.
while True:

	html_source = web.page_source
	soup= bs4.BeautifulSoup(html_source,'lxml')
	list_of_tbody = soup.find_all(name='tbody')
	list_of_rows = list_of_tbody[1].find_all(name='tr')
	for i in list_of_rows:
		elements=(i.text).replace('[MW]                        ','').split('\n')
		final_string=''
		for j in elements[1:-1]:
			final_string=final_string + j +'|'
		file1.write(final_string[:-1]+'\n')

	next_page = web.find_element_by_xpath('//*[@id="archive_eqs_next"]')
	print(next_page.get_attribute('class'))
	if 'paginate_button next disabled'==str(next_page.get_attribute('class')):
		break
	next_page.click()
	time.sleep(2)
file1.close()

#quitting the browser.
web.quit()

file=open('start_time.txt','w')
df = pd.read_csv('last.csv',sep='|')
end_time_raw = df['Date Time'].to_list()[-1].split(' ')[0].split('-')
end_time = end_time_raw[2]+'-'+end_time_raw[1]+'-'+end_time_raw[0]
file.write(end_time)
file.close()
