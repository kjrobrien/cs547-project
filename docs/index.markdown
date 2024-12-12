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
IGDB API and classified properties with 3 different weight groups based on importance. We then used Jaccard similarity to calculate
similarities betweeen items' attributes.


We used the following properties from the IGDB API:

_Descriptions from the IGDB API Documentation_

### 0.75 weight

This will make sure to recommend games with similar gameplay.

* `genres` - genres of the game
* `game_modes` - modes of gameplay (singeplayer, multiplayer, etc.)
* `player_perspectives` - describe the view/perspective of the player in a video game
* `multiplayer_modes` - multiplayer modes for the game
* `keywords` - words or phrases that get tagged to a game such as “world war 2” or “steampunk”
* `similar_games` - games that are similar to this game
* `category` - the category of this game
* `franchises` - franchises the game belongs to
* `remakes` - remakes of this game
* `expansions` - expansions of the game
* `tags` - related entities in the IGDB API

### 0.5 weight

This will make sure to recommend games with similar artwork, region, language and age requirements.

* `age_ratings` - age Rating according to various rating organisations
* `artworks` - official artworks of this game
* `themes` - themes of the game
* `language_supports` - supported languages for this game
* `collections` - the series the game belongs to
* `game_engines` - game engines used in this game
* `game_localizations` - game localizations for this game. A region can have at most one game localization for a given game

### 0.25 weight

This will make sure to recommend games from similar developers and parent games.

* `involved_companies` - companies who developed this game
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

In order to easily try out our above models, we built a simple website. The website includes a dropdown where a user can
select multiple games. When the user presses submit, each of the recommenders run, with the results displayed on the web page.

### Demo

<video controls width="100%" playsinline autoplay muted loop>
  <source src="{{ '/assets/videos/site_recording.webm' | relative_url }}" type="video/webm">
  Your browser does not support the video tag.
</video>

### DATA/Graphs

Most popular Games by rating range
`Pic`

Most popular Games by aggregated rating range
`Pic`

Worst Games by rating range
`Pic`

Worst Games by aggregated rating range
`Pic`

Most Popular Genres:
* 31: Adventure (981 Games)
* 32: Indie (971 Games
* 9: Puzzle (435 Games)
* 12: RPG (422 Games)
* 33: Arcade (381)
`Pic`

Most Franchises:
* 845: Mario (20 Games)
* 51: Lego (17 Games)
* 60: Pokemon (12 Games)
* 16: NBA (10 Games)
* 1: Star Wars (9 Games)
`Pic` 
    
Most Game Modes:
* 1: Single Player (3994 Games)
* 2: Multiplayer (1233 Games
* 3: Co-operative (864 Games)
* 4: Split Screen (176 Games)
* 5: Massively Multiplayer Online (36 Games)
* 6: Battle Royale (21 Games)
`Pic` 

Popular Player Perspectives:
* 4: Side View (1212 Games)
* 3: Bird View / Isometric (1004 Games
* 2: Third person (906 Games)
* 1: First person (475 Games)
* 5: Text (184 Games)
* 7: Virtual Reality (51 Games)
* 6: Auditory (8 Games)
`Pic`

Popular Themes:
* 1: Action (2575 Games)
* 17: Fantasy (1047 Games
* 18: Science Fiction (600 Games)
* 27: Comedy (493 Games) 

Popular Game Engines:
* 13: Unity (631 Games)
* 439: Unreal Engine 4 (166 Games)
* 6: Unreal Engine (80 Games)
* 79: GameMaker: Studio (31 Games)
            
# Evaluation
 We developed a survey and shared it with friends to get the below results.                              
 50% of the users preferred ChatGPTs response and the other two algorithm were evenly distributed at 25%.

`Survey`: https://forms.gle/NMbAY2fMg3LU6sSP8

`Collaborative Filtering Rating:` 2.78/5

`Content-Based Filtering Rating:` 3.11/5

`ChatGPT:` 3.44/5

How Familiar are you with the listed games? 3.75/5
How likely are you to use a website like this? 3.55/5

Why was ChatGPT the winner, in summary is because unlike the other two algorithms.
It had diverse options and did not overfit on the given data from the user. 

From a user:

`The recommended games were diverse enough to connect to each of the games I had selected giving a good variety
nd not focusing on just one aspect or game in my list`


# Conclusion

Developing algorithms to recommend video games is challenging because users have highly diverse
tastes and preferences influenced by multiple factors. Games require active participation,
therefore preferences can vary drastically based on mood, available time, desired level of
engagement and even social trends. This makes it difficult to create a one-size-fits-all
recommendation system. Furthermore, the sheer volume and sparsity of games complicates the task of
categorizing and predicting user preferences accurately. 
