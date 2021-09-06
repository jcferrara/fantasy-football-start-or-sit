# -*- coding: utf-8 -*-
"""
Spyder Editor

Fantasy Football Start 'em or Sit 'em
Streamlit Web App
Created by: Justin Ferrara
"""

import streamlit as st
import pymysql
import pandas as pd
from datetime import date

st.set_page_config(layout="wide")

today = date.today()

@st.cache(suppress_st_warning=True)
def initial_queries():
    
    db = pymysql.connect(host = host_name,
                     user = user_name,
                     passwd = password,
                     db = db_name)
    
    cursor = db.cursor()
    cursor.execute("USE fantasy_football;")

    player_sql = '''
    SELECT Player.player_name, Player.player_code, Player.player_image_url, Player.player_position, Team.team_image_url
    FROM Player
    INNER JOIN Team ON Player.player_team = Team.team_name;
    '''
    players = pd.read_sql(player_sql, db)
    
    schedule_sql = '''
    SELECT Schedule.week_number, MIN(Schedule.date) AS week_start, MAX(Schedule.date) AS week_end
    FROM Schedule
    GROUP BY Schedule.week_number;
    '''
    schedule = pd.read_sql(schedule_sql, db)
    
    schedule = schedule[schedule['week_start'] >= today]
    week_num = list(schedule['week_number'])[0]
    
    return(players, week_num)

output = initial_queries()

players = output[0]
week_num = output[1]

st.title(''' Fantasy Football Start 'em or Sit 'em ''')
st.caption('Open source tool for gaining that extra edge in your fantasy football matchups')
st.write(''' The tool you use after you have scoured analyst reports and memorized fantasy point projections, but still don't know which player to start''')

st.write(''' ## Compare players ''')
my_expander = st.expander(label='Filter by position')
pos = my_expander.multiselect('Select position(s)', ["QB","WR","RB","TE"], "QB")

players_filtered = players[players['player_position'].isin(pos)]

st.container()
col1, col2 = st.columns(2)
col1.subheader('Player 1')
col2.subheader('Player 2')

player1_name = col1.selectbox('Select player', set(players_filtered['player_name']), key="player1")
player2_name = col2.selectbox('Select player', set(players_filtered['player_name']), key="player2")

player1 = players_filtered[players_filtered['player_name'] == player1_name]
player1_image = player1['player_image_url']
player1_team_logo = player1['team_image_url']

player2 = players_filtered[players_filtered['player_name'] == player2_name]
player2_image = player2['player_image_url']
player2_team_logo = player2['team_image_url']

col1.image(list(player1_team_logo)[0], width=100)
col1.image(list(player1_image)[0], width=85)

col2.image(list(player2_team_logo)[0], width=100)
col2.image(list(player2_image)[0], width=85)

db = pymysql.connect(host = host_name,
                 user = user_name,
                 passwd = password,
                 db = db_name)

cursor = db.cursor()
cursor.execute("USE fantasy_football;")

# find player's next matchup
matchup_sql = '''
SELECT Schedule.date, Schedule.opponent, TeamDetails.defensive_rank AS prior_yr_def_rank
FROM (Schedule
INNER JOIN Player ON Player.player_team = Schedule.team)
LEFT JOIN Team ON Schedule.opponent = Team.team_name
LEFT JOIN TeamDetails ON Team.team_code = TeamDetails.team_code
WHERE Schedule.week_number = %(week_num)s AND Player.player_code = %(player_cod)s AND TeamDetails.year = (year(Schedule.date)-1);
'''

player1_next_matchup_df = pd.read_sql(matchup_sql, db, params={"week_num":1, "player_cod":list(player1['player_code'])[0]})
player2_next_matchup_df = pd.read_sql(matchup_sql, db, params={"week_num":1, "player_cod":list(player2['player_code'])[0]})

col1.write("**Next matchup: ** vs. " + list(player1_next_matchup_df['opponent'])[0])
col2.write("**Next matchup: ** vs. " + list(player2_next_matchup_df['opponent'])[0])

player1_next_matchup_rank = list(player1_next_matchup_df['prior_yr_def_rank'])[0]
player2_next_matchup_rank = list(player2_next_matchup_df['prior_yr_def_rank'])[0]

col1.write("**Opponent defensive rank: **" + str(player1_next_matchup_rank) + ' / 32.0')
col2.write("**Opponent defensive rank: **" + str(player2_next_matchup_rank) + ' / 32.0')

col1.write("*Last 3 games vs. similarly rated defenses*")
col2.write("*Last 3 games vs. similarly rated defenses*")

stats_sql = '''
SELECT
Gamelog.date,
Gamelog.player_team,
Gamelog.game_opponent,
Gamelog.passing_completions,
Gamelog.passing_attempts,
Gamelog.passing_completion_pct,
Gamelog.passing_yards,
Gamelog.passing_td,
Gamelog.passing_int,
Gamelog.passing_qbr,
Gamelog.passing_sacks,
Gamelog.passing_yards_per_att,
Gamelog.rushing_attempts,
Gamelog.rushing_yards,
Gamelog.rushing_yards_per_att,
Gamelog.rushing_td,
Gamelog.receiving_targets,
Gamelog.receiving_receptions,
Gamelog.receiving_yards,
Gamelog.receiving_yards_per_reception,
Gamelog.receiving_td,
Gamelog.receiving_catch_pct,
Gamelog.receiving_yards_per_target,
Gamelog.pct_off_snaps,
Gamelog.player_code,
TeamDetails.defensive_rank AS opponent_defensive_rank_prior_yr,
Player.player_position
FROM Gamelog
LEFT JOIN Team ON Gamelog.game_opponent = Team.team_abbreviation
LEFT JOIN TeamDetails ON Team.team_code = TeamDetails.team_code
LEFT JOIN Player ON Gamelog.player_code = Player.player_code
WHERE TeamDetails.year = (year(Gamelog.date)) AND Gamelog.player_code = %(player_code)s
ORDER BY Gamelog.date DESC;
'''

player1_all_stats_raw = pd.read_sql(stats_sql, db, params={"player_code":list(player1['player_code'])[0]})
player2_all_stats_raw = pd.read_sql(stats_sql, db, params={"player_code":list(player2['player_code'])[0]})

player1_all_stats_raw['def_quartile'] = player1_all_stats_raw['opponent_defensive_rank_prior_yr'].apply(lambda x: "Quartile 4" if x >= 27 else "Quartile 3" if x >= 21 else "Quartile 2" if x >= 14 else "Quartile 1")
player2_all_stats_raw['def_quartile'] = player2_all_stats_raw['opponent_defensive_rank_prior_yr'].apply(lambda x: "Quartile 4" if x >= 27 else "Quartile 3" if x >= 21 else "Quartile 2" if x >= 14 else "Quartile 1")

if player1_next_matchup_rank >= 27:
    player1_next_matchup_quartile = "Quartile 4"
elif player1_next_matchup_rank >= 21:
    player1_next_matchup_quartile = "Quartile 3"
elif player1_next_matchup_rank >= 14:
    player1_next_matchup_quartile = "Quartile 2"
else:
    player1_next_matchup_quartile = "Quartile 1"

if player2_next_matchup_rank >= 27:
    player2_next_matchup_quartile = "Quartile 4"
elif player2_next_matchup_rank >= 21:
    player2_next_matchup_quartile = "Quartile 3"
elif player2_next_matchup_rank >= 14:
    player2_next_matchup_quartile = "Quartile 2"
else:
    player2_next_matchup_quartile = "Quartile 1"


player1_all_stats = player1_all_stats_raw[player1_all_stats_raw['def_quartile'] == player1_next_matchup_quartile]
player2_all_stats = player2_all_stats_raw[player2_all_stats_raw['def_quartile'] == player2_next_matchup_quartile]


if list(player1_all_stats['player_position'])[0] == "QB":

    cols = player1_all_stats.filter(regex='date|game_opponent|pct_off_snaps|passing').columns

elif list(player1_all_stats['player_position'])[0] == "RB":

    cols = player1_all_stats.filter(regex='date|game_opponent|pct_off_snaps|rushing|receiving').columns

elif list(player1_all_stats['player_position'])[0] in ["WR", "TE"]:

    cols = player1_all_stats.filter(regex='date|game_opponent|pct_off_snaps|receiving').columns

player1_stats = player1_all_stats[list(cols)]

if list(player2_all_stats['player_position'])[0] == "QB":

    cols = player2_all_stats.filter(regex='date|game_opponent|pct_off_snaps|passing').columns

elif list(player2_all_stats['player_position'])[0] == "RB":

    cols = player2_all_stats.filter(regex='date|game_opponent|pct_off_snaps|rushing|receiving').columns

elif list(player2_all_stats['player_position'])[0] in ["WR", "TE"]:

    cols = player2_all_stats.filter(regex='date|game_opponent|pct_off_snaps|receiving').columns

player2_stats = player2_all_stats[list(cols)]

col1.write(player1_stats[0:3])
col2.write(player2_stats[0:3])

db.close()

my_expander2 = st.expander(label='Notes on methodology')
my_expander2.markdown('''
                      * Opponent defensive rank is calculated as average of a team's rank (out of 32 teams) on yardage allowed per game and points allowed per game. 1 = best defensive rank, 32 = worst defensive rank
                      * Similarly rated defenses defined as the same quartile of score on the opponent defensive rank measure. For example, a team with a defensive rank of 28.0 would be classified as *Quartile 4*. Performances against similarly rated defenses would include only games against teams with a *Quartile 4* defensive rating. 
                      * Rookie players are excluded from the tool given the methodology's reliance on historical data
                      ''')

st.markdown('Created by [Justin Ferrara](https://github.com/jcferrara)')
st.markdown('Data and images sourced from [ESPN](https://www.espn.com/), [Pro Football Reference](https://www.pro-football-reference.com/)')


