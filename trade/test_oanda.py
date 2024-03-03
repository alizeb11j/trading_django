import requests
from bs4 import BeautifulSoup

# Fetch the web page
url = "https://www.xe.com/currencyconverter/convert/?Amount=1&From=EUR&To=USD"
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
print(float(price[0]))
