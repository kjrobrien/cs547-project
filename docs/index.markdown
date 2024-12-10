---
layout: home
---

[Github](https://github.com/kjrobrien/cs547-project)


# Abstract

NextGame enhances gaming discovery by recommending games based on user preferences. Users select several games as a starting point and NextGame then 
offers game recommendations for the user to try out. NextGame uses the [IGDB API](https://api-docs.igdb.com/#getting-started) to retrieve information and reviews about all Nintendo Switch games. 
Then, NextGame uses three methods for generating recommendations: item-based collaborative filtering, content-based filtering, and an LLM-based recommender. 


# Dataset

We used the [IGDB API](https://api-docs.igdb.com/#getting-started) for retrieving all Nintendo Switch games and some user reviews for those games.
[IGDB](https://www.igdb.com/) is the Internet Game Database, which contains details about essentially all video games and their attributes like: console, genre, release date, etc.
There is also a community section of the website where users can review games. We retrieved all Nintendo Switch games, their attributes, and reviews.

## Games

Our Nintendo Switch games dataset can be found [here](https://github.com/kjrobrien/cs547-project/blob/master/scrape_data/all_switch_games.json). This dataset contains 4,110 games. For each game, it contains several properties, we used the following:

_Descriptions from the IGDB API Documentation_

* `genres` - genres of the game
* `involved_companies` - companies who developed this game
* `age_ratings` - age Rating according to various rating organisations
* `artworks` - official artworks of this game
* `game_modes` - modes of gameplay (singeplayer, multiplayer, etc.)
* `keywords` - words or phrases that get tagged to a game such as “world war 2” or “steampunk”
* `player_perspectives` - describe the view/perspective of the player in a video game
* `similar_games` - games that are similar to this game
* `tags` - related entities in the IGDB API
* `themes` - themes of the game
* `language_supports` - supported languages for this game
* `game_localizations` - game localizations for this game. A region can have at most one game localization for a given game
* `collections` - the series the game belongs to
* `franchises` - franchises the game belongs to
* `game_engines` - game engines used in this game
* `multiplayer_modes` - multiplayer modes for the game
* `remakes` - remakes of this game
* `category` - the category of this game
* `expansions` - expansions of the game
* `parent_game` - if a DLC, expansion or part of a bundle, this is the main game or bundle

## Game Ratings

Our Nintendo Switch game reviews dataset can be found in JSON [here](https://github.com/kjrobrien/cs547-project/blob/master/scrape_data/all_switch_games_reviews.json) and in a simplified and cleaner CSV [here](https://github.com/kjrobrien/cs547-project/blob/master/transform_data/ratings.csv).

This dataset consisted of 1543 reviews by 596 unique users for 793 unique games. This was an incredbily sparse dataset as each game had few reviews, with many games having no reviews.

<!-- Insert Graphs Here -->

# Methodology

We employed three recommendation strategies: item-based collaborative filtering, content-based filtering, and LLM-based recommender using Open AI ChatGPT's API. We then built a basic web page for some survey respondents to try.

## Item-based Collaborative Filtering

## Content-based Filtering

## LLM-based Recommendations

## Website

<video controls width="100%" playsinline autoplay muted loop>
  <source src="{{ '/assets/videos/site_recording.webm' | relative_url }}" type="video/webm">
  Your browser does not support the video tag.
</video>



# Evaluation

<!-- Insert RMSE for Collaborative Filtering -->

<!-- Insert results of survey -->

# Conclusion

