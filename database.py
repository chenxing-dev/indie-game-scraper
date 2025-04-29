import sqlite3
import csv
from pathlib import Path


def create_table():
	# Connect to SQLite database (creates if not exists)
	conn = sqlite3.connect('indie_games.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS games
	          (title TEXT, 
	           developer TEXT, 
	           url TEXT PRIMARY KEY, 
	           published_date DATETIME, 
	           price TEXT, 
	           tags TEXT,
	           description TEXT)''')

	conn.commit()
	conn.close()
	print("Created indie_games.db with 'games' table")

def import_from_csv(csv_path):
	conn = sqlite3.connect('indie_games.db')
	c = conn.cursor()

	with open(csv_path, 'r', encoding='utf-8') as f:
		reader = csv.DictReader(f)
		for row in reader:
			# Insert or ignore duplicates based on URL
			c.execute('''INSERT OR IGNORE INTO games VALUES 
			          (:title, :developer, :url, 
			           :published_date, :price, :tags, :description)''', row)

	conn.commit()
	print(f"Imported {conn.total_changes} rows from {csv_path}")
	conn.close()

def get_latest_csv():
	data_dir = Path('data')
	csv_files = list(data_dir.glob('indie_games_*.csv'))
	if not csv_files:
		return None
	return max(csv_files, key=lambda f: f.stat().st_birthtime)

if __name__ == "__main__":
	create_table()
	latest_csv = get_latest_csv()

	if latest_csv:
		import_from_csv(latest_csv)
	else:
		print("No CSV files found in data/ directory")
