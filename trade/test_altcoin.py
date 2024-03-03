import requests
from bs4 import BeautifulSoup


# Making a GET request
r = requests.get("https://www.altcointrader.co.za/")

# Parsing the HTML
soup = BeautifulSoup(r.content, "html.parser")

# print(soup.prettify())
s = soup.find("div", id="sell-orders")
lines = s.find_all("tr")
print("no of values:", len(lines))
Sell_object = {}
Sell_object["Price"] = []
cnt = 0
avg_price = 0
sum_price = 0
for line in lines:
    if cnt < 2:
        mstr = line.text
        mstr_list = mstr.split("\n")
        mstr_list.pop(0)
        mstr_list.pop(3)

        if cnt > 0:
            sum_price += float(mstr_list[0])
        print(mstr_list)
        cnt += 1
    else:
        break
# avg_price = sum_price / 3
# print(avg_price)
print(sum_price)
