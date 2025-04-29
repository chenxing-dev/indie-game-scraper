import sqlite3
import json

def create_table():
    conn = sqlite3.connect('indie_games.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS games
                (title TEXT, developer TEXT, url TEXT PRIMARY KEY, 
                 published_date TEXT, price TEXT, tags TEXT)''')
    conn.commit()
    conn.close()

def insert_games(games):
    conn = sqlite3.connect('indie_games.db')
    c = conn.cursor()
    
    for game in games:
        try:
            c.execute('''INSERT INTO games VALUES 
                        (:title, :developer, :url, 
                         :published_date, :price, :tags)''', 
                      game)
        except sqlite3.IntegrityError:
            pass  # Skip duplicates
    conn.commit()
    conn.close()

# Usage
with open('data/latest.json') as f:
    games = json.load(f)
    create_table()
    insert_games(games)