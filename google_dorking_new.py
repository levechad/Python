#!/bin/python3

# Auther: Lev-Echad Tsuella

# Description: this python script scrapes urls of pdf hyperlinks off of intel.com - this script for educational purposes only !

#Notes: you need to insert the headers inside of the varient 'self.headers' - line 27. the headers are from the search page on Google.com, use the values inside the 'query' varient - line 16.



import requests
import re
from bs4 import BeautifulSoup
from tools import headers_parser
import urllib.parse

domain = input("Enter A Domain:  ")
query = f"site:{domain} filetype:pdf"
# url_number = input(str("Insert A Number Of Links You Wish To Scrape: "))
class Google_Fu:

	def __init__(self):
		self.urls = []
		self.url = ''
		self.headers = ''
		self.params = ''
		self.emails_list = []

	def run_request(self):
		self.url = "https://www.google.com/search"
		self.headers = '''Host: www.google.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fsource%3Dhp%26ei%3DBLgeX4z8JsLzkwXKt4DoAw%26q%3Dsite%253Agoogle.com%2Bfiletype%253Apdf%26oq%3Dsite%253Agoogle.com%2Bfiletype%253Apdf%26gs_lcp%3DCgZwc3ktYWIQAzoICAAQsQMQgwE6BQgAELEDOgIIADoFCC4QsQM6BggAEAoQAToCCC46BAgAEApQvAVY8ldgn1toAHAAeACAAfYEiAGpMJIBDDAuMjIuMy4wLjEuM5gBAKABAaoBB2d3cy13aXo%26sclient%3Dpsy-ab%26ved%3D0ahUKEwiMjpPbp-3qAhXC-aQKHcobAD0Q4dUDCAY%26uact%3D5&q=EgRNi0KXGNuW-_gFIhkA8aeDS_hOcF4igCscobhujLdH8dJuoSL4MgFy
Connection: keep-alive
Cookie: NID=204=BWRiRcoB3IOBTeESX99gSt4bn9P98u2oT2a4TtAfB-b4jpD9tiEl6YyD1g68EAOm2o6zBUyhSk6BkzJNmgwcwlDcapMXQ53BSVp-Lw9p1iRynd3_l6XDpkj47ZIn3Hzd8sWdEkheYbIpJHsMmkiLisATZiaQS8mEbjdIBJFxrrs
Upgrade-Insecure-Requests: 1'''
		self.params = {
			"q": query,
			"oq": query,
			}
		res = requests.get(self.url, params=self.params, headers=headers_parser(self.headers))
		return res.text


	def url_scraping(self, htmlfile):
		html = htmlfile
		soup = BeautifulSoup(html, 'html.parser')
		# Scraping the "href"s , which in HTML are in the "<a" tags.
		for url in soup.select('div.g div.r > a:nth-of-type(1)'):
			self.urls.append(url['href'])

	def click_nextpage(self, html):
		# This function makes sure the next page is scraped incase the number of URLs isn't as requested - see line 71.
		# The informetion is transfered from "url_scrapin" into here via the "html" variable.
		soup = BeautifulSoup(html, 'html.parser')
		link = soup.select_one('#pnnext')
		link_split = str(link).split('href="')[1].split('"')
		str_link = urllib.parse.unquote(link_split[0])
		# Splitting the "/search? + the advanced operators for another scrape.
		url = f'https://www.google.com{str_link}'
		res = requests.get(url, params=self.params, headers=headers_parser(self.headers))
		scraped = res.text
		self.url_scraping(scraped)
		if len(self.urls) != 50:
			self.click_nextpage(scraped)
		else:
			print(*self.urls, sep = "\n")
			print('''###############################################################################
                          Winner Winner Chicken Dinner
###############################################################################''')


def main():
	GF = Google_Fu()
	print("""###############################################################################
				Good Hunting
###############################################################################""")
	GF.url_scraping(GF.run_request())
	GF.click_nextpage(GF.run_request())
main()


