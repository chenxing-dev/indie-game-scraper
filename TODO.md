

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
