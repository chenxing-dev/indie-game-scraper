import sqlite3

def query_games():
	conn = sqlite3.connect('indie_games.db')
	c = conn.cursor()

	# Get 5 latest games
	c.execute('''SELECT title, developer, published_date 
	          FROM games 
	          ORDER BY published_date DESC 
	          LIMIT 10''')

	for row in c.fetchall():
		print(f"{row[2]} | {row[0]} by {row[1]}")

if __name__ == "__main__":
	query_games()
