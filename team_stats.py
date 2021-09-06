#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 17:44:39 2021

@author: JustinFerrara
"""

import pandas as pd


def get_teams():
    
    teams_tuple = [("Arizona Cardinals", "ARI", "crd", "https://a.espncdn.com/i/teamlogos/nfl/500/ari.png"), 
               ("San Francisco 49ers", "SFO", "sfo", "https://a.espncdn.com/i/teamlogos/nfl/500/sf.png"),
               ("Los Angeles Rams", "LAR", "ram", "https://a.espncdn.com/i/teamlogos/nfl/500/lar.png"),
               ("Seattle Seahawks", "SEA", "sea", "https://a.espncdn.com/i/teamlogos/nfl/500/sea.png"),
               ("New Orleans Saints", "NOR", "nor", "https://a.espncdn.com/i/teamlogos/nfl/500/no.png"),
               ("Tampa Bay Buccaneers", "TAM", "tam", "https://a.espncdn.com/i/teamlogos/nfl/500/tb.png"),
               ("Carolina Panthers", "CAR", "car", "https://a.espncdn.com/i/teamlogos/nfl/500/car.png"),
               ("Atlanta Falcons", "ATL", "atl", "https://a.espncdn.com/i/teamlogos/nfl/500/atl.png"),
               ("Kansas City Chiefs", "KAN", "kan", "https://a.espncdn.com/i/teamlogos/nfl/500/kc.png"),
               ("Las Vegas Raiders", "LVR", "rai", "https://a.espncdn.com/i/teamlogos/nfl/500/lv.png"),
               ("Los Angeles Chargers", "LAC", "sdg", "https://a.espncdn.com/i/teamlogos/nfl/500/lac.png"),
               ("Denver Broncos", "DEN", "den", "https://a.espncdn.com/i/teamlogos/nfl/500/den.png"),
               ("Tennessee Titans", "TEN", "oti", "https://a.espncdn.com/i/teamlogos/nfl/500/ten.png"),
               ("Indianapolis Colts", "IND", "clt", "https://a.espncdn.com/i/teamlogos/nfl/500/ind.png"),
               ("Houston Texans", "HOU", "htx", "https://a.espncdn.com/i/teamlogos/nfl/500/hou.png"),
               ("Jacksonville Jaguars", "JAX", "jax", "https://a.espncdn.com/i/teamlogos/nfl/500/jax.png"),
               ("Green Bay Packers", "GNB", "gnb", "https://a.espncdn.com/i/teamlogos/nfl/500/gb.png"),
               ("Chicago Bears", "CHI", "chi", "https://a.espncdn.com/i/teamlogos/nfl/500/chi.png"),
               ("Minnesota Vikings", "MIN", "min", "https://a.espncdn.com/i/teamlogos/nfl/500/chi.png"),
               ("Detroit Lions", "DET", "det", "https://a.espncdn.com/i/teamlogos/nfl/500/det.png"),
               ("Washington Football Team", "WAS", "was", "https://a.espncdn.com/i/teamlogos/nfl/500/wsh.png"),
               ("New York Giants", "NYG", "nyg", "https://a.espncdn.com/i/teamlogos/nfl/500/nyg.png"),
               ("Dallas Cowboys", "DAL", "dal", "https://a.espncdn.com/i/teamlogos/nfl/500/dal.png"),
               ("Philadelphia Eagles", "PHI", "phi", "https://a.espncdn.com/i/teamlogos/nfl/500/phi.png"),
               ("Pittsburgh Steelers", "PIT", "pit", "https://a.espncdn.com/i/teamlogos/nfl/500/pit.png"),
               ("Baltimore Ravens", "BAL", "rav", "https://a.espncdn.com/i/teamlogos/nfl/500/bal.png"),
               ("Cleveland Browns", "CLE", "cle", "https://a.espncdn.com/i/teamlogos/nfl/500/cle.png"),
               ("Cincinnati Bengals", "CIN", "cin", "https://a.espncdn.com/i/teamlogos/nfl/500/cin.png"),
               ("Buffalo Bills", "BUF", "buf", "https://a.espncdn.com/i/teamlogos/nfl/500/buf.png"),
               ("Miami Dolphins", "MIA", "mia", "https://a.espncdn.com/i/teamlogos/nfl/500/mia.png"),
               ("New England Patriots", "NWE", "nwe", "https://a.espncdn.com/i/teamlogos/nfl/500/ne.png"),
               ("New York Jets", "NYJ", "nyj", "https://a.espncdn.com/i/teamlogos/nfl/500/nyj.png")]

    teams = pd.DataFrame(teams_tuple, columns=["team_name", "team_abbreviation", "team_code", "team_image_url"])
    
    return(teams)
    

def get_team_stats(team_code):
    
    url = 'https://www.pro-football-reference.com/teams/' + str(team_code) + '/'
    
    table = pd.read_html(url)[0]
    
    col_names = []
    
    for col in table.columns:
        col_names.append(col[0] + "_" + col[1])
        
    table.columns = col_names
    
    table = table.rename(columns={"Unnamed: 0_level_0_Year":"year",
                          "Unnamed: 1_level_0_Lg":"league",
                          "Unnamed: 2_level_0_Tm":"team",
                          "Unnamed: 3_level_0_W":"wins",
                          "Unnamed: 4_level_0_L":"losses",
                          "Unnamed: 5_level_0_T":"ties",
                          "Unnamed: 6_level_0_Div. Finish":"division_finish",
                          "Unnamed: 7_level_0_Playoffs":"playoffs",
                          "Off Rank_Pts":"offensive_rank_points",
                          "Off Rank_Yds":"offensive_rank_yards",
                          "Def Rank_Pts":"defensive_rank_points",
                          "Def Rank_Yds":"defensive_rank_yards"})
    
    table = table[['year', 'wins', 'losses', 'ties', 'playoffs', 'offensive_rank_points',
                   'offensive_rank_yards', 'defensive_rank_points', 'defensive_rank_yards']]
    
    table['playoffs'] = table['playoffs'].astype(str)
    table['playoffs'] = table['playoffs'].apply(lambda x: 0 if x == "nan" else 1)
    
    table = table.dropna(subset=['year', 'offensive_rank_points'])
    table = table[table['year'] != "Year"]
    
    table[table.columns] = table[table.columns].apply(pd.to_numeric)
    table['offensive_rank'] = (table['offensive_rank_points'] + table['offensive_rank_yards'])/2
    table['defensive_rank'] = (table['defensive_rank_points'] + table['defensive_rank_yards'])/2
    
    table = table[table['year'] >= 2018]
    
    table['team_code'] = team_code
    
    return(table)



teams = get_teams()
team_stats = pd.DataFrame()

for t in teams['team_code']:
    
    team_stats_temp = get_team_stats(t)
    team_stats = pd.concat([team_stats, team_stats_temp])
    
team_stats.to_csv('team_stats_db.csv', index = False)
teams.to_csv('teams_db.csv', index = False)

