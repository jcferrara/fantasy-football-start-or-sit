#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 01:25:36 2021

@author: JustinFerrara
"""

import pandas as pd


def get_gamelog(player_code, year):

    player_url = 'https://www.pro-football-reference.com' + player_code[0:len(player_code)-4] + '/gamelog/' + str(year) + '/'
    
    table = pd.read_html(player_url)
    
    table = table[0]
    
    col_names = []
    
    for col in table.columns:
        col_names.append(col[0] + "_" + col[1])
        
    table.columns = col_names
    
    table = table.rename(columns={"Unnamed: 0_level_0_Rk":"row_tracker",
                          "Unnamed: 1_level_0_Date":"date",
                          "Unnamed: 2_level_0_G#":"game_number",
                          "Unnamed: 3_level_0_Week":"week_number",
                          "Unnamed: 4_level_0_Age":"player_age",
                          "Unnamed: 5_level_0_Tm":"player_team",
                          "Unnamed: 6_level_0_Unnamed: 6_level_1":"game_setting",
                          "Unnamed: 7_level_0_Opp":"game_opponent",
                          "Unnamed: 8_level_0_Result":"game_result",
                          "Unnamed: 9_level_0_GS":"game_started"})
    
    table.drop(table.tail(1).index, inplace = True)
    
    table['game_started'] = table['game_started'].astype(str)
    table['game_played'] = table['game_started'].apply(lambda x: "*" if x == "nan" else x)
    table = table[table['game_played'] == "*"]
    
    table = table.astype(str)
    
    table['player_code'] = player_code
    
    table['game_setting'] = table['game_setting'].apply(lambda x: "Away" if x == "@" else "Home")
    
    table = table.replace({'%': ''}, regex=True)
    
    return(table)



game_stats = pd.DataFrame()
num = 0

for i in players['player_code']:
    
    for y in ['2020', '2019']:
        
        try:
            gamelog = get_gamelog(i, y)
            game_stats = pd.concat([game_stats, gamelog])
        except:
            continue
        
    num += 1
    print(num)
    
    

game_stats = game_stats[['date', 'week_number', 'player_team', 'game_setting', 'game_opponent', 'game_result',
                          'Passing_Cmp', 'Passing_Att', 'Passing_Cmp%', 'Passing_Yds', 'Passing_TD', 'Passing_Int', 'Passing_Rate', 'Passing_Sk', 'Passing_Y/A',
                          'Rushing_Att', 'Rushing_Yds', 'Rushing_Y/A', 'Rushing_TD', 
                          'Receiving_Tgt', 'Receiving_Rec', 'Receiving_Yds', 'Receiving_Y/R', 'Receiving_TD', 'Receiving_Ctch%', 'Receiving_Y/Tgt',
                          'Scoring_TD', 'Scoring_Pts',
                          'Fumbles_Fmb', 'Fumbles_FL', 'Fumbles_FR',
                          'Off. Snaps_Num', 'Off. Snaps_Pct', 'ST Snaps_Num', 'ST Snaps_Pct',
                          'player_code']]

game_stats.columns = ['date', 'week_number', 'player_team', 'game_setting', 'game_opponent', 'game_result',
                       'passing_completions', 'passing_attempts', 'passing_completion_pct', 'passing_yards', 'passing_td', 'passing_int', 'passing_qbr', 'passing_sacks', 'passing_yards_per_att',
                       'rushing_attempts', 'rushing_yards', 'rushing_yards_per_att', 'rushing_td', 
                       'receiving_targets', 'receiving_receptions', 'receiving_yards', 'receiving_yards_per_reception', 'receiving_td', 'receiving_catch_pct', 'receiving_yards_per_target',
                       'scoring_total_td', 'scoring_total_points',
                       'fumbles_num', 'fumbles_num_lost', 'fumbles_num_recovered',
                       'num_off_snaps', 'pct_off_snaps', 'num_st_snaps', 'pct_st_snaps',
                       'player_code']

game_stats = game_stats.replace("nan", "0")
game_stats = game_stats.fillna("0")

game_stats[[ 'passing_completions',
             'passing_attempts', 
             'passing_completion_pct', 
             'passing_yards', 
             'passing_td', 
             'passing_int', 
             'passing_qbr', 
             'passing_sacks', 
             'passing_yards_per_att',
             'rushing_attempts', 
             'rushing_yards', 
             'rushing_yards_per_att', 
             'rushing_td', 
             'receiving_targets', 
             'receiving_receptions', 
             'receiving_yards', 
             'receiving_yards_per_reception', 
             'receiving_td', 
             'receiving_catch_pct', 
             'receiving_yards_per_target',
             'scoring_total_td', 
             'scoring_total_points',
             'fumbles_num', 
             'fumbles_num_lost', 
             'fumbles_num_recovered',
             'num_off_snaps', 
             'pct_off_snaps', 
             'num_st_snaps', 
             'pct_st_snaps']] = game_stats[[ 'passing_completions',
                                             'passing_attempts', 
                                             'passing_completion_pct', 
                                             'passing_yards', 
                                             'passing_td', 
                                             'passing_int', 
                                             'passing_qbr', 
                                             'passing_sacks', 
                                             'passing_yards_per_att',
                                             'rushing_attempts', 
                                             'rushing_yards', 
                                             'rushing_yards_per_att', 
                                             'rushing_td', 
                                             'receiving_targets', 
                                             'receiving_receptions', 
                                             'receiving_yards', 
                                             'receiving_yards_per_reception', 
                                             'receiving_td', 
                                             'receiving_catch_pct', 
                                             'receiving_yards_per_target',
                                             'scoring_total_td', 
                                             'scoring_total_points',
                                             'fumbles_num', 
                                             'fumbles_num_lost', 
                                             'fumbles_num_recovered',
                                             'num_off_snaps', 
                                             'pct_off_snaps', 
                                             'num_st_snaps', 
                                             'pct_st_snaps']].apply(pd.to_numeric)

game_stats.to_csv('game_stats_db.csv', index = False)








