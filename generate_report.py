import datetime
import glob
import os
import sys

try:
	import pandas as pd
except ImportError:
	print("Error: generate_report.py requires pandas.")
	print("Install it with: pip install pandas")
	sys.exit(1)

def create_daily_summary():
	latest_file = max(glob("data/indie_games_*.csv"), key=os.path.getctime)
	df = pd.read_csv(latest_file)

	# Top Tags Today
	all_tags = [tag for sublist in df['tags'].apply(eval) for tag in sublist]
	top_tags = pd.Series(all_tags).value_counts().head(5)

	# Price Distribution
	price_stats = df['price'].value_counts()

	# Generate Markdown report
	report = f"""
	          # Daily Indie Game Report - {datetime.today().strftime('%Y-%m-%d')}
	          
	          ## New Releases: {len(df)} games
	          
	          ### Trending Tags
	          {top_tags.to_markdown()}
	          
	          ### Price Distribution
	          {price_stats.to_markdown()}
	          
	          ### Releases
	          {df[['title', 'developer', 'tags']].to_markdown(index=False)}
	          """

	with open(f"reports/daily_report_{today}.md", "w") as f:
		f.write(report)
