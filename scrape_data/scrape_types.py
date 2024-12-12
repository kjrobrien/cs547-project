from igdb.wrapper import IGDBWrapper
import json
import argparse

default_fields = 'name'


parser = argparse.ArgumentParser(description="Fetch IGDB games and save to file.")

parser.add_argument("--client-id", required=True, help="Your IGDB Client ID")
parser.add_argument("--access-token", required=True, help="Your IGDB Access Token")
parser.add_argument("--output", required=False, help="Output file (JSON)", default="games.json")
parser.add_argument("--type", required=True, help="The type of object to grab")
parser.add_argument("--fields", required=False, help="IGDB game fields to retrieve (comma-separated) default is all fields", default=default_fields)
parser.add_argument("--page-size", required=False, help="IGDB Limit for number of games to retrieve per query", default=500)

args = parser.parse_args()

wrapper = IGDBWrapper(args.client_id, args.access_token)

offset = 0

all_games = []

while True:
  byte_array = wrapper.api_request(
              args.type,
              f'fields {args.fields}; offset {offset}; limit {args.page_size};'
            )
  result = json.loads(byte_array)

  print(f"offset {offset} limit {args.page_size} length {len(result)}")
  
  if len(result) == 0:
    break
  
  all_games.extend(result)
  offset += args.page_size

with open(args.output, "w") as file:
  json.dump(all_games, file, indent=2)
  
print(f"Results save to {args.output}")