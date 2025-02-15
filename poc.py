import json
import time
import requests
import re
from datetime import datetime

# Regular expression for matching potential Solana token contract addresses
SOLANA_REGEX = r"[1-9A-HJ-NP-Za-km-z]{32,44}"

def get_price(contract_address, retries=3, delay=5):
    """
    Fetch the current price (in USD) for the given contract address using CoinGecko's API.
    Endpoint:
      https://api.coingecko.com/api/v3/simple/token_price/solana?contract_addresses={contract_address}&vs_currencies=usd
    """
    # Clean up the contract address (remove extra whitespace)
    contract_address_clean = contract_address.strip()
    url = f"https://api.coingecko.com/api/v3/simple/token_price/solana?contract_addresses={contract_address_clean}&vs_currencies=usd"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "INPUT COINGEKO API KEY" # Coingeko API Key
    }
    for attempt in range(1, retries + 1):
        try:
            print(f"Fetching price for {contract_address_clean} (attempt {attempt}):")
            print(f"URL: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            print("Response JSON:", data)
            # Use the contract address as given (case-sensitive)
            if contract_address_clean in data:
                return data[contract_address_clean]["usd"]
            else:
                print(f"No price data found for contract address: {contract_address_clean}")
                return None
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"Rate limit hit (attempt {attempt}/{retries}). Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            else:
                print(f"Error retrieving price for contract '{contract_address_clean}': {e}")
                return None
        except Exception as ex:
            print(f"Unexpected error retrieving price for contract '{contract_address_clean}': {ex}")
            return None
    return None

def percent_change(new_price, old_price):
    """
    Calculate the percentage change between two prices.
    Returns None if either price is None.
    """
    if new_price is None or old_price is None:
        return None
    return ((new_price - old_price) / old_price) * 100

def load_sample_tweets(json_file):
    """
    Load tweets from a JSON file.
    The JSON file should contain a list of tweet objects with keys:
      - tweet_id (string or number)
      - timestamp (ISO8601 string, e.g. "2025-01-10T14:30:00Z")
      - content (string)
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_tweet(tweet):
    """
    Process a tweet record to extract its fields and any matching token contract addresses.
    """
    tweet_id = tweet.get("tweet_id")
    timestamp = tweet.get("timestamp")
    content = tweet.get("content", "")
    addresses = re.findall(SOLANA_REGEX, content)
    return tweet_id, timestamp, content, addresses

def main():
    # === CONFIGURATION ===
    # sample_json = "sample_tweets.json"  # JSON file with SAMPLE tweet records
    sample_json = "tweets.json"  # JSON file with LIVE tweet records
    output_json = "results.json"         # Output JSON file name
    # For demo purposes, simulate intervals with a short delay (2 seconds).
    delay_interval = 2  # seconds

    tweets = load_sample_tweets(sample_json)
    results = []

    for tweet in tweets:
        tweet_id, ts_str, content, addresses = process_tweet(tweet)
        # Only process tweets that contain at least one token contract address
        if not addresses:
            continue

        # Use the first detected contract address for price lookup
        contract_address = addresses[0]
        print(f"\nProcessing Tweet ID: {tweet_id} (Timestamp: {ts_str})")
        print("Tweet content:")
        print(content)
        print("Found contract address:", contract_address)

        # Get the initial price using the contract address
        initial_price = get_price(contract_address)
        if initial_price is None:
            print("Skipping tweet due to error retrieving initial price.")
            continue
        print(f"Initial Price: ${initial_price:.4f}")

        # Simulate waiting for intervals and fetching the price each time
        time.sleep(delay_interval)
        price_5min = get_price(contract_address)
        pc_5min = percent_change(price_5min, initial_price)

        time.sleep(delay_interval)
        price_10min = get_price(contract_address)
        pc_10min = percent_change(price_10min, initial_price)

        time.sleep(delay_interval)
        price_15min = get_price(contract_address)
        pc_15min = percent_change(price_15min, initial_price)

        results.append({
            "influencer": "@0xSonOfUri", 
            "tweet_id": tweet_id,
            "timestamp": ts_str,
            "contract_address": contract_address,
            "initial_price": initial_price,
            "price_5min": price_5min,
            "pc_change_5min": pc_5min,
            "price_10min": price_10min,
            "pc_change_10min": pc_10min,
            "price_15min": price_15min,
            "pc_change_15min": pc_15min,
            "tweet_content": content
        })

    # Write the results to a JSON file
    with open(output_json, 'w', encoding='utf-8') as jsonfile:
        json.dump(results, jsonfile, indent=4)

    print(f"\nResults written to {output_json}")

if __name__ == "__main__":
    main()
