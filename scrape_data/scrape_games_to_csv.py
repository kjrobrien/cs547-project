import json
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

with open('all_switch_games.json', 'r') as file:
    games = json.load(file)

def countByKey(games, key):
    enums = []
    for game in games:
        try:
            val = game[key]
            if isinstance(val, int):
                val = [val]
            enums.extend(val)
        except KeyError as e:
            pass
    counter = Counter(enums)
    return counter


def plotGraphsByKey(counter, key):
    counterKeys = list(counter.keys())
    counterValues = list(counter.values())

    if key == "genres":
        # sortedGenre = genreCounts.most_common()
        # for genre, count in sortedGenre:
        #     print("Genre (Enum): ", genre)
        #     print("Count : ", count)
        plt.figure(figsize=(10, 6))
        plt.bar(counterKeys, counterValues, color='skyblue')
        plt.xlabel('Genre (Enum)')
        plt.ylabel('Number of Games')
        plt.title('Number of Games per Genre')
        plt.xticks(counterKeys)
        plt.tight_layout()
        plt.show()

    elif key == "franchises":
        # sortedGenre = counter.most_common()
        # for genre, count in sortedGenre:
        #     print("Franchises (Enum): ", genre)
        #     print("Count : ", count)
        plt.figure(figsize=(10, 6))
        plt.bar(counterKeys, counterValues, color='skyblue')
        plt.xlabel('Franchises (Enum)')
        plt.ylabel('Number of Games')
        plt.title('Number of Games per Franchises')
        plt.xticks(counterKeys)
        plt.tight_layout()
        plt.show()

    elif key == "game_engines":
        # sortedGenre = counter.most_common()
        # for genre, count in sortedGenre:
        #     print("Game Engines (Enum): ", genre)
        #     print("Count : ", count)
        plt.figure(figsize=(10, 6))
        plt.bar(counterKeys, counterValues, color='skyblue')
        plt.xlabel('Game Engines (Enum)')
        plt.ylabel('Number of Games')
        plt.title('Number of Games per Game Engines')
        plt.xticks(counterKeys)
        plt.tight_layout()
        plt.show()

    elif key == "game_modes":
        # sortedGenre = counter.most_common()
        # for genre, count in sortedGenre:
        #     print("Game Modes (Enum): ", genre)
        #     print("Count : ", count)
        plt.figure(figsize=(10, 6))
        plt.bar(counterKeys, counterValues, color='skyblue')
        plt.xlabel('Game Modes (Enum)')
        plt.ylabel('Number of Games')
        plt.title('Number of Games per Game Modes')
        plt.xticks(counterKeys)
        plt.tight_layout()
        plt.show()

    elif key == "player_perspectives":
        # sortedGenre = counter.most_common()
        # for genre, count in sortedGenre:
        #     print("Game Player Perspectives (Enum): ", genre)
        #     print("Count : ", count)
        plt.figure(figsize=(10, 6))
        plt.bar(counterKeys, counterValues, color='skyblue')
        plt.xlabel('Game Player Perspectives (Enum)')
        plt.ylabel('Number of Games')
        plt.title('Number of Games per Player Perspective')
        plt.xticks(counterKeys)
        plt.tight_layout()
        plt.show()

    elif key == "themes":
        # sortedGenre = counter.most_common()
        # for genre, count in sortedGenre:
        #     print("Game Themes (Enum): ", genre)
        #     print("Count : ", count)
        plt.figure(figsize=(10, 6))
        plt.bar(counterKeys, counterValues, color='skyblue')
        plt.xlabel('Game Themes (Enum)')
        plt.ylabel('Number of Games')
        plt.title('Number of Games per Themes')
        plt.xticks(counterKeys)
        plt.tight_layout()
        plt.show()

graphKeys = ["genres", "franchises", "game_engines", "game_modes", "player_perspectives", "themes"]
for gKeys in graphKeys:
    counterByKey = countByKey(games, gKeys)
    plotGraphsByKey(counterByKey, gKeys)

print("==================")
df1 = pd.DataFrame(games)
print("length df: ", len(df1))
dfRating = df1.dropna(subset=['rating'])
dfAggregatedRating = df1.dropna(subset=['aggregated_rating'])
print("length df rating: ", len(dfRating))
print("length df aggregated rating: ", len(dfAggregatedRating))

bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100"]

# Plot by rating
dfRating['rating_range'] = pd.cut(dfRating['rating'], bins=bins, labels=labels, right=False)
rating_counts = dfRating['rating_range'].value_counts().reindex(labels).fillna(0)

plt.figure(figsize=(10, 6))
plt.bar(rating_counts.index, rating_counts.values, color='skyblue')
plt.xlabel('Rating Range')
plt.ylabel('Number of Items')
plt.title('Distribution of Items by Rating Ranges')

plt.tight_layout()
plt.show()

# Plots by aggregated rating
dfAggregatedRating['rating_range'] = pd.cut(dfAggregatedRating['aggregated_rating'], bins=bins, labels=labels,
                                            right=False)
aggregatedRating_counts = dfAggregatedRating['rating_range'].value_counts().reindex(labels).fillna(0)

plt.figure(figsize=(10, 6))
plt.bar(aggregatedRating_counts.index, aggregatedRating_counts.values, color='skyblue')
plt.xlabel('Aggregated Rating Range')
plt.ylabel('Number of Items')
plt.title('Distribution of Items by Aggregated Rating Ranges')

plt.tight_layout()
plt.show()

# Get the names of the games with highest rating
games_in_90_100 = dfRating[dfRating['rating_range'] == '90-100']
sorted_games = games_in_90_100.sort_values(by='rating', ascending=False)
print("Games in the 90-100 rating range")
count = 0
for _, game in sorted_games.iterrows():
    print("Game: ", game['name'], " Score: ", game['rating'])
    count += 1
    if count == 5:
        break

games_in_10_20 = dfRating[dfRating['rating_range'] == '10-20']
sorted_games = games_in_10_20.sort_values(by='rating', ascending=True)
print("\nWorst games in the rating range")
count = 0
for _, game in sorted_games.iterrows():
    print("Game: ", game['name'], " Score: ", game['rating'])
    count += 1
    if count == 5:
        break

gamesAggregated_in_90_100 = dfAggregatedRating[dfAggregatedRating['rating_range'] == '90-100']
aggregatedSorted_games = gamesAggregated_in_90_100.sort_values(by='aggregated_rating', ascending=False)
print("\nGames in the 90-100 aggregated rating range")
count = 0
for _, game in aggregatedSorted_games.iterrows():
    print("Game: ", game['name'], " Score: ", game['aggregated_rating'])
    count += 1
    if count == 5:
        break

gamesAggregated_in_0_10 = dfAggregatedRating[dfAggregatedRating['rating_range'] == '0-10']
aggregatedSorted_games = gamesAggregated_in_0_10.sort_values(by='aggregated_rating', ascending=True)
print("\nWorst games in the aggregated rating range")
count = 0
for _, game in aggregatedSorted_games.iterrows():
    print("Game: ", game['name'], " Score: ", game['aggregated_rating'])
    count += 1
    if count == 5:
        break
