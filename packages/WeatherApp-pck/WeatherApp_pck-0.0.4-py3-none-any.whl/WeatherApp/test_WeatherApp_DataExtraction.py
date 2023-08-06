from .WeatherApp_DataExtraction import HTMLfetcher, HTMLparser
import pytest

''' http://agromet.mkgp.gov.si/APP2/AgrometContent/xml/72.xml'''

# test to check xmls web-links 
def test_getXMLfiles():
    #right webpage test
    url = "http://agromet.mkgp.gov.si/APP2/sl/Home/Index?id=2&archive=0&graphs=1#esri_map_iframe"
    # url = "https://en.wikipedia.org/wiki/Banksia_grossa"
    fetchURL = HTMLfetcher(url)
    createdResponse = fetchURL.createResponse()
    ## get all xml files on the main webpage
    ParseWebpage = HTMLparser(createdResponse)
    xmls = ParseWebpage.getXMLfiles()
    for i in xmls:
        if(len(i)>51):
            assert i[0:51] =='http://agromet.mkgp.gov.si/APP2/AgrometContent/xml/', "xml web-links are not in right format"
            assert i[-4:] =='.xml', "xml web-links are not in right format"
        elif(len(i)<51):
            assert len(i) < 51, "xml web-links are not in right format"
    assert len(xmls)!=0, "xml web-links are not in right format"
    
    #wrong web page test
    # url = "https://en.wikipedia.org/wiki/Banksia_grossa"
    # fetchURL = HTMLfetcher(url)
    # createdResponse = fetchURL.createResponse()
    # ## get all xml files on the main webpage
    # ParseWebpage = HTMLparser(createdResponse)
    # xmls = ParseWebpage.getXMLfiles()
    # for i in xmls:
    #     if(len(i)>51):
    #         assert i[0:51] =='http://agromet.mkgp.gov.si/APP2/AgrometContent/xml/', "xml web-links are not in right format"
    #         assert i[-4:] =='.xml', "xml web-links are not in right format"
    #     elif(len(i)<51):
    #         assert len(i) < 51, "xml web-links are not in right format"
    # assert len(xmls)!=0, "xml web-links are not in right format: " + url
       
# test_getXMLfiles()

#% Test to check data extraction
@pytest.mark.parametrize("inUrl", [
    ("http://agromet.mkgp.gov.si/APP2/sl/Home/Index?id=2&archive=0&graphs=1#esri_map_iframe")
    # ("https://en.wikipedia.org/wiki/Banksia_grossa"),
])

 
def test_getData_fromXML(inUrl):
    url = inUrl#"http://agromet.mkgp.gov.si/APP2/sl/Home/Index?id=2&archive=0&graphs=1#esri_map_iframe"
    # url = "https://en.wikipedia.org/wiki/Banksia_grossa"
    fetchURL = HTMLfetcher(url)
    createdResponse = fetchURL.createResponse()
    ## get all xml files on the main webpage
    ParseWebpage = HTMLparser(createdResponse)
    xmls = ParseWebpage.getXMLfiles()
    
    places = []
    for i in range(len(xmls)):
        fetchURL_xml = HTMLfetcher(xmls[i])
        createdResponse_xml = fetchURL_xml.createResponse()
        ParseWebpage_xml = HTMLparser(createdResponse_xml)
        places.append(ParseWebpage_xml.getData_fromXML())
    
    from datetime import datetime
    
    if(len(places)>0):
        for i in range(len(places[i])):
            #check if all values are correct type
            if(len(places[i][0])>0):  
                assert isinstance(places[i][0][0], str)
            if(len(places[i][1])>0): 
                #are all dates really dates
                noOfInstances = [isinstance(x, datetime) for x in places[i][1]]
                assert len(noOfInstances) == sum(noOfInstances)
            if(len(places[i][2])>0): 
                #are all temp. really temp.
                noOfInstances = [isinstance(x, float) for x in places[i][2]]
                assert len(noOfInstances) == sum(noOfInstances)    
            if(len(places[i][3])>0): 
                #are all rh really rh
                noOfInstances = [isinstance(x, float) for x in places[i][3]]
                assert len(noOfInstances) == sum(noOfInstances)   
            if(len(places[i][4])>0): 
                #are all wspeed really wspeed
                noOfInstances = [isinstance(x, float) for x in places[i][4]]
                assert len(noOfInstances) == sum(noOfInstances)   
        
            #Check the sizes of data
            if len(places[i][1]) > 0:          
                  assert ((len(places[i][1]) == len(places[i][2])) or len(places[i][2])==0), "Wrong length of data."
                  assert ((len(places[i][1]) == len(places[i][3])) or len(places[i][3])==0), "Wrong length of data."
                  assert ((len(places[i][1]) == len(places[i][4])) or len(places[i][4])==0), "Wrong length of data."
    assert not len(places)==0, "No xmls files to read."