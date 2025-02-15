import tweepy
import json

# ==========================
# CONFIGURATION
# ==========================
BEARER_TOKEN = "INPUT_TWITTER_BEARER_TOKEN"  # Twitter Bearer token
USERNAME = "0xSonOfUri"          # The influencer's Twitter handle

# ==========================
# INITIALIZE TWITTER CLIENT
# ==========================
# client = tweepy.Client(bearer_token=BEARER_TOKEN)
client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True) #This tells Tweepy to automatically pause your requests until the rate limit resets.


# ==========================
# FUNCTION TO FETCH THE LAST N TWEETS
# ==========================
def fetch_last_tweets(username, count=3):
    # Get user details to retrieve the user ID.
    user = client.get_user(username=username)
    if not user.data:
        print(f"User {username} not found.")
        return []
    
    user_id = user.data.id
    print(f"Fetched user {username} with ID: {user_id}.")
    
    # Fetch recent tweets; tweets are returned in reverse chronological order.
    tweets = client.get_users_tweets(
        id=user_id,
        tweet_fields=["created_at", "text"],
        max_results=5  # Fetch a few tweets so we can take the latest 'count'
    )
    
    if not tweets.data:
        print(f"No tweets found for {username}.")
        return []
    
    # Return only the first 'count' tweets
    return tweets.data[:count]

# ==========================
# MAIN FUNCTION
# ==========================
def main():
    tweets = fetch_last_tweets(USERNAME, count=3)
    if not tweets:
        return

    # Format the output as a list of dictionaries with the required keys.
    results = []
    for tweet in tweets:
        results.append({
            "tweet_id": str(tweet.id),
            "timestamp": tweet.created_at.isoformat() if tweet.created_at else "",
            "content": tweet.text
            
        })
    
    # Write results to a JSON file.
    output_file = "tweets.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
