import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = "data/cleaned_trends.csv"

# check file exists
if not os.path.exists(file_path):
    print("CSV file not found")
    exit()

# load data
data = pd.read_csv(file_path)

# 1. Category count bar chart
category_counts = data["category"].value_counts()

plt.figure()
category_counts.plot(kind="bar")
plt.title("Number of Stories per Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()

if not os.path.exists("data"):
    os.makedirs("data")

plt.savefig("data/category_distribution.png")
plt.close()


# 2. Top 10 scores chart
top_scores = data.sort_values(by="score", ascending=False).head(10)

plt.figure()
plt.barh(top_scores["title"], top_scores["score"])
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Title")
plt.tight_layout()

plt.savefig("data/top_scores.png")
plt.close()


# 3. Comments vs Score scatter plot
plt.figure()
plt.scatter(data["num_comments"], data["score"])
plt.title("Comments vs Score")
plt.xlabel("Number of Comments")
plt.ylabel("Score")
plt.tight_layout()

plt.savefig("data/comments_vs_score.png")
plt.close()

print("Visualizations saved in data/ folder")