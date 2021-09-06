#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 19:07:37 2021

@author: JustinFerrara
"""

import pandas as pd
import pymysql


def upload_team_stats(data):
    
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
            
            cursor.execute('DROP TABLE IF EXISTS TeamDetails;')
            
            print('Creating \'TeamDetails\' table...')
            
            cursor.execute('''
                           CREATE TABLE TeamDetails(
                               year INT(4),
                               wins INT(2),
                               losses INT(2),
                               ties INT(2),
                               playoffs INT(1),
                               offensive_rank_points INT(2),
                               offensive_rank_yards INT(2),
                               defensive_rank_points INT(2),
                               defensive_rank_yards INT(2),
                               offensive_rank FLOAT(4),
                               defensive_rank FLOAT(4),
                               team_code VARCHAR(3))
                           ''')
            
            print('Table created successfully...')
            
            # creating column list for insertion
            cols = "`,`".join([str(i) for i in data.columns.tolist()])
            
            # Insert DataFrame recrds one by one.
            for i,row in data.iterrows():
                
                sql = "INSERT INTO `TeamDetails` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
                cursor.execute(sql, tuple(row))
            
                # the connection is not autocommitted by default, so we must commit to save our changes
                db.commit()
                
            print("Table import complete!")
                        
    except:
        
        print("Error while connecting to MySQL")
        
    finally:
        
        db.close()
        
        print("Connection closed")
        
        

team_stats = pd.read_csv('team_stats_db.csv')

upload_team_stats(team_stats)