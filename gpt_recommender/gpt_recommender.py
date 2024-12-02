import argparse
import json
from openai import OpenAI
from pydantic import BaseModel



parser = argparse.ArgumentParser(description="Take a ratings CSV file and a games JSON file and generate recommendations using chatgpt.")

parser.add_argument("--games-input", required=True, help="Input games JSON file")
parser.add_argument("--game-slugs", required=True, help="The game slug to get recommendations")
parser.add_argument("--openai-api-key", required=True, help="API Key for Open AI")

args= parser.parse_args()



class GameResponse(BaseModel):
    slugs: list[str]
    
client = OpenAI(
    api_key=args.openai_api_key
)

games = []

with open(args.games_input, "r") as file:
  games = json.load(file)
  
slugs = []
  
for game in games:
    slugs.extend([game["slug"]])

slugs_string = ",".join(slugs)
completion = client.beta.chat.completions.parse(
    messages=[
        {
            "role": "system",
            "content": f"You are a helpful video game recommender. You will give recommendations for new games to the user given their preferences expressed as slugs. Return just the recommended game slugs. Only return games slugs from the following list, do not return any extras. Return these exact slugs. The list of slugs: {slugs_string}",
        },
        {
            "role": "user",
            "content": f"My favorite game slugs are: {args.game_slugs}"
        }
    ],
    model="gpt-4o-mini",
    response_format=GameResponse,
)

recommendations = completion.choices[0].message.parsed
print(recommendations)
