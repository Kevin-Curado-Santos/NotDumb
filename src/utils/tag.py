import requests
import json
from bs4 import BeautifulSoup

url = "https://codeforces.com/problemset#"
resp = requests.get(url)
html_cnt = resp.text

soup = BeautifulSoup(html_cnt, 'html.parser')

div = soup.find('div', class_='_FilterByTagsFrame_addTag smaller')

l = div.findChildren('option')

with open('tag.txt', 'a') as f:
    for e in l[2:]:
        f.write(e.text + '\n')
