import urllib
import urllib2
import re
import thread
import time
import codecs

class QSBK:
    def __init__(self):
        self.page = 1
        self.user_agent = 'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)'
        self.headers={'User-Agent':self.user_agent}
        self.stories = []
        self.enable = False
        self.file = None
    def GetPage(self,page):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(page)
            request = urllib2.Request(url,headers = self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            return content
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"link error",e.reason
                return None
    def GetPageItems(self,page):
        content=self.GetPage(page)
        if not content:#################################
             print "loading fail...."
             return None
        pattern = re.compile('<div class="content">(.*?)</div>.*?<div class="stats">.*?</div>',re.S)
        items = re.findall(pattern,content)
        pageStory = []
        for item in items:
            pageStory.append(item)
        return pageStory
    # def loadPage(self):
    #     if self.enable == True:
    #         if len(self.stories) < 2:
    #             pageStories = self.GetPageItems(self.page)
    def getOneStory(self,pageStories):
        for story in pageStories:

            # self.GetPageItems()
            print u"ooooooo%soooooooo"%(story)
            # input = raw_input()
            # if input == "Q":
            #     self.enable = False
            #     returnfi'u'u'u'y'y


    # def setFileTitle(self,title):
    #     __defaultTitle = 'a'
    #      if title is not None:
    #         self.file = open(title + ".txt","w+")
    #     else:
    #         self.file=open(self.__defaultTitle + ".txt","w+")
    __title = None
    def writeData(self,contents):
       self.__title = str(time.time())
       self.file =codecs.open('D:\DD\_'+self.__title+'.txt','w+','utf-16')
       for item in contents:
            self.file.write(item)
            self.file.write("\r")
            self.file.write("\r")
       self.file.close()


    def start(self):
        __joke=None
        self.enable = True
        self.__joke=self.GetPageItems(1)
        #self.writeData(self.__joke)
        self.getOneStory(self.__joke)
run = QSBK()
run.start()
