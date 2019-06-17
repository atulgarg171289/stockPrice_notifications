# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 22:20:25 2019

@author: Atul Garg
"""
#import libraries
import time
import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def news_popup(user_input,toaster,name2link):
    for company_name in user_input:
        page2company = requests.get(name2link[company_name],verify=False)
        page2company_soup = BeautifulSoup(page2company.content,'html.parser') 
        news = page2company_soup.find_all('div',{'class':'FL w308',})[0].find_all('a')[0]
        news_text = news.text
        #news_link = news['href']
        price = page2company_soup.find_all('div',{'id':'Bse_Prc_tick_div',})[0].text
        up_down = page2company_soup.find_all('div',{'id':'b_changetext',})[0].text
        value = price+" , "+"change:"+up_down
        content = ("{} \nCMP: {}".format(news_text,value))
        toaster.show_toast(company_name,content,icon_path="python.ico",duration=30)
        time.sleep(10)
        

def main():    
    url = "https://www.moneycontrol.com/india/stockpricequote/"    #source url
    toaster = ToastNotifier()       #win10toast.ToastNotifier() 
    page = requests.get(url,verify=False)
    soup = BeautifulSoup(page.content,'html.parser')    
    
    #name2link dict (key,value)==(company_name,link2_stock_news) 
    name2link = {}
    ref = soup.find_all('a',{'class':'bl_12'})
    for _ in ref:
      name2link[_.text]=_['href']
    
    #deleting first 2 unneccessary items of dict 
    del name2link['']
    del name2link[' Customize']

    
    #User input
    temp_input = list(input("Enter stocks name: ").split(','))
    
    #remove extra space around Stock_name provided as input by user
    user_input = []
    for _ in temp_input:
        user_input.append(_.strip())
    
    temp_counter=0

    while (True): 
        if temp_counter==0:
            news_popup(user_input,toaster,name2link)
            temp_counter+=1
        else:
            time.sleep(1800)
            news_popup(user_input,toaster,name2link)



if __name__ == "__main__":
    main()
    
    


      


