# coding=utf-8
import requests
from bs4 import BeautifulSoup
import html5lib
import urllib
class tianya(object):
    def __init__(self,url):
        self.url = url
        self.page = requests.get(url)
        self.html = self.page.text
        self.containt = []
        self.getText_temp()
    # def getText(self):
    #     soup = BeautifulSoup(self.html, 'html.parser')
    #     author_info = soup.find_all('div', class_='atl-info')
    #     listauthor = [x.get_text() for x in author_info]
    #     list_info = soup.find_all('div', class_='bbs-content')
    #     listtext = [x.get_text() for x in list_info]
    #     for x in range(len(listauthor)):
    #         listauthor[x] = listauthor[x].encode("utf-8")
    #         if "主" in listauthor[x]:
    #             self.containt.append(listtext[x].strip())
    # def getText_temp2(self):
    #     soup = BeautifulSoup(self.html, 'html.parser')
    #     author_info = soup.find_all('div', class_='atl-info')
    #     list_info =   soup.find_all('div', class_='bbs-content')
    #     author_list = [x.get_text() for x in author_info]
    #     contain_list = [x.get_text() for x in list_info]
    #     for i in range(len(author_list)):
    #         if "主" in author_list[i].encode("utf-8"):
    #             contain = contain_list[i].encode("utf-8")
    #             print contain.strip()
    #             print "-----------------------"








    def getText_temp(self):
        # soup = BeautifulSoup(self.html, 'html.parser')
        soup = BeautifulSoup(self.html, 'html5lib')
        soup = soup.body
        # r = soup.find_all("div",class_="container")
        r = soup.find_all("div",class_="article-content")
        print list(r)
        a = (x.get_text() for x in r)
        print a
        for i in a:
            print i.encode("utf8")
        # for i in r:
        #     url_jpg = self.url+ i["src"]
        #
        #     print url_jpg
        #     urllib.urlretrieve(url_jpg,"a.jpg")

if __name__ == '__main__':

    url = "http://baijiahao.baidu.com/s?id=1583829444941903211&wfr=spider&for=pc"
    html = tianya(url)
