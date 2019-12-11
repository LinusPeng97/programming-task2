import requests
import re
import datetime

url = 'https://issues.apache.org/jira/browse/CAMEL-13188'
response = requests.get(url)