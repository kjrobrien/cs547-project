import json
import pandas as pd
import matplotlib.pyplot as plt


with open('switch_games.json', 'r') as file:
    data = json.load(file)

print("Hello World")
print("Length: ", len(data))
print("Keys Length: ", len(data[0].keys()))
''
'id', 'age_ratings', 'alternative_names', 'artworks', 'category', 'cover', 'created_at',
'external_games', 'first_release_date', 'game_modes', 'genres', 'involved_companies',
'name', 'platforms', 'rating', 'rating_count', 'release_dates', 'screenshots', 'similar_games',
'slug', 'summary', 'tags', 'total_rating', 'total_rating_count', 'updated_at', 'url', 'websites',
'checksum', 'language_supports', 'game_localizations'
''
print("Keys: ", data[0].keys())

print("==================")
df = pd.DataFrame(data)
df = df.dropna(subset=['rating'])
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
labels = ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-100"]
# print("df[rating]: ", df['rating'])
df['rating_range'] = pd.cut(df['rating'], bins=bins, labels=labels, right=False)
rating_counts = df['rating_count'].value_counts().sort_index()
print("len of rating_counts: ", len(rating_counts))


