import requests
import re

url = 'https://issues.apache.org/jira/browse/CAMEL-10597'
response = requests.get(url)
comments = []
for match in re.finditer('twixi-wrap verbose actionContainer.*twixi-wrap concise actionContainer', response.text):
    comments.append(match.group(0))
comments = comments[0].split('twixi-wrap verbose actionContainer')
print(comments[1])
print(comments[2])
print(comments[3])
print(re.findall(' \w* added a comment'+'', comments[4].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '')))
print(comments[5].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', ''))
print(re.findall('\\\\\\\\ \w.* added a comment '+'', comments[5].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', '')))
name_tmp = re.findall('\\\\\\\\ \w.* added a comment '+'', comments[5].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', ''))[0].split(' ')
name = []
for i in name_tmp[1:]:
    if i == 'added':
        break
    name.append(' ' + i)
print(''.join(name))


print(comments[1].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', ''))
print(re.findall('\\\\\\\\ \w.* added a comment '+'', comments[1].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', '')))
name_tmp = re.findall('\\\\\\\\ \w.* added a comment '+'', comments[1].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', ''))[0].split(' ')
name = []
for i in name_tmp[1:]:
    if i == 'added':
        break
    name.append(' ' + i)
print(''.join(name))
comments = []
comments_xml = []
for match in re.finditer('twixi-wrap verbose actionContainer.*twixi-wrap concise actionContainer', response.text):
    comments_xml.append(match.group(0))

if len(comments_xml) > 0:
    comments_xml = comments_xml[0].split('twixi-wrap verbose actionContainer')
    # extract every single comment
    count = 1
    for i in comments_xml[1:]:
        # parse the comment and extract the name
        name_tmp = re.findall('\\\\\\\\ \w.* added a comment ' + '',comments_xml[count].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', ''))[0].split(' ')
        print(name_tmp)
        name = []
        count += 1
        for j in name_tmp[1:]:
            if j == 'added':
                break
            name.append(' ' + j)
        comment_single = ''
        real_name = ''.join(name)
        comment_single = comment_single + real_name + ':'
        comments.append(comment_single)

print(''.join(comments))