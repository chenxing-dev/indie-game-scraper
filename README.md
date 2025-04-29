# Indie Game News Scraper 🕹️

A Python web scraper that extracts the latest indie game releases from [itch.io](https://itch.io/games/new) and exports structured data to CSV/JSON. Ideal for tracking trends, curating newsletters, or analyzing the indie game market.

---

## Features
- Scrapes game **title, developer, URL, published date, genre, tags, and description**.
- Exports data to both `CSV` and `JSON` formats.

## Installation

1. **Clone the repository**:
```bash
git clone https://github.com/chenxing-dev/indie-game-scraper.git
cd indie-game-scraper
```

2. **Install dependencies**:
```bash
pip install requests beautifulsoup4
```

## Usage

### Basic Execution

Execute the script to fetch the latest games:
   ```bash
   python scraper.py
   ```

Output files (`indie_games_YYYYMMDD_HHMMSS.csv` and `indie_games_YYYYMMDD_HHMMSS.json`) will be generated in the `data` directory.


### Scheduled Scraping
To collect data periodically, use a cron job. Example cron job (runs daily at noon):
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

## Output Example

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

## Use Cases
- **Discover New Games**: Track daily releases automatically.
- **Trend Analysis**: Identify trending genres (e.g., "horror", "roguelike") from tags.
- **Content Curation**: Power newsletters, blogs, or social media feeds highlighting new indie games with fresh game data.
- **Integration**: Feed data into APIs, or databases.

## Disclaimer
This script is for educational purposes only. 

## License
MIT License. See [LICENSE](LICENSE).
