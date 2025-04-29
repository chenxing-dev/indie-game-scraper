from datetime import datetime
from glob import glob
import os
import sys
from pathlib import Path

try:
	import pandas as pd
except ImportError:
	print("Error: generate_report.py requires pandas and tabulate.")
	print("Install it with: pip install pandas tabulate")
	sys.exit(1)
except ModuleNotFoundError:
	print("Error: generate_report.py requires pandas and tabulate.")
	print("Install it with: pip install pandas tabulate")
	sys.exit(1)

def escape_markdown(text):
	"""Escape special Markdown characters in text"""
	if not isinstance(text, str):
		return text
	# Escape special Markdown characters
	for char in ['|', '\\', '`', '*', '_', '{', '}', '[', ']', '(', ')']:
		text = text.replace(char, f'\\{char}')
	return text

def create_daily_summary():
	# Get today's date
	today_date = datetime.today().strftime("%Y%m%d")

	# Get newest CSV file
	csv_files = glob("data/indie_games_*.csv")
	if not csv_files:
		print("Error: No CSV files found in data/ directory")
		return

	latest_file = max(csv_files, key=os.path.getctime)
	df = pd.read_csv(latest_file)

	# Clean and escape all text fields
	df['title'] = df['title'].apply(escape_markdown)
	df['developer'] = df['developer'].apply(escape_markdown)

	# Top Tags Today
	all_tags = [tag for sublist in df['tags'].apply(eval) for tag in sublist]
	top_tags = (
		pd.Series(all_tags)
		.value_counts()
		.head(5)
		.reset_index() # Convert to DataFrame
		.rename(columns={'index': 'Tag', 'count': 'Count'})
)

	# Price Distribution
	df['price'] = df['price'].fillna('Free') # Replace null with 'Free'
	price_stats = (
		df['price']
		.value_counts()
		.head(5)
		.reset_index()
		.rename(columns={'price': 'Price', 'count': 'Count'})
)

	# Generate Markdown report
	report = f"# Daily Indie Game Report - {today_date}\n"
	report += f"## Total Games: {len(df)}\n"
	report += f"### Trending Tags\n{top_tags.to_markdown(index=False)}\n"
	report += f"### Price Distribution\n{price_stats.to_markdown(index=False)}\n"
	report += f"### Releases\n{
		df[['title', 'developer', 'tags', 'url']]
		.assign(
        title=lambda x: x.apply(
            lambda row: f"[{row['title']}]({row['url']})", 
            axis=1
        ),
        tags=lambda x: x['tags'].apply(
            lambda y: ', '.join(eval(y)) if pd.notna(y) else ''
        ).apply(escape_markdown)
    )
    .drop(columns=['url'])
		.rename(columns={'title': 'Title', 'developer': 'Developer', 'tags': 'Tags'})
		.to_markdown(index=False)
		}"

	report_path = Path("reports") / f"daily_report_{today_date}.md"
	report_path.parent.mkdir(exist_ok=True)

	with open(report_path, "w", encoding="utf-8") as f:
		f.write(report)

	print(f"Report generated: {report_path}")

if __name__ == "__main__":
	create_daily_summary()
