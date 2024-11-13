import json
import pandas as pd
import matplotlib.pyplot as plt


with open('all_switch_games.json', 'r') as file:
    data = json.load(file)

print("==================")
df1 = pd.DataFrame(data)
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

plt.figure(figsize=(10,6))
plt.bar(rating_counts.index, rating_counts.values, color='skyblue')
plt.xlabel('Rating Range')
plt.ylabel('Number of Items')
plt.title('Distribution of Items by Rating Ranges')

plt.tight_layout()
plt.show()

# Plots by aggregated rating
dfAggregatedRating['rating_range'] = pd.cut(dfAggregatedRating['aggregated_rating'], bins=bins, labels=labels, right=False)
aggregatedRating_counts = dfAggregatedRating['rating_range'].value_counts().reindex(labels).fillna(0)

plt.figure(figsize=(10,6))
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
for game in sorted_games['name']:
    print("Game: ", game)

gamesAggregated_in_90_100 = dfAggregatedRating[dfAggregatedRating['rating_range'] == '90-100']
aggregatedSorted_games = gamesAggregated_in_90_100.sort_values(by='rating', ascending=False)
print("\n Games in the 90-100 aggregated rating range")
for game in sorted_games['name']:
    print("Game: ", game)




