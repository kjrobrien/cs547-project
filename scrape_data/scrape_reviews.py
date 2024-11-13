import argparse
import json
import cloudscraper
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, RetryError

parser = argparse.ArgumentParser(description="Fetch IGDB reviews and save to file.")

parser.add_argument("--input", required=True, help="An input JSON file of IGDB games")
parser.add_argument("--output", required=False, help="Output file (JSON)", default="games_reviews.json")
parser.add_argument("--url", required=False, help="The IGDB GraphQL endpoint", default="https://www.igdb.com/gql")

args = parser.parse_args()

@retry(stop=stop_after_attempt(10), wait=wait_exponential_jitter())
def fetch_reviews(game_slug):
    query = """
    query GetGamePageCommunityData($gameSlug: String!) {
    game(input: {slug: $gameSlug}) {
        id
        slug
        reviewsCount
        reviews {
        id
        title
        slug
        createdAt
        user {
            username
            slug
            profileImageUrl
            __typename
        }
        reviewLikesCount
        reviewText {
            content
            __typename
        }
        ratingValue
        __typename
        }
        __typename
    }
    }
    """

    variables = {
    "gameSlug": game_slug
    }

    scraper = cloudscraper.create_scraper()

    response = scraper.post(args.url, json={'query': query, 'variables': variables})

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("failed to grab")

input_slugs = []

with open(args.input, "r") as input_file:
    input_json = json.load(input_file)
    for input_game in input_json:
        if input_game.get("aggregated_rating_count", 0) > 0 or input_game.get("rating_count", 0) > 0:
            input_slugs.append(input_game["slug"])

existing_slugs = []

all_reviews = []

try:
    with open(args.output, "r") as output_file:
        all_reviews = json.load(output_file)
        for existing_game in all_reviews:
            existing_slugs.append(existing_game["slug"])
except FileNotFoundError:
    pass

game_slugs = list(set(input_slugs).difference(existing_slugs))

print(f"input slugs len {len(input_slugs)}")

print(f"Need to fetch {len(game_slugs)} reviews")

try:
    for game_slug in game_slugs:
        try:
            reviews = fetch_reviews(game_slug)
            all_reviews.append(reviews["data"]["game"])
            print(f"Fetched {game_slug}")
        except RetryError as e:
            print(f"Fetch failed {game_slug} after retries:", e)
except KeyboardInterrupt:
    print("writing out current progress")
    pass


with open(args.output, "w") as output_file:
    json.dump(all_reviews, output_file, indent=2)
  
print(f"Results saved to {args.output}")