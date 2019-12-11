import requests
import re
import datetime

url = 'https://issues.apache.org/jira/browse/CAMEL-14280'
response = requests.get(url)

for p in response.xpath(
        '//html/body/div[1]/section/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div'):
    text_tmp = p.xpath('p/text()').extract()
    print(text_tmp)
    href_tmp = p.xpath('p/a/text()').extract()
    print(href_tmp)
    description_tmp = text_tmp + href_tmp
    description = description + description_tmp
print(description)