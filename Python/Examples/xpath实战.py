'''
Author: hugepower
Date: 2021-02-10 04:48:20
LastEditors: hugepower
LastEditTime: 2021-02-17 21:10:21
Description: file content
'''

import requests
from lxml import etree

s = requests.Session()
s.headers = {
    "User-Agent":
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

def xclient_response(func, url):
	res = func.get(url=url)
	if res.status_code == 200:
		return res.text

def main():
	html1 = etree.HTML(xclient_response(func=s, url="https://xclient.info/s/"))
	app_url = html1.xpath('//li[@class="col-6 col-4-m col-3-l col-2-xl"]/div/a/@href')
	app_title = html1.xpath('//li[@class="col-6 col-4-m col-3-l col-2-xl"]/div/a/@title')
	print(app_title)
	print(app_url)
	for item in app_url:
		html2 = etree.HTML(xclient_response(func=s, url=item))
		version_num = html2.xpath('//*[@id="versions"]/table/tbody/tr[1]/td[1]/text()')
		update_time = html2.xpath('//*[@id="versions"]/table/tbody/tr[1]/td[3]/text()')
		url1 = html2.xpath('//*[@id="versions"]/table/tbody/tr[1]/td[5]/a[1]/@href')
		if len(url1) > 0:
			print(version_num,update_time,url1[0])

if __name__ == "__main__":
	main()