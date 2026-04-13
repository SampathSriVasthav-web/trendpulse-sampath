import json
import csv
import os

input_file = "data/trends_20260412.json"
output_file = "data/trends_clean.csv"

if not os.path.exists(input_file):
    print("File not found")
    exit()

with open(input_file, "r") as f:
    records = json.load(f)

print(f"Loaded {len(records)} stories from {input_file}")

cleaned_data = []
seen_ids = set()

# remove duplicates
for item in records:
    post_id = item.get("post_id")
    if post_id in seen_ids:
        continue
    seen_ids.add(post_id)
    cleaned_data.append(item)

print("After removing duplicates:", len(cleaned_data))

# remove missing values
cleaned_data = [
    i for i in cleaned_data
    if i.get("post_id") and i.get("title") and i.get("score") is not None
]

print("After removing nulls:", len(cleaned_data))

# clean + filter low score
final_data = []
for i in cleaned_data:
    try:
        score = int(i.get("score", 0))
        comments = int(i.get("num_comments", 0))

        if score < 5:
            continue

        final_data.append({
            "post_id": i.get("post_id"),
            "title": i.get("title").strip(),
            "category": i.get("category"),
            "score": score,
            "num_comments": comments,
            "author": i.get("author"),
            "collected_at": i.get("collected_at")
        })

    except:
        continue

print("After removing low scores:", len(final_data))

# save CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=final_data[0].keys())
    writer.writeheader()
    writer.writerows(final_data)

print(f"Saved {len(final_data)} rows to {output_file}")

# category summary
category_count = {}
for i in final_data:
    cat = i["category"]
    category_count[cat] = category_count.get(cat, 0) + 1

print("\nStories per category:")
for k, v in category_count.items():
    print(k, v)
