"""Module for scraping cacao data of the current data and of the preveious 5 days"""
from random import choice
import requests
from bs4 import BeautifulSoup as bs
import json


desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

link_of_page = "https://www.boursorama.com/bourse/matieres-premieres/cours/_CJ/"


def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
 


def scrapCacaoToJson() :


#getting page data
    page = requests.get(link_of_page,headers=random_headers())
    soup = bs(page.content,'html.parser',from_encoding="iso-8859-1")


#prepare the dict, where current is the data of today and historic_5days is for the previous 5 days
    data_cacao = {'current':{}}


#current contains the last value, the incative value and the variation percent
    data_cacao['current']['last_value'] = soup.find('span',{"class":"c-instrument c-instrument--last"}).text.strip()
    data_cacao['current']['indicative_value'] = soup.find('span',{"class":"c-faceplate__indicative-value"}).text.strip()
    data_cacao['current']['variation'] = soup.find('span',{"c-instrument c-instrument--variation"}).text.strip()

    """prepare to fill the historic_5days with the data in the table containing 5 consecutive days     
    of the value (Der.),the variation percent (Var.), the indicative value (Ouv.)"""

    table_5days = soup.find('table', class_='c-table c-table--generic')
    headers = table_5days.find_all('th')
    body = table_5days.find_all('td')
    
    
    for i in range(0,len(body),len(headers)):
        opt = ''.join(e for e in body[i].text if e.isalnum())
        data_cacao[opt] = {}
        for j in range(1,len(headers)):
            date = headers[j].get_text().strip()
            data = body[i+j].get_text().strip()
            data_cacao[opt][date] = data

#return the json of the dict
    return data_cacao


