# NextGame

This is a final project part of the WPI CS-547 Fall 2024 Information Retrieval course.

By: Augusto Wong, Kevin O'Brien

For more details, see [our website](https://kjrobrien.github.io/cs547-project/).

# Structure

- `scrape_data` - contains scripts for retrieveing data from IGDB API.
- `transform_data` - contains scripts for transforming data from IGDB API for usage in the rest of the project.
- `collaborative_filtering` - contains the code for running item-based collaborative filtering on the transformed data. 
- `content_based_filtering` - contains the code for running content-based filtering.
- `gpt_recommender` - contains the code for running the Open AI ChatGPT based recommender.
- `web` - contains the code for running the web page that invokes `collaborative_filtering`, `content_based_filtering`, and `gpt_recommender`.
- `docs` - contains the source for the [documentation site](https://kjrobrien.github.io/cs547-project/).


## `scrape_data`

### `scrape_games.py`

This script retrieves games from the [IGDB API](https://api-docs.igdb.com/#getting-started). By default, it only retrieves Nintendo Switch games, but can be modified via program arguments.

| Argument | Description | Default |
| -------- | ----------- | ------- |
| `--client-id` | IGDB Client ID:  See [IGDB documentation](https://api-docs.igdb.com/#account-creation)| None
| `--access-token` | IGDB Client Access Token: See [IGDB documentation](https://api-docs.igdb.com/#account-creation)| None | 
| `--output` | The file path for the output JSON results | `games.json` | 
| `--fields` | Comma-separated list of game fields to retrieve from IGDB | All fields |
| `--filter` | IGDB game filter | Nintendo Switch Main Games |
| `--page-size` | IGDB Limit for number of games to retrieve per query | 500 |

### `all_switch_games.json`

This file contains the main dataset, it is the output of `scrape_games.py`.

### `scrape_reviews.py`

This script retrieves game reviews from IGDB. It takes in several program arguments:

| Argument | Description | Default |
| -------- | ----------- | ------- |
| `--input` | The file path for the input JSON games from `scrape_games.py` | None |
| `--output` | The file path for the output JSON results | `game_reviews.json` | 

### `all_switch_games_reviews.json`

This file contains the review dataset, it is the output of `scrape_reviews.py`.

### `scrape_games_to_csv.py`

This script ingests the JSON outputs of the API and converts the data to help with creating graphs.

## `transform_data`

### `transform_ratings.py`

This script takes the JSON file (`all_switch_games_reviews.json`) and converts it to CSV. It takes in a couple of arguments:

| Argument | Description | Default |
| -------- | ----------- | ------- |
| `--input` | The file path for the input JSON games from `scrape_reviews.py` | None |
| `--output` | The file path for the output CSV results | None | 

### `ratings.csv`

This is the main ratings dataset and the output of `transform_ratings.py`.

## `collaborative_filtering`

### `collaborative_filtering.py`

This script runs item-based collaborative filtering based on an input dataset of games and reviews. It takes in a list of games to use as the basis for recommending games to the user. It takes in a few arguments:

| Argument | Description | Default |
| -------- | ----------- | ------- |
| `--input` | The file path for the ratings CSV results from `transform_ratings.py` | None |
| `--game-slugs` | A comma-separated list of games from `--input` to use as the basis for recommendations | None | 
| `--num-recommendations` | The number of recommendations to return | None |

## `gpt_recommender`

### `gpt_recommender.py`

This script queries Open AI ChatGPT using its API to generate recommendations. It takes in the following argments:

| Argument | Description | Default |
| -------- | ----------- | ------- |
| `--games-input` | The file path for the input JSON games from `scrape_reviews.py` | None |
| `--game-slugs` | A comma-separated list of games from `--input` to use as the basis for recommendations | None | 
| `--num-games` | The number of recommendations to return | None |
| `--openai-api-key` | The API Key to use to call the [Open AI API](https://openai.com/api/) | None |


## `web`

### `app.py`

This application serves a simple web server for generating recommendations. It has a dropdown to select games and then runs all three recommenders and displays the results. It takes in the following arguments:

| Argument | Description | Default |
| -------- | ----------- | ------- |
| `--games-input` | The file path for the input JSON games from `scrape_reviews.py` | None |
| `--ratings-csv` | The file path for the ratings CSV results from `transform_ratings.py` | None |
| `--openai-api-key` | The API Key to use to call the [Open AI API](https://openai.com/api/) | None |



## Dependencies

Each folder contains a `requirements.txt` with python pip dependencies. Those can be installed with `pip install -r requirements.txt`.
