# Recommending by category using jaccard similarity
import json

# Load the JSON file
def getJson(input_file):
    with open(input_file, "r") as file:
        all_switch_games = json.load(file)
    return all_switch_games


# Jaccard Similarity Function
def jaccard_similarity(set1, set2):
    if isinstance(set1, int):
        set1 = [set1]
        set2 = [set2]
    intersection = len(set(set1) & set(set2))
    union = len(set(set1) | set(set2))
    return intersection / union if union > 0 else 0


def jaccard_similarity_by_keyword(keyword, game, input_data):
    try:
        similarity = sum(jaccard_similarity(
            game[keyword], input_game[keyword]) for input_game in input_data) / len(input_data)
    except KeyError as e:
        return 0.0
    return similarity


# Recommender System
def recommend_games(game_slugs, dataset, top_n):
    # Extract genre lists of input games
    input_data = [game for game in dataset if game["slug"] in game_slugs]

    # Compute similarity scores
    scores = []
    games_considered = 0
    seenGames = {}
    for game in dataset:
        if game["slug"] in game_slugs:
            continue  # Skip input games
        if game["id"] in seenGames:
            continue
        seenGames[game["id"]] = True
        games_considered += 1
        # map, keyword to weight
        keyword_to_weights = {"genres": 0.75, "game_modes": 0.75, "player_perspectives": 0.75,
                              "multiplayer_modes": 0.75, "keywords": 0.75,
                              "similar_games": 0.75, "category": 0.75, "franchises": 0.75,
                              "remakes": 0.75, "expansions": 0.75, "tags": 0.75,
                              "age_ratings": 0.5, "artworks": 0.5, "themes": 0.5,
                              "language_supports": 0.5, "collections": 0.5, "game_engines": 0.5,
                              "involved_companies": 0.25, "parent_game": 0.25, "game_localizations": 0.25}
        combined_score = 0.0
        for keyword, weight in keyword_to_weights.items():
            similarity = jaccard_similarity_by_keyword(keyword, game, input_data)
            combined_score += similarity * weight
        scores.append((game, combined_score))

    # Sort by similarity and return top N
    print("=========================")
    print("Games considered: ", games_considered)
    print("Total game dataset: ", len(dataset))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_n]


# games = list of game ids
# returns: top N games to be recommended
def getRecommendations(input_file, game_slugs, top_n=5):
    all_switch_games = getJson(input_file)
    # Get recommendations
    recommendations = recommend_games(game_slugs, all_switch_games, top_n)
    return recommendations


# Output recommendations
# 138251: Mario Kart Live: Home Circuit #10
# 26758: Super Mario Odyssey # 8,31 # 69095, 268535, 268536
# 119388: The Legend of Zelda: Tears of the Kingdom #12,31
# input = [138251,26758,119388]

if __name__ == "__main__":
    game_slugs = ["the-legend-of-zelda-tears-of-the-kingdom"]
    recommendations = getRecommendations("../scrape_data/all_switch_games.json", game_slugs)
    print("=========================")
    print("Recommended Games:")
    for game, score in recommendations:
        print(f"{game['name']} (ID: {game['id']})")
