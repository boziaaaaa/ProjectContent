# -*- coding: UTF-8 -*-
from urllib import request
from bs4 import BeautifulSoup

if __name__=="__main__":
    html = "https://www.biqukan.com/1_1094/5403177.html"
    req = request.urlopen(html)
    conta = req.read()
    soup = BeautifulSoup(conta,"html.parser")
    # print(soup)
    ss = soup.find_all(div="content",class_="showtxt")
    print(ss)

