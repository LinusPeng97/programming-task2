# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from model.items import ModelItem
import datetime
import re


class ModelinfoSpider(scrapy.Spider):

    name = 'issueInfo'
    allowed_domains = ['apache.org']
    start_urls = ['https://issues.apache.org/jira/projects/CAMEL/issues?startIndex=0']


    def parse_href(self, href):
        """
        rule out all redundant information and extract real href
        :param href:    e.g.a href="https:\\github.com\bobpaulin\camel" class="external-link" rel="nofollow"https:\\github.com\bobpaulin\camel\a
        :return: real_href    e.g.https:\\github.com\bobpaulin\camel
        """
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

    def parse_item(self, response):
            item = ModelItem()

            item['Type'] = response.xpath('//span[@id="type-val"]/text()').extract()[1].replace(' ', '').replace('\n', '')

            item['Assignee'] = response.xpath("//html/body/div[1]/section/div[2]/div/div/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/ul[1]/li/dl[1]/dd/span/text()").extract()[1].replace(' ', '').replace('\n', '')

            Created = response.xpath("//html/body/div[1]/section/div[2]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[2]/ul/li/dl[1]/dd/span/time/@datetime").extract()
            item['Created'] = Created
            # translate the original format to python format
            utc_former = Created[0][0:22]
            utc_timezone = Created[0][22:24]
            item['Created_Epoch'] = datetime.datetime.strptime(utc_former + ':' + utc_timezone, "%Y-%m-%dT%H:%M:%S%z").timestamp()

            description = []
            description_tmp = []
            text_tmp = []
            href_tmp = []
            for p in response.xpath('//html/body/div[1]/section/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div'):
                text_tmp = p.xpath('p/text()').extract()
                href_tmp = p.xpath('p/a/text()').extract()
                description_tmp = text_tmp + href_tmp
                description = description + description_tmp
            item['Description'] = ''.join(description).replace('\xa0', '')

            comments = []
            comments_xml = []
            # the comment is in the middle of <script>twixi-wrap verbose actionContainer ********  twixi-wrap concise actionContainer</script>
            for match in re.finditer('twixi-wrap verbose actionContainer.*twixi-wrap concise actionContainer', response.text):
                comments_xml.append(match.group(0))

            # len(comments_xml) == 0 means no comment
            if len(comments_xml) > 0:
                comments_xml = comments_xml[0].split('twixi-wrap verbose actionContainer')
                count = 1
                # process every single comment
                for i in comments_xml[1:]:
                    # rule out some redundant labels
                    comments_concise = comments_xml[count].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('\\\\/a\\', '').replace('\\\\/', '')
                    # parse the comment and extract the name   e.g. ASF GitHub Bot added a comment
                    name_tmp = re.findall('\\\\\\\\ \w.* added a comment ' + '', comments_concise)[0].split(' ')
                    name = []
                    for j in name_tmp[1:]:
                        if j == 'added':
                            break
                        name.append(' ' + j)
                    comment_single = ''
                    real_name = ''.join(name)
                    comment_single = comment_single + real_name + ':'

                    # parse the comment and extract the timestamp    e.g.datetime=2016-12-14T14:55:56+0000
                    timestamp_xml = re.findall('datetime=.{26}', comments_concise)[0]
                    datetime_utc = timestamp_xml[11:33] + ':' + timestamp_xml[33:35]
                    timestamp = datetime.datetime.strptime(datetime_utc, "%Y-%m-%dT%H:%M:%S%z").timestamp()
                    comment_single = comment_single + str(timestamp) + ':'

                    # parse the comment and extract the datetime    e.g.14Dec16 14:55time
                    datetime_xml = re.findall('title.{18}time class', comments_concise)[0][8:21]
                    comment_single = comment_single + datetime_xml[0:2] + '/' + datetime_xml[2:5] + '/' + datetime_xml[5:13] + ':'

                    # parse the comment and extract the content, which is the most difficult procedure in the process of comments.
                    # Step 1: extract the content and rule out some redundant labels
                    comment_content_step1_tmp = comments_xml[count].replace('\\u003e', '').replace('\\u003c', '').replace('\\n', '').replace('/span', '').replace('p\\\\p', '').replace('\\\\\\', '').replace('\\\\/', '').replace('\\\'', '').split('Expand comment')[0]
                    comment_content_step1 = re.findall('action-body flooded\".*twixi-wrap concise actionContainer', comment_content_step1_tmp)[0][21:][:-63]
                    # Step 2: some comments have href, so we need to parse them   e.g. a href="https:issues.apache.orgjirasecureViewProfile.jspa?name=davsclaus" class="user-hover" rel="davsclaus"Claus Ibsena
                    comments1_step2 = re.findall(r'a href=.*?class=.*?\\a[\\ ]', comment_content_step1)
                    for i in range(len(comments1_step2)):
                        comment_content_step1 = comment_content_step1.replace(comments1_step2[i], ' ' + self.parse_href(comments1_step2[i]) + ' ')
                    comment_single = comment_single + '"' + comment_content_step1.replace('\   ', '') + '"'

                    count += 1
                    comments.append(comment_single)

            item['Comments'] = ''.join(comments)


            yield item

    def parse_url(self, response):
        for match in re.finditer('CAMEL-\d{2,7}', response.text):
            yield Request('https://issues.apache.org/jira/browse/' + match.group(0), self.parse_item)

    def parse(self, response):
        url = 'https://issues.apache.org/jira/projects/CAMEL/issues?startIndex=0'
        yield Request(url, self.parse_url)
