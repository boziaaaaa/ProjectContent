#coding=utf8
import requests
from bs4 import BeautifulSoup

url = "https://item.btime.com/f3dhfqbdqur8vnpchs0roni2slk?from=haoz1t1p1"
tmp = requests.get(url).text
soup = BeautifulSoup(tmp, 'html.parser')
r = soup.find_all("div")
a = (x.get_text() for x in r)
# print a
for lines in a:
    # print lines
    print lines.encode("utf8")

