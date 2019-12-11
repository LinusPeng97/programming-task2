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
print(comments[6].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', '').replace('\\\'', ''))
datetime_xml = re.findall('datetime=.{26}', comments[1].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', ''))[0]
print(datetime_xml)
datetime_utc = datetime_xml[11:33] + ':' + datetime_xml[33:35]
timestamp = datetime.datetime.strptime(datetime_utc, "%Y-%m-%dT%H:%M:%S%z").timestamp()
print(timestamp)