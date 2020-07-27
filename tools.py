#!/usr/bin/python3
def headers_parser(headers_string):
	headers_split=headers_string.split('\n')
	headers={}
	for header in headers_split:
		headers[header.split(': ')[0]]=header.split(': ')[1]
	return headers
