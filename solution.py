import csv
import requests
import xml.etree.ElementTree as ET

def get_data_from_xml(self, input_xml):
        tree = ET.fromstring(input_xml)
        # Enter your code here.
        #   Sample code has been provided as an example, but please restructure/rewrite/replace it as
        #   necessary to create a complete, elegant, and maintainable solution that passes the test cases.

        result = {
            'name': tree.findall(r'Name')[0].text,
            'strategies': [],
        }
        for element in tree.findall(r'TradingStrategies/TradingStrategy'):
            result['strategies'].append({
                'enabled': element.attrib['enabled'],
                # 'symbols': element.attrib['symbol']
            })
            #for element in tree.findall('Multiplier'):
                # result['strategies'].append({
                #     'multiplier': element.attrib['Multiplier'],
                #})
                #multi = multiplier.find(Multiplier, result)
        return result

def main():
    # load rss from web to update existing xml file
    loadRSS()
  
    # parse xml file
    newsitems = parseXML('topnewsfeed.xml')
  
    # store news items in a csv file
    savetoCSV(newsitems, 'topnews.csv')
      
      
if __name__ == "__main__":
  
    # calling main function
    main()

