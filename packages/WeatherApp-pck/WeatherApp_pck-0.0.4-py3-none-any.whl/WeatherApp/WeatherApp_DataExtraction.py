import lxml
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# class HTMLfetcher intended to fetch a response from RS agromet web page.
class HTMLfetcher:
    def __init__(self, inURL:str):
        self.__URL = inURL

    def createResponse(self):
        self.__response = requests.get(self.__URL)
        if self.__response.status_code == 200:
            return self.__response
        else:
            print("Error: Failed to fetch the webpage")
                  
    @property #getter for URL(encapsulation)
    def URL(self):
        return self.__URL
    
    @property  #getter for response(encapsulation)
    def response(self):
        return self.__response

# class HTMLparser intended to get data from RS agromet web page. Input is a response generated from HTMLfetcher
class HTMLparser:
    def __init__(self, inResponse):
        self.__soupFeed = inResponse
        self.__domainTitle = []
        self.__TimeDate = []
        self.__avTemperature = []
        self.__avRelativeHumidity = []
        self.__avWindSpeed = []
        
    #Get all .xml (full)links (with main part of the URL: "http://agromet.mkgp.gov.si" + "/APP2/AgrometContent/xml/55.xml")
    def getXMLfiles(self):
        def findMainURL(self):
            return self.__soupFeed.url[self.__soupFeed.url.find('http'):self.__soupFeed.url.find('.si')+3]
       
        self.soup = BeautifulSoup(self.__soupFeed.content, features="html.parser")
        # print("Tole je URL: ", self.__soupFeed.url)
        self.xml = []
        for a in self.soup.findAll('td'):
            if(a.find('a')):
                if(a.find('a')['href'].find('.xml')>0):
                    # print(a.find('a')['href'])
                    self.xml.append(findMainURL(self) + a.find('a')['href'])
        return self.xml
                    
    def getData_fromXML(self):
        #Get the dates that have corresponding measurements (some of them are empty - without measurements)
        def getDate(self, inDate):
            txt = getTXT_normal(self, inDate)
            # print(txt)
            self.datetime = []
            for i in range(len(txt)-1):
                if(len(txt[i])>0 and txt[i][-3:] == 'CET'):
                    try:
                        eval(txt[i+1]) #if i+1 is a number, than it corresponds to timedate inDate[i].
                        self.datetime.append(txt[i])
                    except:
                        pass
            return self.datetime
        
        #extract text content from a txt within a tags 
        def getTXT_normal(self, inTxt):
            self.outTxt = []
            for param in inTxt:
                self.outTxt.append(param.get_text())
            return self.outTxt
        
        #extract text content from a txt within a tags 
        def getTXT(self, inTxt_):
          self.inTxt = getTXT_normal(self, inTxt_)
          self.outTxt = []
          for i in range(len(self.inTxt)-1):
              if(len(self.inTxt[i])>0 and self.inTxt[i][-3:] == 'CET'):
                  try:
                      self.outTxt.append(eval(self.inTxt[i+1]))
                      # datetime.append(domainTitle[i]) # we dont need date anymore as it is deriven from getDate function 
                  except:
                      pass
          return self.outTxt
                
        self.XMLsoup = BeautifulSoup(self.__soupFeed.content, features="lxml")
        
        self.__domainTitle = getTXT_normal(self.XMLsoup, self.XMLsoup.findAll('domain_title'))
        [self.__TimeDate.append(datetime.strptime(x[:-4], '%d.%m.%Y %H:%M')) for x in getDate(self.XMLsoup, self.XMLsoup.findAll(['valid', 'tavg']))] # to get correct number of dates - some are redundant
        # [self.__TimeDate.append(x[:-4]) for x in getTXT(self.XMLsoup, self.XMLsoup.findAll('valid'))]
        [self.__avTemperature.append(x) for x in getTXT(self.XMLsoup, self.XMLsoup.findAll(['valid', 'tavg']))]
        [self.__avRelativeHumidity.append(x) for x in getTXT(self.XMLsoup, self.XMLsoup.findAll(['valid', 'rhavg']))]
        [self.__avWindSpeed.append(x) for x in getTXT(self.XMLsoup, self.XMLsoup.findAll(['valid', 'ffavg']))]
        
        # print("Timedate length: ", len(self.__TimeDate))
        return [self.__domainTitle, self.__TimeDate, self.__avTemperature, self.__avRelativeHumidity, self.__avWindSpeed]
            
    @property  #getter for response(encapsulation)
    def soupFeed(self):
        return self.__soupFeed