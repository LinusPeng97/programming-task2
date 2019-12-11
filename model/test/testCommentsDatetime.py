import requests
import re
import datetime

url = 'https://issues.apache.org/jira/browse/CAMEL-10597'
response = requests.get(url)

comments = []
for match in re.finditer('twixi-wrap verbose actionContainer.*twixi-wrap concise actionContainer', response.text):
    comments.append(match.group(0))
comments = comments[0].split('twixi-wrap verbose actionContainer')
# print(comments[1])
# print(comments[2])
# print(comments[3])
# print(comments[4])
# print(comments[5])
# print(comments[6])
datetime_xml = ''
print(comments[1].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', '').replace('\\\'', ''))
datetime_xml = re.findall('title.{18}time class', comments[1].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', ''))[0][8:21]
datetime_format = datetime_xml[0:2] + '/' + datetime_xml[2:5] + '/' + datetime_xml[5:13]
print(datetime_format)