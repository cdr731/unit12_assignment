#!/usr/bin/env python
# coding: utf-8

# Unit 12 Assignment - Mission to Mars
# by Christopher Reutz

# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import re
import time
import pandas as pd

def scrape():

	# Initial dictionary to store scraping code
	mtm_data = {}

	# Initialize executable path for the chromedriver
	executable_path = {'executable_path': 'chromedriver.exe'}
	browser = Browser('chrome', **executable_path, headless=True)

	# --- Scrape "NASA Mars News" website for news info ---
	mars_news_url = 'https://mars.nasa.gov/news/'

	# Retrieve page with Splinter
	browser.visit(mars_news_url)
	time.sleep(2)

	# Create BeautifulSoup object and parse with 'html.parser'
	html = browser.html
	soup = bs(html, "html.parser")

	# Initialize lists to put titles and paragraphs into
	news_title_list = []
	news_p_list = []

	# Extract all article titles and paragraphs and put into lists
	results = soup.find_all('li', class_='slide')
	for result in results:
			# Error handling
		try:
			# Identify and return the news title
			nasa_news_title = result.find('div', class_="content_title").a.text
			# Identify and return the news paragraph text
			nasa_news_p = result.find('div', class_="article_teaser_body").text

			# Print results only if title and paragraph text are available
			if (nasa_news_title and nasa_news_p):
				news_title_list.append(nasa_news_title)
				news_p_list.append(nasa_news_p)
		except AttributeError as e:
			print(e)

	# Latest "NASA Mars News" news title -- the first article (index=0)
	# news_title = news_title_list[0]
	mtm_data['news_title'] = news_title_list[0]

	# Latest "NASA Mars News" next paragraph text -- the first article (index=0)
	# news_p = news_p_list[0]
	mtm_data['news_p'] = news_p_list[0]

	# --- Scrape "JPL Mars Space Images" to get a URL for the featured image ---

	# Use Splinter to open up web browser to main page
	jpl_domain = 'https://www.jpl.nasa.gov'
	jpl_path = '/spaceimages/?search=&category=Mars'
	jpl_url = jpl_domain + jpl_path
	browser.visit(jpl_url)
	time.sleep(2)

	# Open the full featured image
	browser.click_link_by_partial_text('FULL IMAGE')
	time.sleep(1)

	# Open and parse the page with 'more info'
	browser.click_link_by_partial_text('more info')
	time.sleep(1)
	html = browser.html
	soup = bs(html, 'html.parser')

	# Obtain URL for the full-size featured image
	main_img_path = soup.find('img', class_="main_image")['src']
	# featured_image_url = jpl_domain + main_img_path
	mtm_data['featured_image_url'] = jpl_domain + main_img_path

	# Open and parse the Twitter account
	mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
	browser.visit(mars_weather_url)
	time.sleep(2)
	html = browser.html
	soup = bs(html, 'html.parser')

	# Find the latest weather report
	results = soup.find_all('div', class_='js-tweet-text-container')
	for result in results:
		tweet_txt = result.find('p').text
		try:
			anchor_txt = result.find('a').text
		except:
			anchor_txt = ''
		if re.search(r'^InSight sol', tweet_txt, re.IGNORECASE): break 

	# Remove anchor url from the weather tweet
	regex = re.compile(anchor_txt)
	# mars_weather = regex.sub('', tweet_txt)
	mtm_data['mars_weather'] = regex.sub('', tweet_txt)

	# --- Scrape "Mars Facts" website table ---

	# Use Pandas to pull html table and put into a list
	marsfacts_url = 'https://space-facts.com/mars/'
	marsfacts_list = pd.read_html(marsfacts_url)

	# Put list into a dataframe and format
	marsfacts_df = marsfacts_list[0]
	marsfacts_df.columns = ['Description', 'Value']
	marsfacts_df.set_index('Description', inplace=True)

	# Convert dataframe into an html table string
	# marsfacts_table = marsfacts_df.to_html()
	mtm_data['marsfacts_table'] = marsfacts_df.to_html()

	# --- Scrape "Mars Hemispheres" images at USGS Astrogeology site ---

	# Use Splinter to open up web browser to main page
	usgs_domain = 'https://astrogeology.usgs.gov'
	usgs_path = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	usgs_url = usgs_domain + usgs_path
	browser.visit(usgs_url)
	time.sleep(2)
	html = browser.html
	soup = bs(html, 'html.parser')

	# Initialize list of hemispheres
	hemisphere_image_urls = []

	# Find the images
	results = soup.find('div', class_='collapsible results').find_all('div', class_='item')

	for result in results:
		
		# Jump to image page
		link_text = result.find('div', class_='description').a.h3.text
		browser.click_link_by_partial_text(link_text)
		time.sleep(1)
		
		# Pull the image url
		html = browser.html
		soup = bs(html, 'html.parser')
		img_path = soup.find('img', class_='wide-image')['src']
		pic_dict = {}
		pic_dict["title"] = re.compile('Enhanced').sub('', link_text).rstrip()
		pic_dict["img_url"] = usgs_domain + img_path
		hemisphere_image_urls.append(pic_dict)
		
		# Jump back to main page
		browser.back()
		time.sleep(1)
		
	mtm_data['hemisphere_image_urls'] = hemisphere_image_urls
	return(mtm_data)

