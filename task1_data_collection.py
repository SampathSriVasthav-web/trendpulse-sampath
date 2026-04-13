import requests
import time
import json
from datetime import datetime
import os

TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
DETAIL_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# full keywords (IMPORTANT)
category_map = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "api", "cloud", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

def assign_category(title):
    text = title.lower()
    for cat, words in category_map.items():
        if any(word in text for word in words):
            return cat
    return None


stories = []

try:
    top_ids = requests.get(TOP_URL).json()
except:
    top_ids = []

count_per_category = {cat: 0 for cat in category_map}

# category-wise loop (IMPORTANT)
for category in category_map:
    for sid in top_ids:
        try:
            res = requests.get(DETAIL_URL.format(sid))
            if res.status_code != 200:
                continue

            item = res.json()
            if not item or "title" not in item:
                continue

            cat = assign_category(item["title"])
            if cat != category:
                continue

            if count_per_category[category] >= 25:
                break

            story = {
                "post_id": item.get("id"),
                "title": item.get("title"),
                "category": category,
                "score": item.get("score", 0),
                "num_comments": item.get("descendants", 0),
                "author": item.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            stories.append(story)
            count_per_category[category] += 1

        except:
            print("Error fetching story")

    # IMPORTANT sleep
    time.sleep(2)


# save file
if not os.path.exists("data"):
    os.makedirs("data")

file_name = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(file_name, "w") as f:
    json.dump(stories, f, indent=4)

print(f"Collected {len(stories)} stories. Saved to {file_name}")
