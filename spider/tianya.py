# coding=utf-8
import requests
from bs4 import BeautifulSoup


def getHtml(url):
    page = requests.get(url)
    html = page.text
    return html


def getText(html):
    soup = BeautifulSoup(html, 'html.parser')

    author_info = soup.find_all('div', class_='atl-info')
    listauthor = [x.get_text() for x in author_info]

    list_info = soup.find_all('div', class_='bbs-content')
    listtext = [x.get_text() for x in list_info]

    global i
    if i > 1:
        listtext = [""] + listtext

    for x in range(len(listauthor)):
        listauthor[x] = listauthor[x].encode("utf-8")
        if "主" in listauthor[x]:
             print (listtext[x].strip())
             input("enter:")

if __name__ == '__main__':
    for i in range(1, 6):
        url = ("http://bbs.tianya.cn/post-no05-463610-1.shtml")

        html = getHtml(url)
        getText(html)


