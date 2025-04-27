import os
import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import random
from datetime import datetime

# Configuration
BASE_URL = "https://itch.io/games/newest/last-day?page="
HEADERS = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_CSV = f"data/indie_games_{timestamp}.csv"
OUTPUT_JSON = f"data/indie_games_{timestamp}.json"

# Rate limiting controls
PAGE_DELAY = 5 # Seconds between page requests
GAME_DELAY = 3 # Base seconds between game detail requests

def get_game_details(game_url):
	"""Scrape additional details from individual game page"""
	try:
		response = requests.get(game_url, headers=HEADERS)
		response.raise_for_status()
		print(f"Scraping game details from {game_url}...")
		soup = BeautifulSoup(response.text, 'html.parser')

		# Find the game info panel
		info_panel = soup.find('div', class_='game_info_panel_widget')
		if not info_panel:
			return None, []

		# Extract published date
		published_date = info_panel.select_one('abbr') 
		published_date = published_date["title"] if published_date else None

		# Extract tags
		tags = []
		# Find the Tags row in the table
		for row in info_panel.select('tr'):
			cells = row.find_all('td')
			if cells[0].text.strip().lower() == 'tags':
				# Extract all <a> tags in the second cell
				tags = [a.text.strip() for a in cells[1].find_all('a')]
				break

		return published_date, tags

	except Exception as e:
		return None, []


def scrape_indie_games():
	games = []
	page = 1

	while True:
		try:
			url = f"{BASE_URL}{page}"
			print(f"Scraping page {page}...") 
			response = requests.get(url, headers=HEADERS)
			response.raise_for_status()
			soup = BeautifulSoup(response.text, "html.parser")

			# Check for termination conditions
			no_results = soup.select_one("div.empty_message")
			game_cells = soup.select("div.game_cell")
			if no_results or not game_cells:
				print("No more games found. Ending scrape.")
				break

			# Extract game data
			for game_cell in game_cells:
				# Extract data from each game cell
				title = game_cell.select_one(".game_title a").text.strip()
				print(f"Scraping game: {title}")
				developer = game_cell.select_one(".game_author").text.strip()
				url = game_cell.select_one(".game_title a")["href"]
				published_date, tags = get_game_details(url)
				if game_cell.select_one(".price_value"):
					price = game_cell.select_one(".price_value").text.strip()
				else:
					price = None
				if game_cell.select_one(".game_genre"):
					genre = game_cell.select_one(".game_genre").text.strip()
				else:
					genre = None
				if game_cell.select_one(".game_text"): 
					description = game_cell.select_one(".game_text").text.strip()
				else:
					description = None

				games.append({
					"title": title,
					"developer": developer,
					"url": url,
					"published_date": published_date,
					"price": price,
					"genre": genre,
					"description": description,
					"tags": tags
				})
				print(f"finished extracting game data from {url}")
				time.sleep(GAME_DELAY + random.uniform(0, 1)) # Randomized delay

			page += 1
			time.sleep(PAGE_DELAY + random.uniform(0, 2)) # Randomized page delay

		except requests.exceptions.HTTPError as e:
			if e.response.status_code == 429:
				wait_time = 60 # Wait 1 minute for rate limit reset
				print(f"Rate limited! Waiting {wait_time} seconds")
				time.sleep(wait_time)
			else:
				print(f"HTTP error: {e}")
				break
		except Exception as e:
			print(f"Fatal error: {e}")
			break




	# Export data if games found
	if games:
		save_data(games)
	else:
		print("No games scraped.")

def save_data(games):
	# Create directory if needed
	os.makedirs("data", exist_ok=True)

	# Export to CSV
	with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=games[0].keys())
		writer.writeheader()
		writer.writerows(games)

	# Export to JSON
	with open(OUTPUT_JSON, "w", encoding="utf-8") as jsonfile:
		json.dump(games, jsonfile, ensure_ascii=False, indent=2)

	print(f"Successfully exported {len(games)} games to {OUTPUT_CSV} and {OUTPUT_JSON}")

if __name__ == "__main__":
	scrape_indie_games()
