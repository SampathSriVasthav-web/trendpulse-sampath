import pandas as pd
import matplotlib.pyplot as plt
import os

file_path = "data/trends_analysed.csv"

if not os.path.exists(file_path):
    print("File not found")
    exit()

df = pd.read_csv(file_path)

# create outputs folder
if not os.path.exists("outputs"):
    os.makedirs("outputs")


# shorten title
def short_title(t):
    return t[:50] + "..." if len(t) > 50 else t


# --- Chart 1: Top 10 stories ---
top10 = df.sort_values(by="score", ascending=False).head(10)
titles = top10["title"].apply(short_title)

plt.figure()
plt.barh(titles, top10["score"])
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.ylabel("Title")
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()


# --- Chart 2: Category count ---
counts = df["category"].value_counts()

plt.figure()
counts.plot(kind="bar")
plt.title("Stories per Category")
plt.xlabel("Category")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()


# --- Chart 3: Scatter ---
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.figure()
plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.title("Score vs Comments")
plt.xlabel("Score")
plt.ylabel("Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()


# --- BONUS Dashboard ---
fig, axs = plt.subplots(1, 3, figsize=(15, 5))

# chart1
axs[0].barh(titles, top10["score"])
axs[0].set_title("Top Stories")

# chart2
counts.plot(kind="bar", ax=axs[1])
axs[1].set_title("Categories")

# chart3
axs[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axs[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axs[2].set_title("Score vs Comments")

plt.suptitle("TrendPulse Dashboard")
plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("All charts saved in outputs/ folder")
