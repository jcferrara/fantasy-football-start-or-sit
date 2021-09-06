#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 00:20:16 2021

@author: JustinFerrara
"""

import pandas as pd


def get_schedule(year):
    
    url = 'https://www.pro-football-reference.com/years/' + str(year) + '/games.htm'
    
    table = pd.read_html(url)[0]
    
    table.columns = ['week_number', 'day_of_week', 'date', 'team_visitor', 'points_visitor',
                     'at', 'team_home', 'points_home', 'start_time']
    
    table = table[['week_number', 'date', 'team_visitor', 'team_home']]
    
    filter_values = ['Pre0','Pre1','Pre2','Pre3', 'Pre4', 'Week'] 
    pattern = '|'.join(filter_values)
    
    table = table.loc[~(table['week_number'].str.contains(pattern, case=False))]
    
    date = []
    
    for d in table['date']:
        
        if (d.find('January') == 0 or d.find('February') == 0):
            
            date.append(d + ' ' + str(year+1))
        
        else:
            
            date.append(d + ' ' + str(year))
            
    table['date'] = date
    table['date'] = pd.to_datetime(table['date'], format='%B %d %Y').dt.date
    
    table['teams_in_game'] = table['team_visitor'] + '-' + table['team_home']
    
    week_num = []
    date_num = []
    opponent = []
    team = []
    
    for t in set(table['team_home']):
        
        temp_table = table[table['teams_in_game'].str.contains(t)]
        
        for w, d, h, a in zip(temp_table['week_number'], temp_table['date'], temp_table['team_home'], temp_table['team_visitor']):
            
            if h == t:
                
                week_num.append(w)
                date_num.append(d)
                opponent.append(a)
                team.append(t)
                                
            else:
                
                week_num.append(w)
                date_num.append(d)
                opponent.append(h)
                team.append(t)
                
    return_table = pd.DataFrame(list(zip(week_num, date_num, opponent, team)),
                                columns=['week_number', 'date', 'opponent', 'team'])
                    
    return(return_table)
    

schedule = get_schedule(2021)

schedule.to_csv('schedule_db.csv', index = False)
