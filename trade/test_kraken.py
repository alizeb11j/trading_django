# import asyncio
# import json
# import websockets
import requests
import time

# async def kraken_btc_eur_ticker():
#     async with websockets.connect("wss://ws.kraken.com/") as websocket:
#         # Subscribe to the BTC/EUR ticker
#         subscribe_message = {
#             "event": "subscribe",
#             "pair": ["XBT/EUR"],
#             "subscription": {"name": "ticker"},
#         }
#         await websocket.send(json.dumps(subscribe_message))

#         while True:
#             response = await websocket.recv()
#             # Get Json
#             data = json.loads(response)
#             # Ignore heartbeat event and get price ticker
#             print(data)

#             if (
#                 isinstance(data, list)
#                 and len(data) > 1
#                 and isinstance(data[1], dict)
#                 and "c" in data[1]
#             ):
#                 # Extract the values of 'c'
#                 c_values = data[1]["c"]
#                 print("Price", c_values[0], "Quantity", c_values[1])
#                 # print(c_values)


# asyncio.get_event_loop().run_until_complete(kraken_btc_eur_ticker())


# URL for the Kraken API Ticker endpoint for BTC/EUR
url = "https://api.kraken.com/0/public/Ticker?pair=XBTEUR"
min_trade_bid = float("inf")
last_trade_list = []
# Make a GET request to the Kraken API
for i in range(1, 10):
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print(data)
        # Extract the last trade price from the response
        # The structure of the response might change, so adjust the keys accordingly

        last_trade_price = data["result"]["XXBTZEUR"]["c"][0]
        last_trade_price = float(last_trade_price)
        last_trade_list.append(last_trade_price)
        if (last_trade_price < min_trade_bid) and (last_trade_price != 0):
            min_trade_bid = last_trade_price

        # print(f"The current BTC to Euro buy price is: {last_trade_price} EUR")
        # return last_trade_price
    else:
        print(
            f"Failed to fetch data from Kraken API. Status code: {response.status_code}"
        )
        # return None
    time.sleep(0.8)
print("List", last_trade_list)
print("min val", min_trade_bid)
