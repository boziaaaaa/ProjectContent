#conding=utf8
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
def ClickBaidu():
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36')
    html = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",options=options)
    html.get('http://www.baidu.com')
    print(html.title)
    elem = html.find_element_by_id('kw')
    elem.send_keys("python")
    elem.send_keys(Keys.RETURN)
    time.sleep(2)
    elem = html.find_element_by_xpath("//strong//a[@href]").send_keys(Keys.ENTER)

def ClickBaidu2():
    html = webdriver.Chrome(r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    html.get('https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html')
    page = html.page_source
    return page

def getText(page):
    import requests
    req = requests.get("https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html")
    req.encoding="gb2312"
    # page = req.text
    soup = BeautifulSoup(page,'html.parser')
    text = soup.find_all("div",id="doc",class_="page")
    # text = text[0].find_all("div",id="bd")
    # text = text[0].find_all("div",class_="bd")
    text = text[0].find_all("div",class_="ie-fix")

    print(len(text))
    for each in text:
        print(each.name)
        print(each.attrs)
        print(each.text)


if __name__=="__main__":
    page = ClickBaidu2() #open url via webdriver is important!!! otherwise may lose content
    getText(page)