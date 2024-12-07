import argparse
import json
from openai import OpenAI
from pydantic import BaseModel



def convert_slugs_to_tag_strings(slugs):
    slugs_with_tags = []
    for slug in slugs:
        slugs_with_tags.extend(["<SLUG>"+slug+"</SLUG>"])
    return "\n".join(slugs_with_tags)


class SlugWithScore(BaseModel):
    slug: str
    score: float

class GameResponse(BaseModel):
    slugs: list[SlugWithScore]
    
def recommend_games(api_key, input_file, user_slugs, num_games):
    
    client = OpenAI(
        api_key=api_key
    )

    games = []

    with open(input_file, "r") as file:
        games = json.load(file)
    
    known_slugs = []
    
    for game in games:
        known_slugs.extend([game["slug"]])

    completion = client.beta.chat.completions.parse(
        messages=[
            {
                "role": "system",
                "content":
    f'''<INSTRUCTIONS>You are a helpful video game recommender. You have existing knowledge of all Nintendo Switch games.

You will receive multiple tags:

<KNOWN_SLUGS> - this contains all of the known game slugs that correspond to Nintendo Switch games. You will only recommend games that are included in this tag. Each game is wrapped in a <SLUG> tag.
<USER_SLUGS> - this contains the game slugs that we know the user likes. You will recommend other games from <KNOWN_SLUGS> that you think the user will like based on <USER_SLUGS>. Each game is wrapped in a <SLUG> tag. You will include a rating score between 0 and 1 for the user in the response.
<NUM_GAMES> - this contains the number of games the user would like to have returned as recommendations.
</INSTRUCTIONS>

<KNOWN_SLUGS>
    {convert_slugs_to_tag_strings(known_slugs)}

    </KNOWN_SLUGS>''',
            },
            {
                "role": "user",
                "content": f"<USER_SLUGS>{convert_slugs_to_tag_strings(user_slugs)}</USER_SLUGS><NUM_GAMES>{num_games}</NUM_GAMES>"
            }
        ],
        model="gpt-4o-mini",
        response_format=GameResponse,
    )

    recommendations = completion.choices[0].message.parsed


    # Filter out any slug hallucinations, don't include any slugs the user provided
    filtered_slugs = [x for x in recommendations.slugs if x.slug in known_slugs and x.slug not in user_slugs]
    
    return filtered_slugs



if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Take a ratings CSV file and a games JSON file and generate recommendations using chatgpt.")

    parser.add_argument("--games-input", required=True, help="Input games JSON file")
    parser.add_argument("--game-slugs", required=True, help="The game slug to get recommendations")
    parser.add_argument("--num-games", required=True, help="The number of games to recommend")
    parser.add_argument("--openai-api-key", required=True, help="API Key for Open AI")

    args= parser.parse_args()
    
    games = recommend_games(args.openai_api_key, args.games_input, args.game_slugs.split(","), args.num_games)
    print(games)
