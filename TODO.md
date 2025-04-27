

### **Set Up Your Cron Job**
1. **Open your crontab file** (task scheduler):
   ```bash
   crontab -e
   ```

2. **Add this line** (customize paths):
   ```bash
   # Run scraper daily at noon
   0 12 * * * /usr/bin/python3 /path/to/indie-game-scraper/scraper.py >> /home/user/scraper.log 2>&1
   ```
   - `>> scraper.log` saves output to a log file
   - `2>&1` captures errors too
  - **Use absolute paths**:
     - Find your Python path:
       ```bash
       which python3  # Usually /usr/bin/python3
       ```

---

### **Step 3: Verify**
- **List active cron jobs**:
  ```bash
  crontab -l
  ```

- **Check logs**:
  ```bash
  tail -f scraper.log
  ```

---

`generate_report.py` creates a markdown summary

### Report Preview:

```markdown
# Daily Indie Game Report - 2023-10-27

## New Releases: 42 games

### Trending Tags
| Tag          | Count |
|--------------|-------|
| Horror       | 12    |
| Pixel Art    | 9     |
| RPG          | 7     |

### Notable Releases
| Title               | Developer       | Tags                          |
|---------------------|-----------------|-------------------------------|
| Space Quest         | Cosmic Dev      | [RPG, Space, Adventure]       |
| Haunted Mansion     | Spooky Studios  | [Horror, Puzzle, Atmospheric] |
```

---

**Discord Bot**: Post updates to a private Discord channel.
