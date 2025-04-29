
## Use Cases
- **Discover New Games**: Track daily releases automatically.
- **Trend Analysis**: Identify trending genres (e.g., "horror", "roguelike") from tags.
- **Content Curation**: Power newsletters, blogs, or social media feeds highlighting new indie games with fresh game data.
- **Integration**: Feed data into APIs, or databases.

---

**Discord Bot**: Post updates to a private Discord channel.

---

**API Testing with cURL**

```bash
curl -X POST -H "Content-Type: application/json" \
     -d @data/latest.json \
     http://localhost:8000/games/
```