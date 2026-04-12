import requests
import time
import json
from datetime import datetime
import os

# API endpoints
TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
DETAIL_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulseApp/1.0"}

# category keywords
category_map = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "api"],
    "worldnews": ["war", "government", "country", "election", "climate", "global"],
    "sports": ["nfl", "nba", "fifa", "game", "team", "player"],
    "science": ["research", "study", "space", "physics", "nasa", "biology"],
    "entertainment": ["movie", "film", "music", "netflix", "show", "stream"]
}

# store collected stories
stories = []
count_per_category = {key: 0 for key in category_map}


# function to decide category
def assign_category(title):
    text = title.lower()
    for cat, words in category_map.items():
        if any(word in text for word in words):
            return cat
    return None


# fetch top IDs
try:
    response = requests.get(TOP_URL, headers=headers)
    response.raise_for_status()
    top_ids = response.json()[:500]
except Exception as e:
    print("Error fetching top stories:", e)
    top_ids = []


# loop through IDs
for sid in top_ids:
    try:
        res = requests.get(DETAIL_URL.format(sid), headers=headers)
        if res.status_code != 200:
            continue

        item = res.json()

        if not item or "title" not in item:
            continue

        cat = assign_category(item["title"])

        if not cat:
            continue

        # limit per category
        if count_per_category[cat] >= 25:
            continue

        # create dictionary
        story_data = {
            "post_id": item.get("id"),
            "title": item.get("title"),
            "category": cat,
            "score": item.get("score", 0),
            "num_comments": item.get("descendants", 0),
            "author": item.get("by"),
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        stories.append(story_data)
        count_per_category[cat] += 1

        # stop after enough stories
        if len(stories) >= 125:
            break

    except Exception as err:
        print("Skipping ID due to error:", err)


# create folder if not exists
if not os.path.exists("data"):
    os.makedirs("data")

# file name with date
file_name = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

# save JSON
with open(file_name, "w") as file:
    json.dump(stories, file, indent=4)

print(f"Collected {len(stories)} stories. Saved to {file_name}")