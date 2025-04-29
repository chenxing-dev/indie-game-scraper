# Indie Game News Scraper 🕹️

A Python web scraper that extracts the latest indie game releases from [itch.io](https://itch.io/games/new) and exports structured data to CSV/JSON. Ideal for tracking trends, curating newsletters, or analyzing the indie game market.

## Features
- Scrapes game **title, developer, URL, published date, genre, tags, and description**.
- **Output Formats**: CSV, JSON, SQLite

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/chenxing-dev/indie-game-scraper.git
cd indie-game-scraper
pip install -r requirements.txt  # requests, beautifulsoup4
```

## Usage

### 1. Core Scraping

Execute the script to fetch the latest games:
   ```bash
   python scraper.py
   ```

Output files (`indie_games_YYYYMMDD_HHMMSS.csv` and `indie_games_YYYYMMDD_HHMMSS.json`) will be generated in the `data/` directory.


#### Scheduled Scraping
To collect data periodically, use a cron job. Example cron job (runs daily at 9pm):
```bash
0 21 * * * cd /path/to/indie-game-scraper && venv/bin/python scraper.py >> scraper.log 2>&1
```

- `>> scraper.log` saves output to a log file
- `2>&1` captures errors too
- **Use absolute paths**:
     - Find your Python path:
```bash
which python
```

#### Output Example

**JSON Fields**:
```json
{
    "title": "Playtesters and Co.",
    "developer": "SeeOne",
    "url": "https://seeone.itch.io/playtesters-and-co",
    "published_date": "26 April 2025 @ 14:32 UTC",
    "price": null,
    "genre": "Puzzle",
    "description": "Balance, A game dev's worst enemy.",
    "tags": [
      "2D",
      "Creepy",
      "Mystery",
      "Pixel Art",
      "Retro",
      "Singleplayer"
    ]
  }
```

### 2. Optional Report Generation
```bash
# Install dependencies
pip install pandas tabulate

# Generate daily summary report
python generate_report.py
```
**Output**: `reports/daily_report_YYYY-MM-DD.md`  

### 3. Database Setup
```bash
# Create database and import latest CSV
python database.py
```
Creates/Updates: `indie_games.db`

### 4. Query Data
```bash
# Get latest 5 releases
python query.py

# Sample output:
# 28 April 2025 @ 07:08 UTC | Shoot by TheChainsawBoy
# 28 April 2025 @ 07:05 UTC | Su-no-ku by ObeseTermite
# 28 April 2025 @ 07:04 UTC | Unstoppable Piko by Severus Prince
# 28 April 2025 @ 07:03 UTC | Lucky Fighter EX Plus Ika by Takishi Usada
# 28 April 2025 @ 06:58 UTC | Speedy Stapler by Shylencce
```

## File Structure
```
indie-game-scraper/
├── data/               # Scraped data (CSV/JSON)
├── reports/            # Generated reports
├── indie_games.db      # SQLite database
├── scraper.py          # Main scraper
├── database.py         # DB management
├── query.py            # Example queries
└── generate_report.py  # Reports (optional)
```

## Disclaimer
This script is for educational purposes only. 

## License
MIT License. See [LICENSE](LICENSE).
