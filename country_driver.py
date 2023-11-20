from main_update2 import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import string
import requests
import time 
import datetime
from duplicate_text_extractor_from_link import *
from selenium.webdriver.chrome.service import Service as ChromeService
from pdf_selector_update1 import *
import pytz
import csv
from googlesearch import search

def scrap_country(country_name):
    start_time=str(datetime.datetime.now()).split()[1]
    date=str(datetime.datetime.now()).split()[0]
    raw_links=[]
    user_response = "cyber security policy/strategy in "+country_name
    print("user_responce >>> ",user_response)
    for j in search(user_response, tld="co.in", num=10, stop=10, pause=2):     ########
        raw_links.append(j)    

    print(raw_links)

    filter1links,c_ex = filter1(raw_links,country_name)

    try:
        filter2links = filter_sublinks(filter1links,c_ex[0])
    except:
        print('index out of bound in filter 2')
        filter2links = filter_sublinks(filter1links,'')

    filter3links = filter3(filter2links)
    links = filter3links

    print("*************stage 2************8")

    for link in links:
        print("URL for policy ------------------>>>>>>> ",link)

        pdf_name_list = []
        pdf_from_sub_link = []

        path=country_name.replace(" ","_")
        name = str(link[8:]).replace("/","_")
        text_dir = f"{path}/{name}.txt"

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        driver = webdriver.Chrome(options=options,service= Service(ChromeDriverManager().install()))
        driver.minimize_window()
        driver.get(link)
        time.sleep(6)
        current_link = driver.current_url
        print("*************current link",link)

        if 'pdf' in current_link.lower():
            x = pdf_selector(link,path,country_name)
            print("x >>>",x)
            if x is not None:
                if '.pdf' in x.lower():
                    pdf_name_list.append(x)
                    driver.quit()
            else:
                pass
        else:
            print("***i am here***")
            list_=[] 
            lnk=driver.find_elements(By.XPATH, "//a[@href]")
            try:
                for i in lnk:
                    list_.append(str(i.get_attribute('href'))) 
            except:
                pass
            final_list = [link]+list_
            sublink_list = list(set(final_list))
            driver.quit()

            # print("raw_sublink >>> ",sublink_list)
            print("sublink list :",len(sublink_list))
            Filter_Sublinks = filter_sublinks(sublink_list,c_ex[0])
            u_filter_sublinks = filter3(Filter_Sublinks)
            https_filtersublinks = [sublink for sublink in u_filter_sublinks if 'https://' in sublink.lower()]

            print("sublinks after filter >>>>>>>>>>>>>>> ",https_filtersublinks)
            print("len of filter sublink :",len(https_filtersublinks))

            pdf_from_sub_link = create_text_for_each_link(text_dir,https_filtersublinks,path,country_name)

        pdf_for_link = pdf_name_list + pdf_from_sub_link

    return pdf_for_link

scrap_country('Belgium')