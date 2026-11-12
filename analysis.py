"""
Netflix Movies and TV Shows - Data Visualization Project
Author: <your name>

What this program does, in order:
  1. Loads the Netflix dataset (a CSV file)
  2. Cleans it (missing values, dates, duration)
  3. Draws 6 charts and saves them in the img/ folder
  4. Prints the key findings in the terminal

Run from the project folder:   python analysis.py
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------------
# STEP 0: Settings (colours and chart style are decided once, here)
# ----------------------------------------------------------------------
RED = "#e50914"      # Netflix red
DARK = "#221f1f"     # Netflix dark grey
sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 120
os.makedirs("img", exist_ok=True)    # create the img folder if it is missing

# ----------------------------------------------------------------------
# STEP 1: Load the data
# ----------------------------------------------------------------------
df = pd.read_csv("data/netflix_titles.csv")

print("Rows and columns:", df.shape)
print("\nColumn names:", list(df.columns))
print("\nMissing values in each column:")
print(df.isnull().sum())

# ----------------------------------------------------------------------
# STEP 2: Clean the data
# ----------------------------------------------------------------------
df = df.drop_duplicates()

# Text columns: replace missing values with the word "Unknown"
for col in ["director", "cast", "country", "rating"]:
    df[col] = df[col].fillna("Unknown")

# date_added is text like "September 25, 2021" -> convert to a real date
df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
df["year_added"] = df["date_added"].dt.year

# duration is text: "90 min" for movies, "2 Seasons" for TV shows.
# Take the number out so we can draw a histogram for movies.
df["duration_num"] = pd.to_numeric(df["duration"].str.extract(r"(\d+)")[0],
                                   errors="coerce")
movies = df[df["type"] == "Movie"]
shows = df[df["type"] == "TV Show"]

# ----------------------------------------------------------------------
# CHART 1: Movies vs TV Shows (pie chart - parts of a whole)
# ----------------------------------------------------------------------
counts = df["type"].value_counts()
plt.figure(figsize=(5, 5))
wedges, labels_, pct_texts = plt.pie(
    counts, labels=counts.index, autopct="%1.1f%%",
    colors=[RED, DARK], startangle=90,
    textprops={"fontsize": 12})
for t in pct_texts:                  # percentages sit inside the slices: white
    t.set_color("white")
plt.title("Movies vs TV Shows on Netflix")
plt.savefig("img/chart1_movies_vs_shows.png", bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# CHART 2: Content added per year (line chart - change over time)
# ----------------------------------------------------------------------
per_year = df.groupby(["year_added", "type"]).size().unstack(fill_value=0)
per_year.plot(kind="line", marker="o", color=[RED, DARK], figsize=(8, 4))
plt.title("Titles added to Netflix each year")
plt.xlabel("Year added")
plt.ylabel("Number of titles")
plt.savefig("img/chart2_added_per_year.png", bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# CHART 3: Top 10 genres (bar chart - compare categories)
# A title can have many genres in one cell: "Dramas, International Movies"
# so we split the text and give each genre its own row (explode).
# ----------------------------------------------------------------------
genres = df["listed_in"].str.split(", ").explode()
top_genres = genres.value_counts().head(10)
plt.figure(figsize=(8, 4.5))
sns.barplot(x=top_genres.values, y=top_genres.index, color=RED)
plt.title("Top 10 genres on Netflix")
plt.xlabel("Number of titles")
plt.ylabel("")
plt.savefig("img/chart3_top_genres.png", bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# CHART 4: Top 10 countries (bar chart) - same split trick as genres
# ----------------------------------------------------------------------
countries = df["country"].str.split(", ").explode()
countries = countries[countries != "Unknown"]
top_countries = countries.value_counts().head(10)
plt.figure(figsize=(8, 4.5))
sns.barplot(x=top_countries.values, y=top_countries.index, color=DARK)
plt.title("Top 10 countries producing Netflix content")
plt.xlabel("Number of titles")
plt.ylabel("")
plt.savefig("img/chart4_top_countries.png", bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# CHART 5: Audience ratings (bar chart)
# ----------------------------------------------------------------------
rating_counts = df["rating"].value_counts().head(8)
plt.figure(figsize=(8, 4))
sns.barplot(x=rating_counts.index, y=rating_counts.values, color=RED)
plt.title("Most common content ratings")
plt.xlabel("Rating")
plt.ylabel("Number of titles")
plt.savefig("img/chart5_ratings.png", bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# CHART 6: Movie length (histogram - how values are spread)
# ----------------------------------------------------------------------
plt.figure(figsize=(8, 4))
plt.hist(movies["duration_num"].dropna(), bins=30, color=RED, edgecolor="white")
plt.axvline(movies["duration_num"].mean(), color=DARK, linestyle="--")
plt.title("How long are Netflix movies? (minutes)")
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of movies")
plt.savefig("img/chart6_movie_duration.png", bbox_inches="tight")
plt.close()

# ----------------------------------------------------------------------
# STEP 4: Print the key findings (use these in README, LinkedIn, viva)
# ----------------------------------------------------------------------
print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)
print(f"Total titles        : {len(df)}")
print(f"Movies              : {len(movies)} ({len(movies) / len(df) * 100:.1f}%)")
print(f"TV Shows            : {len(shows)} ({len(shows) / len(df) * 100:.1f}%)")
print(f"Most common genre   : {top_genres.index[0]} ({top_genres.iloc[0]} titles)")
print(f"Top country         : {top_countries.index[0]} ({top_countries.iloc[0]} titles)")
print(f"Busiest year        : {int(per_year.sum(axis=1).idxmax())}")
print(f"Average movie length: {movies['duration_num'].mean():.0f} minutes")
print(f"Most common rating  : {rating_counts.index[0]}")
print("\nSaved 6 charts in the img/ folder.")
