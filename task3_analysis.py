import pandas as pd
import numpy as np
import os

file_path = "data/trends_clean.csv"

if not os.path.exists(file_path):
    print("File not found")
    exit()

# load data
df = pd.read_csv(file_path)

# basic info
print("Loaded data:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

# averages
print("\nAverage score:", df["score"].mean())
print("Average comments:", df["num_comments"].mean())


# --- NumPy analysis ---
scores = df["score"].values

print("\n--- NumPy Stats ---")
print("Mean score:", np.mean(scores))
print("Median score:", np.median(scores))
print("Std deviation:", np.std(scores))
print("Max score:", np.max(scores))
print("Min score:", np.min(scores))

# most category
most_cat = df["category"].value_counts().idxmax()
count = df["category"].value_counts().max()
print(f"\nMost stories in: {most_cat} ({count} stories)")

# most commented story
top = df.loc[df["num_comments"].idxmax()]
print(f'Most commented story: "{top["title"]}" - {top["num_comments"]} comments')


# --- Add new columns ---
df["engagement"] = df["num_comments"] / (df["score"] + 1)

avg_score = df["score"].mean()
df["is_popular"] = df["score"] > avg_score


# save file
output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
