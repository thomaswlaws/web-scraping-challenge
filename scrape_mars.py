from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def render_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    r = driver.page_source
    return r

def scrape():
	browser = init_browser()
	scraped_data = {}
	url = "https://mars.nasa.gov/news/"
	response = render_page(url)
	browser.visit(url)
	time.sleep(3)
	soup = bs(response, 'html.parser')
	results = soup.find_all('div',class_="list_text")
	news_title = results[0].find('a').text
	scraped_data["news_title"] = news_title
	news_p = results[0].find('div', class_="article_teaser_body").text
	scraped_data["news_p"] = news_p

	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)
	browser.is_text_present('FULL IMAGE', wait_time=10)
	browser.click_link_by_partial_text('FULL IMAGE')
	browser.is_text_present('more info', wait_time=10)
	browser.click_link_by_partial_text('more info')
	browser.is_element_present_by_css('.lede', wait_time=10)
	browser.click_link_by_partial_href('.jpg')
	html = browser.html
	soup = bs(html, 'html.parser')
	featured_image_url = soup.find('img').get('src')
	scraped_data['featured_image_url'] = featured_image_url

	url = "https://twitter.com/marswxreport?lang=en"
	response = render_page(url)
	soup = bs(response, 'html.parser')
	mars_weather = soup.find('p',class_="tweet-text").text
	scraped_data["mars_weather"] = mars_weather

	url = 'http://space-facts.com/mars/'
	tables = pd.read_html(url)
	df = tables[0]
	df.columns = ['Description','Value']
	df.set_index('Description', inplace=True)
	df.head()
	html_table = df.to_html()
	scraped_data["tables"] = html_table.replace('\n', '')

	base_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(base_url)
	html = browser.html
	soup = bs(html, 'html.parser')
	hem_img_urls = []
	hem_dict = {'title': [], 'img_url': [],}
	titles = soup.find_all('h3')
	for t in titles:
		title = t.get_text()
		title_striped = title.strip('Enhanced')
		browser.click_link_by_partial_text(title)
		url = browser.find_link_by_partial_href('download')['href']
		hem_dict = {'title': title_striped, 'img_url': url}
		hem_img_urls.append(hem_dict)
		browser.visit(base_url)
		scraped_data["hemispheres"] = hem_img_urls

	return scraped_data