import requests
import re
import datetime

url = 'https://issues.apache.org/jira/browse/CAMEL-8013'
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



def parse_href(href):
    # class_type_row      e.g.class="external-link"
    class_type_row = re.findall('class=".*?"', href)
    for i in range(len(class_type_row)):
        class_type = re.findall('".*?"', class_type_row[i])[0].replace('"', '')
        # return true url
        if 'external-link' == class_type:
            href = re.findall('href=".*?"', href)[0]
            return href.replace('"', '').replace('href=', '')
        # return special format
        elif 'issue-link' == class_type:
            href = re.findall('data-issue-key=".*?"', href)[0]
            return href.replace('"', '').replace('data-issue-key=', '')
        elif 'user-hover' == class_type:
            href = re.findall(r'rel=".*?".*\\a', href)[0]
            print(re.sub('rel=".*?"', '', href).replace('\\a', ''))
            return re.sub('rel=".*?"', '', href).replace('\\a', '')


comments1_tmp = comments[2].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('p\\\\p', '').replace('\\/', '').replace('\\\\\\', '').replace('\\\'', '').split('Expand comment')[0]
# print(comments1_tmp)
comments1_step1 = re.findall('action-body flooded\".*twixi-wrap concise actionContainer', comments1_tmp)[0][21:][:-63]
print(comments1_step1)
comments1_step2 = re.findall(r'a href=.*?class=.*?\\a[\\ ]', comments1_step1)
print(comments1_step2)
for i in range(len(comments1_step2)):
    comments1_step1 = comments1_step1.replace(comments1_step2[i], ' ' + parse_href(comments1_step2[i]) + ' ')
print(comments1_step1.replace('\   ', '').replace('.\\', '.').replace('\\\\\\\\', '\\\\').replace('\   ', '').replace('br\\\\', '').replace('\\u00A0\\', '').replace('\\u00A0', '').replace('u00A0', '').replace('\\tt', '').replace('\\ tt', '').replace('\\\\ulul', '').replace('\\\\ul', '').replace('\\li', '').replace('class="alternate" type="square"tli', '')[:-3])











# comments2_tmp = comments[3].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('p\\\\p', '').replace('\\\\\\', '').replace('\\\\/', '').replace('\\\'', '').split('Expand comment')[0]
# print(comments2_tmp)
# print(re.findall('action-body flooded\".*twixi-wrap concise actionContainer', comments2_tmp)[0][21:][:-63])

# print(comments[4].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('p\\\\p', '').replace('\\\\\\', '').replace('\\\\/', '').replace('\\\'', '').split('Expand comment')[0])

# comments5_tmp = comments[5].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('p\\\\p', '').replace('\\\\\\', '').replace('\\\\/', '').replace('\\\'', '').split('Expand comment')[0]
# print(comments5_tmp)
# print(re.findall('action-body flooded\".*twixi-wrap concise actionContainer', comments5_tmp)[0][21:][:-63])