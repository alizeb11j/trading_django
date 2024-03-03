import requests
from bs4 import BeautifulSoup


def get_from_kraken_rest():
    return_list = []
    # URL for the Kraken API Ticker endpoint for BTC/EUR
    url = "https://api.kraken.com/0/public/Ticker?pair=XBTEUR"

    # Make a GET request to the Kraken API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # print(data)
        # Extract the last trade price from the response
        # The structure of the response might change, so adjust the keys accordingly

        last_trade_price = data["result"]["XXBTZEUR"]["c"][0]
        # return_list+=last_trade_price
        qty = data["result"]["XXBTZEUR"]["c"][1]
        # return_list+=qty
        # print(f"The current BTC to Euro buy price is: {last_trade_price} EUR")
        return float(last_trade_price), float(qty)
    else:
        print(
            f"Failed to fetch data from Kraken API. Status code: {response.status_code}"
        )
        return None


def get_from_oanda():
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
    sum_price = 0
    for line in lines:
        if cnt < 2:
            mstr = line.text
            mstr_list = mstr.split("\n")
            mstr_list.pop(0)
            mstr_list.pop(3)

            if cnt > 0:
                sum_price += float(mstr_list[0])
                alt_qty += float(mstr_list[1])
            # print(mstr_list)
            cnt += 1
        else:
            break
    # avg_price = sum_price / 3
    # print(avg_price)
    # print(sum_price)
    return sum_price, alt_qty
