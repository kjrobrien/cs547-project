import argparse

import json

import sys

import os


from flask import Flask, request, jsonify, render_template_string

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from collaborative_filtering import collaborative_filtering
from gpt_recommender import gpt_recommender
from content_based_filtering import content_based

games = []

slug_to_name = {}

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NextGame</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.3/dist/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.1.3/dist/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/css/bootstrap-select.min.css">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/js/bootstrap-select.min.js"></script>

    <script>
        async function submitGames(event) {
            event.preventDefault();
            const collabList = document.getElementById("collabResponse");
            const contentList = document.getElementById("contentResponse");
            const chatGPTList = document.getElementById("chatGPTResponse");
            collabList.innerHTML = "Loading...";
            contentList.innerHTML = "Loading...";
            chatGPTList.innerHTML = "Loading...";
            const selectedGames = Array.from(document.getElementById("games").selectedOptions).map(opt => opt.value);
            const response = await fetch('/recommendations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "gameSlugs": selectedGames })
            });
            const result = await response.json();
            
            collabList.innerHTML = "";
            result.itemCollaborativeFiltering.forEach(x => {
                const li = document.createElement("li");
                li.textContent = `${x.name}: ${x.value ?? "Unknown Score"}`;
                collabList.appendChild(li);
            });
            
            contentList.innerHTML = "";
            result.contentBasedFiltering.forEach(x => {
                const li = document.createElement("li");
                li.textContent = `${x.name}: ${x.value ?? "Unknown Score"}`;
                contentList.appendChild(li);
            });
            
            chatGPTList.innerHTML = "";
            result.chatGPT.forEach(x => {
                const li = document.createElement("li");
                li.textContent = `${x.name}: ${x.value ?? "Unknown Score"}`;
                chatGPTList.appendChild(li);
            });
        }
    </script>
</head>

<body>
    <div class="container">
        <div class="row mb-3">
            <h1>Select Games</h1>

            <form onsubmit="submitGames(event)">
                <div class="mb-3">
                
                    <select id="games" name="games" multiple class="form-control selectpicker" data-live-search="true" style="width=100%">
                        {% for game in games %}
                        <option value="{{ game['slug'] }}">{{ game['name'] }}</option>
                        {% endfor %}
                    </select>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
        <div class="row">
            <h2>Recommendations:</h2>

            <div class="col">
                <h3>Collaborative Filtering</h3>
                <ul id="collabResponse"></ul>
            </div>
            <div class="col">
                <h3>Content-Based Filtering</h3>
                <ul id="contentResponse"></ul>
            </div>
            <div class="col">
                <h3>ChatGPT</h3>
                <ul id="chatGPTResponse"></ul>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, games=games)


def run_collab_filter(game_slugs):
    aggregated_df = collaborative_filtering.parse_file(args.ratings_csv)
    ug, sim = collaborative_filtering.get_user_game_matrix_similarity_df(aggregated_df)
    similar_items = collaborative_filtering.get_top_similar(game_slugs, sim, 10)
    
    return [{'name': slug_to_name.get(idx, idx), 'value': None if val != val else round(val,2)} for idx, val in similar_items.items()]

def run_content_based_filter(game_slugs):
    recommendations = content_based.getRecommendations(args.games_input, game_slugs, 10)
    return [{'name': game['name'], 'value': round(score,2)} for game, score in recommendations]

def run_chatgpt_recommender(game_slugs):
    games = gpt_recommender.recommend_games(args.openai_api_key, args.games_input, game_slugs, 10)
    return [{'name': slug_to_name.get(x.slug, x.slug), 'value': x.score} for x in games]
    

@app.route("/recommendations", methods=["POST"])
def get_recommendations():
    data = request.get_json()
    game_slugs = data["gameSlugs"]
    
    response = {
        "itemCollaborativeFiltering": run_collab_filter(game_slugs),
        "contentBasedFiltering": run_content_based_filter(game_slugs),
        "chatGPT": run_chatgpt_recommender(game_slugs)
    }
    
    return jsonify(response), 200
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Runs a basic web ui for game recommendations.")

    parser.add_argument("--games-input", required=True, help="Input games JSON file")
    parser.add_argument("--ratings-csv", required=True, help="Input ratings CSV")
    parser.add_argument("--openai-api-key", required=True, help="API Key for Open AI")
    
    args= parser.parse_args()
    
    with open(args.games_input, "r") as file:
        games = json.load(file)
        def sortKey(g):
            return g["name"]
        games.sort(key=sortKey)
        for game in games:
            slug_to_name[game["slug"]] = game["name"]

    app.run(host='0.0.0.0', port=5000, debug=True)