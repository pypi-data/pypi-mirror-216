from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from WeatherApp_DataExtraction import HTMLfetcher, HTMLparser

from PyQt5.QtWidgets import QApplication
import sys
        
class Window(QMainWindow):
    def __init__(self, app):
        super().__init__()
    
        self.inapp = app
        self.url = "http://agromet.mkgp.gov.si/APP2/sl/Home/Index?id=2&archive=0&graphs=1#esri_map_iframe"
        self.WeatherData = self.getData()
        title = "WeatherApp"

        self.setWindowTitle(title)
        self.setGeometry(0, 0, 1800, 920)
        self.MyUI()
        
    def getData(self):  
        ## create response from main page
        fetchURL = HTMLfetcher(self.url)
        createdResponse = fetchURL.createResponse()
        
        ## get all xml files on the main webpage
        ParseWebpage = HTMLparser(createdResponse)
        xmls = ParseWebpage.getXMLfiles()
        
        data_in_city = []
        for i in range(len(xmls)):
        #% create response from xml files/website
            fetchURL_xml = HTMLfetcher(xmls[i])
            createdResponse_xml = fetchURL_xml.createResponse()
            ## parse xml files
            ParseWebpage_xml = HTMLparser(createdResponse_xml)
            data_in_city.append(ParseWebpage_xml.getData_fromXML())
        return data_in_city  
    
    #Function is used becaused kernel/console did not end. app.exec_() in endless loop.
    def closeEvent(self, event):
        self.inapp.quit()
        
    def MyUI(self):      
        canvas = Canvas(self, 17, 10, 100, self.WeatherData)
        canvas.move(0,0)
        button = QPushButton("Refresh Data", self)
        # setting geometry of button
        button.setGeometry(100, 800, 200, 50)
  
        # adding action to a button
        button.clicked.connect(self.refreshButton)
        
        # self.label = QLabel(self)
        # self.label.move(300, 850)
        # self.label.setText("<--Refresh.")
        
    def refreshButton(self):
        print("Refreshing")
        # self.label.clear()
        # self.label.setText("Refreshing!")   
        self.WeatherData = self.getData()
        self.MyUI()
        print("Data refreshed")
        # self.label.setText("<--Press the button to refresh data.")
        
        
class Canvas(FigureCanvas):
    def __init__ (self, parent = None, width=5, height=5, dpi=100, WeatherData= 0):
        fig = Figure(figsize=(width, height), dpi = dpi)

        self.axes = []
        self.noPlaces = 6
        for n in range(self.noPlaces):
            self.axes.append(fig.add_subplot(3,3,n+1)) 
            self.axes[n].title.set_text(WeatherData[n][0][0])

            #Plot Av. temp
            if(len(WeatherData[n][1])>0):
                # print(WeatherData[n][1])
                # print('\n')
                # print(WeatherData[n][2])
                # print("n is: ", n)
                # print('\n')
                
                self.axes[n].plot(WeatherData[n][1], WeatherData[n][2], '*', c='r', label="T[°C]")
                self.axes[n].set_ylabel('T[°C], RH[%], WS[m/s]')
                self.axes[n].set_xlabel('Month-Day Hour')
                self.axes[n].legend(loc='upper right')
            
            #Plot RH
            if (len(WeatherData[n][3]) == 192):
                self.axes[n].plot(WeatherData[n][1], WeatherData[n][3][::2], '*', c='g', label="RH[%]")
                self.axes[n].legend(loc='upper right')
            elif(len(WeatherData[n][3])>0):
                self.axes[n].plot(WeatherData[n][1], WeatherData[n][3], '*', c='g', label="RH[%]") # Rh in some places has two information number(second is RH on 20cm height) -> first one is relevant
                self.axes[n].legend(loc='upper right')
            #Plot Wind speed                   
            if (len(WeatherData[n][4]) == 192):
                self.axes[n].plot(WeatherData[n][1], WeatherData[n][4][::2], '*', c='b', label="WS[m/s]")
                self.axes[n].legend(loc='upper right')
            elif(len(WeatherData[n][4])>0):
                self.axes[n].plot(WeatherData[n][1], WeatherData[n][4], '*', c='b', label="WS[m/s]")
                self.axes[n].legend(loc='upper right')
            
            plt.setp(self.axes[n].get_xticklabels(), rotation=45, ha="right")
               
        fig.tight_layout()
        
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)  