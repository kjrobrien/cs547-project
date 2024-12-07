import json
import csv
import argparse

parser = argparse.ArgumentParser(description="Take IGDB ratings from JSON and convert to CSV.")

parser.add_argument("--input", required=True, help="Input JSON file")
parser.add_argument("--output", required=True, help="Output CSV file")

args= parser.parse_args()

games = []

with open(args.input, "r") as file:
  games = json.load(file)
  
output = [["game_slug", "user_slug", "rating"]]
  
for game in games:
    for review in game["reviews"]:
        output.extend([[game["slug"], review["user"]["slug"], review["ratingValue"]]])

with open(args.output, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(output)
