from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

from requests import get
from requests.exceptions import RequestException
from contextlib import closing


# launch url
url = "http://kanview.ks.gov/PayRates/PayRates_Agency.aspx"

# create a new Firefox session
driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get(url)

python_button = driver.find_element_by_id('MainContent_uxLevel1_Agencies_uxAgencyBtn_33') #FHSU
python_button.click() #click fhsu link

#Selenium hands the page source to Beautiful Soup
soup_level1=BeautifulSoup(driver.page_source, 'lxml')

datalist = [] #empty list
x = 0 #counter

    #Beautiful Soup grabs all Job Title links
for link in soup_level1.find_all('a', id=re.compile("^MainContent_uxLevel2_JobTitles_uxJobTitleBtn_")):
    
    #Selenium visits each Job Title page
    python_button = driver.find_element_by_id('MainContent_uxLevel2_JobTitles_uxJobTitleBtn_' + str(x))
    python_button.click() #click link
    
    #Selenium hands of the source of the specific job page to Beautiful Soup
    soup_level2=BeautifulSoup(driver.page_source, 'lxml')

    #Beautiful Soup grabs the HTML table on the page
    table = soup_level2.find_all('table')[0]
    
    #Giving the HTML table to pandas to put in a dataframe object
    df = pd.read_html(str(table),header=0)
    
    #Store the dataframe in a list
    datalist.append(df[0])
    
    #Ask Selenium to click the back button
    driver.execute_script("window.history.go(-1)") 
    
    #increment the counter variable before starting the loop over
    x += 1



'''
def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


salvato = simple_get('http://ww2.lagenziadiviaggi.it/annuario/elenco.php?res_start=20&')

html = BeautifulSoup(salvato, 'html.parser')
print (html)
'''
