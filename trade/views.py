from django.shortcuts import render
from django.http import JsonResponse

# from trade.test1 import (
#     get_data_altcoin,
#     get_from_kraken_rest,
#     get_from_xe,
# )

import aiohttp
from bs4 import BeautifulSoup
import asyncio
import json


class AsyncWebScraper:
    def __init__(self, urls):
        self.urls = urls
        self.alt_data = []
        self.xe_data = []
        self.kraken_data = []

    async def fetch_alt(self, session, url):
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")

            # print(soup.prettify())
            s = soup.find("div", id="sell-orders")
            lines = s.find_all("tr")
            # print("no of values:", len(lines))
            Sell_object = {}
            Sell_object["Price"] = []
            cnt = 0
            Alt_Qty = 0
            Alt_List = []
            Max_Alt_Val = 0
            for line in lines:
                if cnt < 11:
                    mstr = line.text
                    mstr_list = mstr.split("\n")
                    mstr_list.pop(0)
                    mstr_list.pop(3)

                    if cnt > 0:
                        Alt_List.append(float(mstr_list[0]))
                        Alt_Qty = float(mstr_list[1])
                    # print(mstr_list)
                    cnt += 1
                else:
                    break
            # avg_price = sum_price / 3
            # print("Alt qty:", alt_qty)
            # print("RAND:", sum_price)
            # print("max val:", max(sum_price))
            Max_Alt_Val = max(Alt_List)
            return Max_Alt_Val, Alt_Qty

    async def fetch_xe(self, session, url):
        async with session.get(url) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            eur_to_rand = 0
            # print(soup.prettify())
            elements = soup.find("p", class_="result__BigRate-sc-1bsijpp-1 dPdXSB")
            # print(elements.text)
            price = elements.text
            price = price.split(" ")
            price.pop(2)
            price.pop(1)
            # print(float(price[0]))
            eur_to_rand = float(price[0])
            return eur_to_rand

    async def fetch_kraken(self, session, url):

        async with session.get(url) as response:
            text = await response.text()
            return_list = []

            min_trade_bid = float("inf")
            last_trade_list = []
            last_trade_qty = 0
            # Check if the request was successful
            if response.status == 200:
                # Parse the JSON response
                # data = text.json()
                data = json.loads(text)
                # print(text)
                # Extract the last trade price from the response
                # The structure of the response might change, so adjust the keys accordingly

                last_trade_price = data["result"]["XXBTZEUR"]["c"][0]
                last_trade_price = float(last_trade_price)
                last_trade_list.append(last_trade_price)
                # print("Trade list", last_trade_list)
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
            # time.sleep(0.4)
        # print("List", last_trade_list)
        # print("min val", min_trade_bid)
        return last_trade_list, last_trade_qty

    async def main_alt(self):
        async with aiohttp.ClientSession() as session:
            task_alt = [self.fetch_alt(session, url_alt[0])]
            self.alt_data = await asyncio.gather(*task_alt)

    async def main_xe(self):
        async with aiohttp.ClientSession() as session:
            task_xe = [self.fetch_xe(session, url_xe[0])]
            self.xe_data = await asyncio.gather(*task_xe)

    async def main_kraken(self):
        async with aiohttp.ClientSession() as session:
            await asyncio.sleep(2)
            task_kraken = [self.fetch_kraken(session, url) for url in url_kraken]
            self.kraken_data = await asyncio.gather(*task_kraken)


url_xe = ["https://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=ZAR"]
url_alt = ["https://www.altcointrader.co.za/"]
url_kraken = ["https://api.kraken.com/0/public/Ticker?pair=XBTEUR"] * 10
scraper1 = AsyncWebScraper(url_alt)

scraper2 = AsyncWebScraper(url_xe)

scraper3 = AsyncWebScraper(url_kraken)

# asyncio.run(scraper1.main_alt())
# asyncio.run(scraper2.main_xe())
# asyncio.run(scraper3.main_kraken())

# Last_Kraken_Qty = 0
# Min_Kraken_Val = float("inf")
# for last_trade_list, last_trade_qty in scraper3.kraken_data:
#     Last_Kraken_Qty = last_trade_qty
#     if (last_trade_list[0] < Min_Kraken_Val) and (last_trade_list[0] != 0):
#         Min_Kraken_Val = last_trade_list[0]


def test_ftn(request):
    asyncio.run(scraper1.main_alt())
    asyncio.run(scraper2.main_xe())
    asyncio.run(scraper3.main_kraken())

    Last_Kraken_Qty = 0
    Min_Kraken_Val = float("inf")
    for last_trade_list, last_trade_qty in scraper3.kraken_data:
        Last_Kraken_Qty = last_trade_qty
        if (last_trade_list[0] < Min_Kraken_Val) and (last_trade_list[0] != 0):
            Min_Kraken_Val = last_trade_list[0]

    for Max_Alt_Val, Alt_Qty in scraper1.alt_data:
        altcoin_data = Max_Alt_Val
        alt_qty = Alt_Qty

    # print("Altcoin_max_bid:", altcoin_data)

    kraken_data = Min_Kraken_Val
    kraken_qty = Last_Kraken_Qty

    for eur_to_rand in scraper2.xe_data:
        fx_data = eur_to_rand

    kraken_price_inc_withdraw = kraken_data * (1.00015)
    interest = (
        (altcoin_data / fx_data) - (kraken_price_inc_withdraw)
    ) / kraken_price_inc_withdraw
    interest *= 100
    data = [
        {"name": "kraken", "data": kraken_price_inc_withdraw},
        {"name": "kraken_qty", "data": kraken_qty},
        {"name": "altcoin", "data": altcoin_data},
        {"name": "alt_qty", "data": alt_qty},
        {"name": "fx_data", "data": fx_data},
        {"name": "interest", "data": round(interest, 2)},
    ]

    return render(request, "trade/home.html", {"data": data})


# Rand_price = [{"price": str(get_data_altcoin())}]


def get_data(request):
    asyncio.run(scraper1.main_alt())
    asyncio.run(scraper2.main_xe())
    asyncio.run(scraper3.main_kraken())

    Last_Kraken_Qty = 0
    Min_Kraken_Val = float("inf")
    for last_trade_list, last_trade_qty in scraper3.kraken_data:
        Last_Kraken_Qty = last_trade_qty
        if (last_trade_list[0] < Min_Kraken_Val) and (last_trade_list[0] != 0):
            Min_Kraken_Val = last_trade_list[0]

    for Max_Alt_Val, Alt_Qty in scraper1.alt_data:
        altcoin_data = Max_Alt_Val
        alt_qty = Alt_Qty

    # print("Altcoin_max_bid:", altcoin_data)

    kraken_data = Min_Kraken_Val
    kraken_qty = Last_Kraken_Qty

    for eur_to_rand in scraper2.xe_data:
        fx_data = eur_to_rand

    kraken_price_inc_withdraw = kraken_data * (1.00015)
    interest = (
        (altcoin_data / fx_data) - (kraken_price_inc_withdraw)
    ) / kraken_price_inc_withdraw
    interest *= 100
    data = [
        {"name": "kraken", "data": kraken_price_inc_withdraw},
        {"name": "kraken_qty", "data": kraken_qty},
        {"name": "altcoin", "data": altcoin_data},
        {"name": "alt_qty", "data": alt_qty},
        {"name": "fx_data", "data": fx_data},
        {"name": "interest", "data": round(interest, 2)},
    ]
    return JsonResponse(data, safe=False)
