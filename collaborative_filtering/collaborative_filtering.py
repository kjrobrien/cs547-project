import argparse
import pandas

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

parser = argparse.ArgumentParser(description="Take a ratings CSV file a run collaborative filtering.")

parser.add_argument("--input", required=True, help="Input CSV file")
parser.add_argument("--game-slug", required=True, help="The game slug to get recommendations")
parser.add_argument("--num-recommendations", required=True, help="Number of recommendations")

args= parser.parse_args()


df = pandas.read_csv(args.input)

df = df.dropna()


# Grab the user's highest rating for a game.
aggregated_df = df.groupby(['user_slug', 'game_slug']).rating.max().reset_index()

user_game_matrix = aggregated_df.pivot(index="user_slug", columns="game_slug", values="rating").fillna(0)

game_similarity_df = user_game_matrix.corr(method="pearson")

def get_top_similar(slug, similarity_df):
    similar = similarity_df[slug].sort_values(ascending=False)
    return similar[1:int(args.num_recommendations) + 1]

similar_items = get_top_similar(args.game_slug, game_similarity_df)

print(similar_items)
