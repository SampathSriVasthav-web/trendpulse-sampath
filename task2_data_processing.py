import json
import csv
import os

# file paths
input_file = "data/trends_20260412.json"  # change date if needed
output_file = "data/cleaned_trends.csv"

# check file exists
if not os.path.exists(input_file):
    print("Input file not found")
    exit()

# read JSON data
with open(input_file, "r") as f:
    records = json.load(f)

cleaned_data = []
seen_ids = set()

for item in records:
    try:
        post_id = item.get("post_id")

        # skip duplicates
        if post_id in seen_ids:
            continue
        seen_ids.add(post_id)

        # clean fields
        title = item.get("title", "").strip()
        category = item.get("category", "unknown")
        score = item.get("score", 0)
        comments = item.get("num_comments", 0)
        author = item.get("author", "unknown")
        time = item.get("collected_at")

        # skip if title empty
        if not title:
            continue

        cleaned_data.append({
            "post_id": post_id,
            "title": title,
            "category": category,
            "score": score,
            "num_comments": comments,
            "author": author,
            "collected_at": time
        })

    except Exception as e:
        print("Error cleaning record:", e)

# write to CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=cleaned_data[0].keys())
    writer.writeheader()
    writer.writerows(cleaned_data)

print(f"Cleaned {len(cleaned_data)} records and saved to {output_file}")