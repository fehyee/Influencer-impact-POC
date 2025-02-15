import requests

url = "https://api.coingecko.com/api/v3/simple/token_price/solana?contract_addresses=So11111111111111111111111111111111111111112&vs_currencies=usd"

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-hdbauALxGpVBxS5vS4NqYrCX"
}

response = requests.get(url, headers=headers)

print(response.text)