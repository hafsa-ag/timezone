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

link_of_page = "https://24timezones.com/temps_du_monde2.php"


def random_headers():
    return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
 


def scrapTimeZone() :


#getting page data
    page = requests.get(link_of_page,headers=random_headers())
    soup = bs(page.text,'html.parser',from_encoding="iso-8859-1")

    table_all = soup.find('table', class_='dataTab1 genericBlock')
    trs = table_all.find_all('tr')

    countries = {}
    countries['countries'] = []
    tmp_ctr = ""
    tmp_state = ""
    for t in range(len(trs)):
        tds = trs[t].find_all('td')
        ctry =  tds[0].find('a',class_='country_link')
        state =  tds[0].find('a',class_='state_link')
        if ctry :
            tmp_ctr =  ctry.text
            tmp_state = ""
            country={}
            country['country'] = tmp_ctr
            country['components'] = []
            countries['countries'].append(cou
                ntry)
        elif state : 
            tmp_state = state.text
            tmp = list(filter(lambda country: country['country'] == tmp_ctr,countries['countries']))[0]
            tmp['components'].append({'state':tmp_state,'components':[]})
        else :
            if tds[0].text=='-':
                tmp_state = ""
            else :
                for a in tds[0].find_all('a'):
                    city = {}
                    city['city'] =  a.text
                    city['time'] = tds[1].find('span',class_='time_format_24').text
                    if tmp_state == "":
                        tmp = list(filter(lambda country: country['country'] == tmp_ctr,countries['countries']))[0]
                        tmp['components'].append(city)
                    else :
                        tmp = list(filter(lambda country: country['country'] == tmp_ctr,countries['countries']))[0]
                        tmp = list(filter(lambda state: state['state']==tmp_state,tmp['components']))[0]
                        tmp['components'].append(city)
    return countries