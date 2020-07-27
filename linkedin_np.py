#!/usr/bin/python3

	### --- When pasting the requests headers make sure you delet the Accept-Encoding headers.
	### --- Also, make sure there isn't more than one space under user agent (for e.g. User-Agent:  Mozilla/5.0 --> User-Agent: Mozilla/5.0).
	### --- Notice the example above (from left to right) two spcaes and one space.


						# GOOD HUNTING #
import requests
from tools import headers_parser
import json


class Linkedin:

	# Receiving the headers, url and params from the scrape function.
	def __init__(self, headers, url, params):
		self.url = url
		self.headers = headers
		self.params = params
		self.names = {}
		self.names_next = {}
		self.urn = ' '

	# Performing a GET request and returning a text to work with.
	def search(self):
		res = requests.get(url=self.url, headers = headers_parser(self.headers), params = self.params)
		return res.text

	# Working with the information in the JSON.
	def filtersearch(self):
		t = self.search()
		parsed = json.loads(t)
		elements = parsed['data']['elements']
		cnt = 0
		options = {}

	# Filtering results for a company.
		for x in elements:
			if x['type'] == 'COMPANY':
				print(x['text']['text'])
				options[x['text']['text'].lower()] = cnt
			cnt += 1
		for key, value in options.items() :
			print(key.strip("'"),f"--> option number: {value}")
#		print(options.keys())

	# Incase the string of the campany's name appears in more than one orginization, a choice can be made.
		if len(options) == 1:

			i = list(options.values())
#			print(i)
			company_conf = i[0]

		else:
			while True:
				c = input('please choose a company by an option number: ')
				if c in options:
					break
					company_conf = options[c]

	# Finding the capmnies uniqe number
		self.urn = elements[company_conf]['targetUrn'].split(':')[3]
#		print(f"This Company's Number is {self.urn}")
		return self.urn


	# Extracting the employee names and titles
	def new_name(self):
		self.headers = ''''''

		self.url = f'https://www.linkedin.com/voyager/api/search/blended?count=10&filters=List(currentCompany-%3E{self.urn},resultType-%3EPEOPLE)&origin=OTHER&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue)&start=0'
		res1 = requests.get(url = self.url, headers = headers_parser(self.headers))
		json_pep = json.loads(res1.text)
		element = json_pep['data']['elements'][1]['elements']
		flnames = []
		titles = []
		for x in element:
			if x['type'] == 'PROFILE':
				flnames = x['title']['text']
				titles = x['headline']['text']
				self.names[flnames] = titles
		for key, value in self.names.items():
			print(f'Name: {key} ------ Title: {value}')
		return self.names

	## Scraping names throughout the next page and beyond

	def next_page(self):
		self.headers = ''''''

		page = 0

		while True:
			headers_next= self.headers
			page += 10
			self.url = f'https://www.linkedin.com/voyager/api/search/blended?count=10&filters=List(currentCompany-%3E{self.urn},resultType-%3EPEOPLE)&origin=OTHER&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue)&start={page}'
			res2 = requests.get(url = self.url, headers = headers_parser(headers_next))
			if res2.status_code == 200:
				json_pep_next = json.loads(res2.text)
				element_next = json_pep_next['data']['elements'][0]['elements']
#				if element_next == True:
#					pass
#				else:
#					element_next = json_pep_next['data']['elements'][0]['elements']
				flnames_next = []
				titles_next = []
				for x in element_next:
					if x['type'] == 'PROFILE':
						flnames_next = x['title']['text']
						titles_next = x['headline']['text']
						self.names_next[flnames_next] = titles_next
					for key, value in self.names_next.items():
						print(f'Name: {key} ------ Title: {value}')
			else:
				print('\nThese are all of them')
				break


def scrape():
	return ''''''

def link_main():
	company = input("please enter a companiy's name (specific as possible for e.g.: intel corporation, western digital etc.): ")
	params = {
        'keywords': company,
        'origin': 'GLOBAL_SEARCH_HEADER',
        'q': 'blended',
        }

	link = Linkedin(scrape(),'https://www.linkedin.com/voyager/api/typeahead/hitsV2', params)
	link.filtersearch()
	link.new_name()
	link.next_page()
link_main()
