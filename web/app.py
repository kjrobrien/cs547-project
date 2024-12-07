import argparse

import json


from flask import Flask, request, jsonify, render_template_string

games = []

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
            const selectedGames = Array.from(document.getElementById("games").selectedOptions).map(opt => opt.value);
            const response = await fetch('/recommendations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "gameSlugs": selectedGames })
            });
            const result = await response.json();
            document.getElementById("response").textContent = JSON.stringify(result);
        }
    </script>
</head>
<style>
    .box {
        width: 200px;
        height: 200px;
    }
    .container {
        display: flex;
        gap: 20px;
        margin-bottom: 20px;
    }
    .buttons {
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 10px;
    }
</style>

<body>
    <div class="mb-3">
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
    <div>
    <h2>Response:</h2>
    <pre id="response" style="background: #f4f4f4; padding: 10px; border: 1px solid #ddd;"></pre>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, games=games)

@app.route("/recommendations", methods=["POST"])
def get_recommendations():
    data = request.get_json()
    game_slugs = data["gameSlugs"]
    
    return jsonify(game_slugs), 200
    

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Take a ratings CSV file and a games JSON file and generate recommendations using chatgpt.")

    parser.add_argument("--games-input", required=True, help="Input games JSON file")
    
    args= parser.parse_args()
    
    with open(args.games_input, "r") as file:
        games = json.load(file)
        def sortKey(g):
            return g["name"]
        games.sort(key=sortKey)

    app.run(host='0.0.0.0', port=5000, debug=True)