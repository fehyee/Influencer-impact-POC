# Influencer-impact-POC
Scrap CA from influencer tweets and ascertain how much impact they have on price. 
---

# CA & Price Impact Tracker

This project is a proof-of-concept that demonstrates how to:

- **Extract Contract Addresses (CAs) from Tweets:**  
  Use the Twitter API to fetch tweets from an influencer and extract Solana token contract addresses from the tweet text.

- **Track Price Impact:**  
  Query the CoinGecko API for the token's price based on the contract address and simulate monitoring the price over intervals (e.g., immediately, 5, 10, and 15 minutes later) to calculate percentage price changes.

This project can be used to analyze how tweets containing token contract addresses might impact the price of the token over time.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [1. Extracting Contract Addresses from Tweets](#1-extracting-contract-addresses-from-tweets)
  - [2. Tracking Price Impact](#2-tracking-price-impact)


---

## Features

- **Twitter API Integration:**  
  Fetch the last few tweets from an influencer’s timeline using Tweepy (Twitter API v2).

- **Contract Address Extraction:**  
  Use regular expressions to detect Solana contract addresses in tweets.

- **Price Tracking:**  
  Query CoinGecko’s API (using the token’s contract address on Solana) to get the current price and simulate future price checks.

- **Data Export:**  
  Save tweet data and price impact data to JSON (or CSV) for further analysis.

---

## Requirements

- Python 3.8+
- [Tweepy](https://www.tweepy.org/)
- [requests](https://docs.python-requests.org/)
- [Twitter/X](https://developer.twitter.com/)
- [Coingeko](https://developer.twitter.com/)

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/fehyee/Influencer-impact-POC
   ```

2. **Create a Virtual Environment and Activate It:**

   On Windows:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the Required Packages:**

   ```bash
   pip install -r requirements.txt
   ```

   *(If you don’t have a `requirements.txt` file, you can install manually:)*

   ```bash
   pip install tweepy requests python-dotenv
   ```

---

## Configuration

Create a `.env` file in the root directory of the project and add your API credentials:

```env
# Twitter API Bearer Token
BEARER_TOKEN=your_twitter_bearer_token_here

# Coingeko API Key
API_KEY=your_coingeko_api_key_here

# (Optional) Other configuration variables can go here.
```

---

## Usage

This project is composed of two main components:

### 1. Extracting Contract Addresses from Tweets

The script fetch script uses Tweepy to fetch the tweets from a given influencer and extracts any Solana token contract addresses. It then saves the tweet data in a JSON format like:

```json
[
    {
        "tweet_id": "1234567890",
        "timestamp": "2025-01-10T14:30:00Z",
        "content": "Check out this new token! Contract: JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
    },
    {
        "tweet_id": "1234567891",
        "timestamp": "2025-01-11T15:00:00Z",
        "content": "Just another tweet without a token address."
    },
    {
        "tweet_id": "1234567892",
        "timestamp": "2025-01-12T16:45:00Z",
        "content": "Amazing drop! Solana token contract: EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    }
]
```

To run this script:

```bash
python test_x_api.py
```

This will generate a `tweets.json` file with the data.

### 2. Tracking Price Impact

The script `price_tracker.py` (or a combined script) uses the generated JSON file as input, extracts the contract addresses, and queries the CoinGecko API to obtain token prices. It then simulates checking prices at later intervals (e.g., 5, 10, and 15 minutes) and calculates the percentage change in price.

The code uses an endpoint such as:

```
https://api.coingecko.com/api/v3/simple/token_price/solana?contract_addresses={contract_address}&vs_currencies=usd
```

and outputs the results as a JSON file (or CSV, if desired).

To run the price tracker:

```bash
python test_coingeko_api.py
```

*(Make sure to update the contract addresses in your sample JSON to ones that are recognized by CoinGecko for accurate price data.)*

---

