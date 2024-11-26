import argparse
import pandas

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

parser = argparse.ArgumentParser(description="Take a ratings CSV file a run collaborative filtering.")

parser.add_argument("--input", required=True, help="Input CSV file")

args= parser.parse_args()


df = pandas.read_csv(args.input)

df = df.dropna()


# Grab the user's highest rating for a game.
aggregated_df = df.groupby(['user_slug', 'game_slug']).rating.max().reset_index()

user_game_matrix = aggregated_df.pivot(index="user_slug", columns="game_slug", values="rating").fillna(0)

game_similarity = cosine_similarity(user_game_matrix.T)

# This is a similarity matrix (x,y) representing the similarity between game x and y.
game_similarity_df = pandas.DataFrame(game_similarity, index=user_game_matrix.columns, columns=user_game_matrix.columns)

def get_top_similar(slug, similarity_df, n=20):
    similar = similarity_df[slug].sort_values(ascending=False)
    return similar[1:n+1]

similar_items = get_top_similar("super-mario-odyssey", game_similarity_df)

print(similar_items)
