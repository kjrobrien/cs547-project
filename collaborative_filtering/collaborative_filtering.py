import argparse
import pandas
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np


def parse_file(input_file):
    df = pandas.read_csv(input_file)

    df = df.dropna()

    # Grab the user's highest rating for a game.
    return df.groupby(['user_slug', 'game_slug']).rating.max().reset_index()


def get_user_game_matrix_similarity_df(df):
    user_game_matrix = df.pivot(index="user_slug", columns="game_slug", values="rating").fillna(0)
    # Use pearson correlation for calculating similarity.
    return [user_game_matrix, user_game_matrix.corr(method="pearson", min_periods=1)]


def predict_rating(user_slug, game_slug, similarity_df, user_game_matrix):
    if game_slug not in similarity_df.index:
        return np.nan
    
    if user_slug not in user_game_matrix.index:
        return np.nan
    
    similar_games = similarity_df[game_slug].drop(game_slug)
    
    user_ratings = user_game_matrix.loc[user_slug, similar_games.index]
    
    user_ratings = user_ratings[user_ratings != 0]
    
    return np.dot(user_ratings, similar_games[user_ratings.index]) / similar_games[user_ratings.index].sum()

def evaluate(train_df, test_df):
    user_game_matrix, game_similarity_df = get_user_game_matrix_similarity_df(train_df)
    
    test_df['predicted_rating'] = test_df.apply(
        lambda row: predict_rating(row['user_slug'], row['game_slug'], game_similarity_df, user_game_matrix),
        axis=1
    )
    test_df = test_df.dropna(subset=['predicted_rating'])
    
    return np.sqrt(mean_squared_error(test_df['rating'], test_df['predicted_rating']))


def get_top_similar(game_slugs, similarity_df, num):
    similar = similarity_df[game_slugs].mean(axis=1)
    similar = similar.drop(game_slugs)
    return similar.sort_values(ascending=False).head(num)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Take a ratings CSV file a run collaborative filtering.")

    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--game-slugs", required=True, help="The game slugs to get recommendations")
    parser.add_argument("--num-recommendations", required=True, help="Number of recommendations")

    args= parser.parse_args()
    

    aggregated_df = parse_file(args.input)
    
    train_df, test_df = train_test_split(aggregated_df, test_size=0.2)

    # Use the training and test sets for evaluation
    print(f"RMSE: {evaluate(train_df, test_df)}")
    
    # Use the full dataset for predicting incoming game_slugs for user outside dataset
    ug, sim = get_user_game_matrix_similarity_df(aggregated_df)

    # RMSE at last run was 2.68

    similar_items = get_top_similar(args.game_slugs.split(","), sim, int(args.num_recommendations))

    print(similar_items)


