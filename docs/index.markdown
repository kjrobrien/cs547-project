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

Our Nintendo Switch games dataset can be found [here](https://github.com/kjrobrien/cs547-project/blob/master/scrape_data/all_switch_games.json). This dataset contains 4,110 games. For each game, it contains various attributes that describe the games and assist users with filtering and searching.

## Game Ratings

Our Nintendo Switch game reviews dataset can be found in JSON [here](https://github.com/kjrobrien/cs547-project/blob/master/scrape_data/all_switch_games_reviews.json) and in a simplified and cleaner CSV [here](https://github.com/kjrobrien/cs547-project/blob/master/transform_data/ratings.csv).

This dataset consisted of 1543 reviews by 596 unique users for 793 unique games. This was an incredbily sparse dataset as each game had few reviews, with many games having no reviews.

<!-- Insert Graphs Here -->

# Methodology

We employed three recommendation strategies: item-based collaborative filtering, content-based filtering, and LLM-based recommender using Open AI ChatGPT's API. We then built a basic web page for some survey respondents to try.

## Item-based Collaborative Filtering

Item-based collaboratvie filtering compares items based on ratings across all users. The recommender then finds items similar to the current item and uses the similarity to calculate a rating prediction for the user.

We used the Pearson correlation coefficient to calculate our similarity matrix. We split our dataset 80% train, 20% test. We then calculated a RMSE of `2.68`. This was expected due to the sparsity of our dataset.

We then used this work to expose a recommender that takes in a list of games and returns the top recommendations based on that list.

## Content-based Filtering

Content-based filtering recommends items that have similar properties to items a user has rated highly. We used many attributes from the 
IGDB API and applied weights to each attribute. We then used Jaccard similarity to calculate similarities betweeen items' attributes.

We used the following properties from the IGDB API:

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

## LLM-based Recommendations

Our final recommender uses an LLM to generate recommendations. We used Open AI's ChatGPT-4o model. We relied on the Open AI API and python package. We utilized the [Structured Output](https://openai.com/index/introducing-structured-outputs-in-the-api/) functionality of their API to ensure that ChatGPT responded in the correct format.

Generating recommendations required some prompt engineering. We settled on the following prompt:

```
<INSTRUCTIONS>

You are a helpful video game recommender.

You have existing knowledge of all Nintendo Switch games.

You will receive multiple tags:

<KNOWN_SLUGS> - this contains all of the known game slugs that correspond
  to Nintendo Switch games. You will only recommend games that are included
  in this tag. Each game is wrapped in a <SLUG> tag.
<USER_SLUGS> - this contains the game slugs that we know the user likes.
    You will recommend other games from <KNOWN_SLUGS> that you think the user
    will like based on <USER_SLUGS>. Each game is wrapped in a <SLUG> tag.
    You will include a rating score between 0 and 1 for the user in the
    response.
<NUM_GAMES> - this contains the number of games the user would like to have
  returned as recommendations.

</INSTRUCTIONS>

<KNOWN_SLUGS>
  <SLUG>super-mario-odyssey</SLUG>
  <SLUG>just-dance-2021</SLUG>
  <SLUG>nba-2k19</SLUG>
  ... repeated for all 4,110 games; omitted for brevity
</KNOWN_SLUGS>


<USER_SLUGS>
  <SLUG>super-mario-odyssey</SLUG>
  <SLUG>the-legend-of-zelda-tears-of-the-kingdom</SLUG>
</USER_SLUGS>

<NUM_GAMES>5</NUM_GAMES>
```

Then, ChatGPT responds with the following format:

```
[
  SlugWithScore(slug='luigis-mansion-3', score=0.8),
  SlugWithScore(slug='puzzle-and-dragons-gold', score=0.75),
  SlugWithScore(slug='bayonetta-3', score=0.85),
  SlugWithScore(slug='mario-golf-super-rush', score=0.7),
  SlugWithScore(slug='mario-plus-rabbids-kingdom-battle', score=0.8)
]
```

## Website

In order to easily try out our above models, we built a simple website. The website includes a dropdown where a user can select multiple games. When the user presses submit, each of the recommenders run, with the results displayed on the web page.

### Demo

<video controls width="100%" playsinline autoplay muted loop>
  <source src="{{ '/assets/videos/site_recording.webm' | relative_url }}" type="video/webm">
  Your browser does not support the video tag.
</video>



# Evaluation

<!-- Insert results of survey -->

# Conclusion

