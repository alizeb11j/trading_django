import requests
from bs4 import BeautifulSoup
import time


def get_from_kraken_rest():
    return_list = []
    url = "https://api.kraken.com/0/public/Ticker?pair=XBTEUR"
    min_trade_bid = float("inf")
    last_trade_list = []
    last_trade_qty = 0
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
                last_trade_qty = float(data["result"]["XXBTZEUR"]["c"][1])

            # print(f"The current BTC to Euro buy price is: {last_trade_price} EUR")
            # return last_trade_price
        else:
            print(
                f"Failed to fetch data from Kraken API. Status code: {response.status_code}"
            )
            # return None
        time.sleep(0.4)
    # print("List", last_trade_list)
    # print("min val", min_trade_bid)
    return min_trade_bid, last_trade_qty


def get_from_xe():
    # Fetch the web page
    url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=ZAR"
    response = requests.get(url)

    # Parse the web page
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup.prettify())
    elements = soup.find("p", class_="result__BigRate-sc-1bsijpp-1 dPdXSB")
    print(elements.text)
    price = elements.text
    price = price.split(" ")
    price.pop(2)
    price.pop(1)
    # print(float(price[0]))
    return float(price[0])


def get_data_altcoin():
    r = requests.get("https://www.altcointrader.co.za/")

    # Parsing the HTML
    soup = BeautifulSoup(r.content, "html.parser")

    # print(soup.prettify())
    s = soup.find("div", id="sell-orders")
    lines = s.find_all("tr")
    # print("no of values:", len(lines))
    Sell_object = {}
    Sell_object["Price"] = []
    cnt = 0
    alt_qty = 0
    sum_price = []
    for line in lines:
        if cnt < 11:
            mstr = line.text
            mstr_list = mstr.split("\n")
            mstr_list.pop(0)
            mstr_list.pop(3)

            if cnt > 0:
                sum_price.append(float(mstr_list[0]))
                alt_qty = float(mstr_list[1])
            # print(mstr_list)
            cnt += 1
        else:
            break
    # avg_price = sum_price / 3
    # print(avg_price)
    # print(sum_price)
    max_kraken_bid = float(max(sum_price))
    # print("Rand List:", sum_price)
    return max_kraken_bid, alt_qty
