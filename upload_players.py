#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 23:59:06 2021

@author: JustinFerrara
"""

import pandas as pd
import pymysql


def upload_players(data):
    
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
            
            cursor.execute('DROP TABLE IF EXISTS Player;')
            
            print('Creating \'Player\' table...')
            
            cursor.execute('''
                           CREATE TABLE Player(
                                player_name VARCHAR(50),
                                player_code VARCHAR(50),
                                player_image_url VARCHAR(100),
                                player_position VARCHAR(2),
                                player_team VARCHAR(50))
                           ''')
            
            print('Table created successfully...')
            
            # creating column list for insertion
            cols = "`,`".join([str(i) for i in data.columns.tolist()])
            
            # Insert DataFrame recrds one by one.
            for i,row in data.iterrows():
                
                sql = "INSERT INTO `Player` (`" +cols + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
                cursor.execute(sql, tuple(row))
            
                # the connection is not autocommitted by default, so we must commit to save our changes
                db.commit()
                
            print("Table import complete!")
                        
    except:
        
        print("Error while connecting to MySQL")
        
    finally:
        
        db.close()
        
        print("Connection closed")
        
        

players = pd.read_csv('player_db.csv')

upload_players(players)