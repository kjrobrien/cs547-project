# Recommending by category using jaccard similarity
import json

# Load the JSON file
def getJson():
    with open("all_switch_games.json", "r") as file:
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
def recommend_games(input_games, dataset, top_n=5):
    # Extract genre lists of input games
    input_data = [game for game in dataset if game["id"] in input_games]

    # Compute similarity scores
    scores = []
    games_considered = 0
    for game in dataset:
        if game["id"] in input_games:
            continue  # Skip input games
        games_considered += 1
        # map, keyword to weight
        keyword_to_weights = {"genres": 0.5, "involved_companies": 0.5, "age_ratings": 0.5,
                              "artworks": 0.5, "game_modes": 0.5, "keywords": 0.5,
                              "player_perspectives": 0.5, "similar_games": 0.5, "tags": 0.5,
                              "themes": 0.5, "language_supports": 0.5, "game_localizations": 0.5,
                              "collections": 0.5, "franchises": 0.5, "game_engines": 0.5,
                              "multiplayer_modes": 0.5, "remakes": 0.5, "category": 0.5,
                              "expansions": 0.5, "parent_game": 0.5}
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
    return [game for game, score in scores[:top_n]]


# games = list of game ids
# returns: top N games to be recommended
def getRecommendations(games):
    all_switch_games = getJson()
    # Get recommendations
    recommendations = recommend_games(games, all_switch_games)
    return recommendations


# Output recommendations
# 138251: Mario Kart Live: Home Circuit #10
# 26758: Super Mario Odyssey # 8,31 # 69095, 268535, 268536
# 119388: The Legend of Zelda: Tears of the Kingdom #12,31
# input = [138251,26758,119388]
input = [119388]
recommendations = getRecommendations(input)
print("=========================")
print("Recommended Games:")
for game in recommendations:
    print(f"{game['name']} (ID: {game['id']})")
