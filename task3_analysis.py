import pandas as pd
import os

file_path = "data/cleaned_trends.csv"

# check file
if not os.path.exists(file_path):
    print("CSV file not found")
    exit()

# load data
df = pd.read_csv(file_path)

# basic info
print("Total records:", len(df))

# top 5 highest score posts
top_scores = df.sort_values(by="score", ascending=False).head(5)
print("\nTop 5 by score:\n", top_scores[["title", "score"]])

# most commented posts
top_comments = df.sort_values(by="num_comments", ascending=False).head(5)
print("\nTop 5 by comments:\n", top_comments[["title", "num_comments"]])

# category count
category_count = df["category"].value_counts()
print("\nStories per category:\n", category_count)

# average score per category
avg_score = df.groupby("category")["score"].mean()
print("\nAverage score per category:\n", avg_score)

# save analysis
output_file = "data/analysis_results.csv"
avg_score.to_csv(output_file)

print(f"\nAnalysis saved to {output_file}")