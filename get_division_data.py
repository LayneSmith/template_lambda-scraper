import requests
from bs4 import BeautifulSoup
import re
import csv
import random
# from random import randint
from datetime import datetime, date
from time import sleep
from io import StringIO

# Pretend to be a web browser
random_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36 OPR/15.0.1147.100',
    'Mozilla/5.0 (Windows; U; Windows NT 5.0; es-ES; rv:1.8.0.3) Gecko/20060426 Firefox/1.5.0.3',
    'Mozilla/5.0 (Linux; Android 7.1; Pixel Build/NDE63L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.68 Mobile Safari/537.36',
]

random.shuffle(random_agents)
browser_headers = (random_agents[0])

def getID(url):
    # team_url = 'http://events.gotsport.com/events/' + url
    # print(team_url)
    # print(url)
    # team_url_r = requests.get(team_url, timeout=60, headers={
    #     'User-Agent': browser_headers
    # })

    # run the requests through soup
    # team_url_soup = BeautifulSoup(team_url_r.content, "html.parser")

    # save details
    # elm = team_url_soup.findAll("a", {"class", "TinyText"})[1]['href']
    id = url.split("applicationID=")[1].split("&")[0]
    return id


def scrape_division():
    print('--- Scraping division data ---')

    division_url = 'http://events.gotsport.com/events/results.aspx?EventID=67315&Gender=Girls&Age=14'
    print(division_url)
    url_r = requests.get(division_url, timeout=60, headers={
        'User-Agent': browser_headers
    })

    # run the requests through soup
    url_soup = BeautifulSoup(url_r.content, "html.parser")

    # save details
    tables = url_soup.findAll("div", {"class", "grid_4"})

    # ###########################################
    #                STANDINGS                  #
    # ###########################################
    standingsTable = tables[1].find("table")
    trs = standingsTable.findAll("tr")

    payload_array = [['id', 'name', 'rank', 'matches', 'wins', 'losses', 'draws', 'goals_for', 'goals_against', 'points']]

    for row in trs[1:]:
        tds = row.findAll("td")

        try:
            url = tds[0].find('a')['href']
            id = getID(url)
        except:
            id = 'N/A'

        name_array = tds[0].text.split(")")
        try:
            rank = int(name_array[0])
            name = re.sub("05G | 05G|05", "", name_array[1].split("(")[0]).strip()
        except:
            rank = 'N/A'
            name = re.sub("05|05G", "", name_array[0].split("(")[0]).strip()

        try:
            matches = int(tds[1].text.strip())
        except:
            matches = 0

        try:
            wins = int(tds[2].text.strip())
        except:
            wins = 0

        try:
            losses = int(tds[3].text.strip())
        except:
            losses = 0

        try:
            draws = int(tds[4].text.strip())
        except:
            draws = 0

        try:
            goals_for = int(tds[5].text.strip())
        except:
            goals_for = 0

        try:
            goals_against = int(tds[6].text.strip())
        except:
            goals_against = 0

        try:
            points = int(tds[7].text.strip())
        except:
            points = 0

        payload_array.append([id, name, rank, matches, wins, losses, draws, goals_for, goals_against, points])

    # Save payload_array into StringIO() and output as text string
    si = StringIO()
    cw = csv.writer(si)


    for row in payload_array:
        cw.writerow(row)

    payload = si.getvalue()

    # print(payload)
    return payload

if __name__ == '__main__':
    scrape_division()
