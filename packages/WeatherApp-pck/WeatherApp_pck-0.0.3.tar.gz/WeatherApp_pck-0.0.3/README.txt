README
Weather App repository contains three python code files, which purpose are to fetch data from agromet web page,
extract temperature, humidity and wind speed of different cities and plot them in a GUI with a refresh button included  
The last, 4th file is intendend for unit testing.

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

DEPENDENCIES
Before running the programm please install all necessary dependencies with pip install: lxml, bs4, requests, datetime, PyQt5, matplotlib, setuptools, wheel, twine.

CODE SEPARATION
Code is separated in a main folder "WeatherApp_main" with an objective to call "WeatherAppGUI" where all necessary plotting widgets are included in a GUI, and a call to functions in
"WeatherApp_DataExtraction" is being made in order to obtain all of the web scrapping funcionality. The last, 4th file is intendend for unit testing.

WEATHERAPP_MAIN
This is the main folder of an application. It is intended to create Qapplication and call Weather app Gui window which starts the programms interface to run. 

WEATHERAPPGUI 
This part of the program functions for the GUI window initialization using PyQt5 and matplotlib libraries and plotting weather data obtained from an agromet website for the last 48h. 

Window class creates a window with necessary number of plots included, it represents the main window and is responsible for data retrieval with a function getData which calls 
HTMLfetcher and HTMLparser classes in Weatherapp_DataExtraction module, specialized for XML doc type. Plots are performed with a call to MyUI function which prepares
environment for all neccessary subplots with a Canvas class. 

Program also contains a refresh button for the ability of updating weather data.

WEATHERAPP_DATAEXTRACTION
Purpose of this part of the program is to extract all necessary data from agromet webpage.

It is divided in two classes called HTMLfetcher and HTMLparser.

HTMLfetcher generates a request to agromet webpage and cretes a response, which is than passed to HTMLparser. Function getXMLfiles gathers names of all of the available XML files on the webpage.
This file names are than passed to BeautifulSoupwhich creates BeautifulSoup class with parse tree for easier data manipulation. This class is than passed to getDate, getTXT_normal and getTXT functions 
which extract the weather data and write it in a corresponding class variables. 

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

TEST_WEATHERAPP_DATAEXTRACTION
In this file, tests for two main classes in WeatherApp_DataExtraction are written; test_getXMLfiles and test_getData_fromXML.

- - test_getXMLfiles
checks if all gathered xml files are in the right format 

- - test_getData_fromXML
Checks if all extracted data is of the right type and correct length

