import requests
from bs4 import BeautifulSoup


# Making a GET request
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
alt_qty = []
sum_price = []
for line in lines:
    if cnt < 11:
        mstr = line.text
        mstr_list = mstr.split("\n")
        mstr_list.pop(0)
        mstr_list.pop(3)

        if cnt > 0:
            sum_price.append(float(mstr_list[0]))
            alt_qty.append(float(mstr_list[1]))
        # print(mstr_list)
        cnt += 1
    else:
        break
# avg_price = sum_price / 3
print("Alt qty:", alt_qty)
print("RAND:", sum_price)
print("max val:", max(sum_price))
# return sum_price, alt_qty
