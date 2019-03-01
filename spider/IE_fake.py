#conding=utf8
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

