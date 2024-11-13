from igdb.wrapper import IGDBWrapper
import json
import argparse

# Grab all fields from IGDB
default_fields = 'age_ratings,aggregated_rating,aggregated_rating_count,alternative_names,artworks,bundles,category,checksum,collection,collections,cover,created_at,dlcs,expanded_games,expansions,external_games,first_release_date,follows,forks,franchise,franchises,game_engines,game_localizations,game_modes,genres,hypes,involved_companies,keywords,language_supports,multiplayer_modes,name,parent_game,platforms,player_perspectives,ports,rating,rating_count,release_dates,remakes,remasters,screenshots,similar_games,slug,standalone_expansions,status,storyline,summary,tags,themes,total_rating,total_rating_count,updated_at,url,version_parent,version_title,videos,websites'

# Filter for Platform:Nintendo Switch and Category:Main Game with at least some ratings
default_filter = 'platforms=130 & category=0 & (rating_count > 0 | aggregated_rating_count > 0)'


parser = argparse.ArgumentParser(description="Fetch IGDB games and save to file.")

parser.add_argument("--client-id", required=True, help="Your IGDB Client ID")
parser.add_argument("--access-token", required=True, help="Your IGDB Access Token")
parser.add_argument("--output", required=False, help="Output file (JSON)", default="games.json")
parser.add_argument("--fields", required=False, help="IGDB game fields to retrieve (comma-separated) default is all fields", default=default_fields)
parser.add_argument("--filter", required=False, help="IGDB game filter default is Nintendo Switch Main Games", default=default_filter)
parser.add_argument("--page-size", required=False, help="IGDB Limit for number of games to retrieve per query", default=500)

args = parser.parse_args()

wrapper = IGDBWrapper(args.client_id, args.access_token)

offset = 0

all_games = []

while True:
  byte_array = wrapper.api_request(
              'games',
              f'fields {args.fields}; where {args.filter}; offset {offset}; limit {args.page_size};'
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