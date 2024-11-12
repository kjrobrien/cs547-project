import argparse
import cloudscraper

parser = argparse.ArgumentParser(description="Fetch IGDB reviews and save to file.")

parser.add_argument("--input", required=True, help="An input JSON file of IGDB games")
parser.add_argument("--output", required=False, help="Output file (JSON)", default="games_reviews.json")
parser.add_argument("--url", required=False, help="The IGDB GraphQL endpoint", default="https://www.igdb.com/gql")

args = parser.parse_args()

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
  "gameSlug": "super-mario-odyssey"
}

scraper = cloudscraper.create_scraper()

response = scraper.post(args.url, json={'query': query, 'variables': variables})

if response.status_code == 200:
    print(response.json())
else:
    print(response.text)
