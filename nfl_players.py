# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_players(year):
    
    players_url = 'https://www.pro-football-reference.com/years/' + str(year) + '/fantasy.htm'
    
    result = requests.get(players_url)
    soup = BeautifulSoup(result.content)
    
    table = soup.find('div', attrs = {'class':'table_container is_setup'})
    table_player_info = soup.findAll('td', attrs = {'data-stat':'player'})
    
    player_names = []
    player_codes = []
    
    for player in table_player_info:
        
        player_name = player.text
        player_name = player_name.replace("*", "")
        player_name = player_name.replace("+", "")
        player_names.append(player_name.strip())
        
        player_codes.append(player.find("a", href=True)["href"])
        
    return(pd.DataFrame(list(zip(player_names, player_codes)), columns = ['player_name', 'player_code']))
    
    

def get_player_details(player_code):

    player_url = 'https://www.pro-football-reference.com' + player_code
    
    result = requests.get(player_url)
    soup = BeautifulSoup(result.content)
    
    table = soup.find('div', attrs = {'id':'meta'})
    table_player_info = soup.find('img', attrs = {'itemscope':'image'})
    
    details = {}
    
    try:
        details['player_image_url'] = table_player_info['src']
    except:
        details['player_image_url']= "Image unavailable"
    
    try:
        details['player_position'] = soup.find('strong', text="Position").next_sibling.strip().replace(": ", "")
    except:
        details['player_position'] = "Position unavailable"
    
    try:
        details['player_team'] = soup.find('strong', text="Team").next_sibling.next_sibling.text
    except:
        details['player_team'] = "No team"
    
    return(details)
    
    
    
players = get_players(2020)

player_codes = []
player_image_urls = []
player_positions = []
player_teams = []

num = 0
    
for code in players['player_code']:
    
    details = get_player_details(code)
    
    player_codes.append(code)
    player_image_urls.append(details['player_image_url'])
    player_positions.append(details['player_position'])
    player_teams.append(details['player_team'])
    
    num = num + 1
    print(num)
    
player_details = pd.DataFrame(list(zip(player_codes, player_image_urls, player_positions, player_teams)),
                              columns = ['player_code', 'player_image_url', 'player_position', 'player_team'])

player_db = pd.merge(players, player_details, on='player_code', how='inner')

player_db.to_csv('player_db.csv', index = False)
    
    
