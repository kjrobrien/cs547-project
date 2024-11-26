import argparse
import pandas
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np


parser = argparse.ArgumentParser(description="Take a ratings CSV file a run collaborative filtering.")

parser.add_argument("--input", required=True, help="Input CSV file")
parser.add_argument("--game-slug", required=True, help="The game slug to get recommendations")
parser.add_argument("--num-recommendations", required=True, help="Number of recommendations")

args= parser.parse_args()

df = pandas.read_csv(args.input)

df = df.dropna()

train_df, test_df = train_test_split(df, test_size=0.2)

# Grab the user's highest rating for a game.
aggregated_df = train_df.groupby(['user_slug', 'game_slug']).rating.max().reset_index()

user_game_matrix = aggregated_df.pivot(index="user_slug", columns="game_slug", values="rating").fillna(0)

# Use pearson correlation for calculating similarity.
game_similarity_df = user_game_matrix.corr(method="pearson")

def predict_rating(user_slug, game_slug, similarity_df, user_game_matrix):
    if game_slug not in similarity_df.index:
        return np.nan
    
    if user_slug not in user_game_matrix.index:
        return np.nan
    
    similar_games = similarity_df[game_slug].drop(game_slug).dropna()
    
    user_ratings = user_game_matrix.loc[user_slug, similar_games.index].dropna()
    
    if user_ratings.empty:
        return np.nan
    
    return np.dot(user_ratings, similar_games[user_ratings.index]) / similar_games[user_ratings.index].sum()

test_df['predicted_rating'] = test_df.apply(
    lambda row: predict_rating(row['user_slug'], row['game_slug'], game_similarity_df, user_game_matrix),
    axis=1
)


test_df = test_df.dropna(subset=['predicted_rating'])

rmse = np.sqrt(mean_squared_error(test_df['rating'], test_df['predicted_rating']))

print(f"RMSE: {rmse}")


def get_top_similar(game_slug, similarity_df):
    similar = similarity_df[game_slug].sort_values(ascending=False)
    # Exclude the current game slug from the results
    similar = similar[similar.index != game_slug]
    return similar[0:int(args.num_recommendations) + 1]

similar_items = get_top_similar(args.game_slug, game_similarity_df)

print(similar_items)
