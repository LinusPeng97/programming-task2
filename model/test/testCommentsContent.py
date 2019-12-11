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
# print(comments[6])replace('\\\\/a\\', '')
comments1_tmp = comments[1].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('p\\\\p', '').replace('\\/', '').replace('\\\\\\', '').replace('\\\'', '').split('Expand comment')[0]
# print(comments1_tmp)
print(re.findall('action-body flooded\".*twixi-wrap concise actionContainer', comments1_tmp)[0][21:][:-63])

comments2_tmp = comments[3].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('p\\\\p', '').replace('\\\\\\', '').replace('\\\\/', '').replace('\\\'', '').split('Expand comment')[0]
# print(comments2_tmp)
print(re.findall('action-body flooded\".*twixi-wrap concise actionContainer', comments2_tmp)[0][21:][:-63])

# print(comments[4].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('p\\\\p', '').replace('\\\\\\', '').replace('\\\\/', '').replace('\\\'', '').split('Expand comment')[0])

comments5_tmp = comments[5].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('p\\\\p', '').replace('\\\\\\', '').replace('\\\\/', '').replace('\\\'', '').split('Expand comment')[0]
# print(comments5_tmp)
print(re.findall('action-body flooded\".*twixi-wrap concise actionContainer', comments5_tmp)[0][21:][:-63])