#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 19:47:52 2021

@author: JustinFerrara
"""

import pandas as pd
import pymysql

def upload_gamelog(data):
    
    try:
        
        db = pymysql.connect(host = host_name, 
                             user = user_name, 
                             passwd = password,
                             db = db_name)
        
        if db.open:
            
            cursor = db.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record[0])
            
            cursor.execute('DROP TABLE IF EXISTS Gamelog;')
            
            print('Creating \'Gamelog\' table....')
            
            cursor.execute('''
                           CREATE TABLE Gamelog(
                                date DATE,
                                week_number INT(2),
                                player_team VARCHAR(50),
                                game_setting VARCHAR(8),
                                game_opponent VARCHAR(3),
                                game_result VARCHAR(12),
                                passing_completions INT(4),
                                passing_attempts INT(4),
                                passing_completion_pct FLOAT(6),
                                passing_yards INT(4),
                                passing_td INT(2),
                                passing_int INT(2),
                                passing_qbr FLOAT(4),
                                passing_sacks FLOAT(3),
                                passing_yards_per_att FLOAT(8),
                                rushing_attempts INT(4),
                                rushing_yards INT(4),
                                rushing_yards_per_att FLOAT(8),
                                rushing_td INT(2),
                                receiving_targets INT(2),
                                receiving_receptions INT(2),
                                receiving_yards INT(3),
                                receiving_yards_per_reception FLOAT(8),
                                receiving_td INT(2),
                                receiving_catch_pct FLOAT(8),
                                receiving_yards_per_target FLOAT(8),
                                scoring_total_td INT(2),
                                scoring_total_points INT(3),
                                fumbles_num INT(2),
                                fumbles_num_lost INT(2),
                                fumbles_num_recovered INT(2),
                                num_off_snaps INT(3),
                                pct_off_snaps FLOAT(8),
                                num_st_snaps INT(3),
                                pct_st_snaps FLOAT(8),
                                player_code VARCHAR(50))
                           ''')
            
            print('Table created successfully....')
            
            for i, row in data.iterrows():

                sql = '''INSERT INTO `Gamelog` 
                (`date`,
                `week_number`,
                `player_team`,
                `game_setting`,
                `game_opponent`,
                `game_result`,
                `passing_completions`,
                `passing_attempts`,
                `passing_completion_pct`,
                `passing_yards`,
                `passing_td`,
                `passing_int`,
                `passing_qbr`,
                `passing_sacks`,
                `passing_yards_per_att`,
                `rushing_attempts`,
                `rushing_yards`,
                `rushing_yards_per_att`,
                `rushing_td`,
                `receiving_targets`,
                `receiving_receptions`,
                `receiving_yards`,
                `receiving_yards_per_reception`,
                `receiving_td`,
                `receiving_catch_pct`,
                `receiving_yards_per_target`,
                `scoring_total_td`,
                `scoring_total_points`,
                `fumbles_num`,
                `fumbles_num_lost`,
                `fumbles_num_recovered`,
                `num_off_snaps`,
                `pct_off_snaps`,
                `num_st_snaps`,
                `pct_st_snaps`,
                `player_code`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                
                cursor.execute(sql, tuple(row))

                db.commit()
                
            print("Table import complete!")
                        
    except:
        
        print("Error while connecting to MySQL")
        
    finally:
        
        db.close()
        
        print("Connection closed")

game_stats = pd.read_csv('game_stats_db.csv')

upload_gamelog(game_stats)




