## Use Cases
- [x] **Discover New Games**: Track daily releases automatically.
- [ ] **Trend Analysis**: Identify trending genres (e.g., "horror", "roguelike") from tags.
- [x] **Integration**: Feed data into APIs, or databases.

---

Here's how to implement **trend analysis** for indie game genres/tags using your scraped data:

---

### **1. Trend Analysis Script (`trend_analysis.py`)**
```python
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def analyze_trends(window_days=30, top_n=10):
    """Identify trending tags over the last N days"""
    conn = sqlite3.connect('indie_games.db')
    
    # Get games from specified time window
    query = f'''
    SELECT published_data, tags 
    FROM games
    WHERE DATE(published_data) >= DATE('now', '-{window_days} days')
    '''
    df = pd.read_sql(query, conn)
    
    # Process tags and dates
    df['tags'] = df['tags'].apply(eval)
    df['release_week'] = pd.to_datetime(df['published_data']).dt.to_period('W')
    
    # Count tag frequencies per week
    weekly_tags = df.explode('tags').groupby(['release_week', 'tags']).size()
    weekly_tags = weekly_tags.reset_index(name='counts')
    
    # Calculate trend metrics
    trend_data = []
    for tag, group in weekly_tags.groupby('tags'):
        if len(group) < 2:  # Needs at least 2 data points
            continue
            
        # Calculate week-over-week growth
        latest = group.iloc[-1]['counts']
        previous = group.iloc[-2]['counts']
        growth_pct = ((latest - previous) / previous) * 100
        
        trend_data.append({
            'tag': tag,
            'current_week': latest,
            'previous_week': previous,
            'growth_pct': round(growth_pct, 1)
        })
    
    # Filter and sort trends
    trends_df = pd.DataFrame(trend_data)
    trends_df = trends_df[trends_df['current_week'] >= 5]  # Min 5 mentions
    trends_df = trends_df.sort_values('growth_pct', ascending=False).head(top_n)
    
    return trends_df

def generate_trend_report():
    trends = analyze_trends()
    
    # Create markdown table with emoji indicators
    report = ["# Trending Game Genres (Last 30 Days)",
              "| Tag | Current Week | Last Week | Growth | Trend |",
              "|-----|-------------:|----------:|-------:|------|"]
    
    for _, row in trends.iterrows():
        trend_emoji = "📈" if row['growth_pct'] > 0 else "📉"
        report.append(
            f"| {row['tag']} | {row['current_week']} | {row['previous_week']} | "
            f"{row['growth_pct']}% | {trend_emoji} |"
        )
    
    with open('reports/trend_report.md', 'w') as f:
        f.write('\n'.join(report))

if __name__ == "__main__":
    generate_trend_report()
```

---

### **2. Sample Output (`trend_report.md`)**
```markdown
# Trending Game Genres (Last 30 Days)
| Tag         | Current Week | Last Week | Growth | Trend |
|-------------|-------------:|----------:|-------:|------|
| Horror      | 142          | 89        | 59.5%  | 📈   |
| Roguelike   | 98           | 65        | 50.8%  | 📈   |
| Pixel Art   | 210          | 185       | 13.5%  | 📈   |
| Metroidvania| 45           | 52        | -13.5% | 📉   |
```

---

### **3. Usage**
```bash
# Generate trend report
python trend_analysis.py

# Custom analysis (60 days window, top 15 trends)
python trend_analysis.py --window 60 --top 15
```

---

