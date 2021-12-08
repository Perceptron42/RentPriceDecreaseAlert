from bs4 import BeautifulSoup
from twilio.rest import Client
import requests
import random
import time
import json

HEADER = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            }

# GET THE DETAILS OF FOLLOWING TWO VARIABLES FROM YOUR TWILIO ACCOUNT
account_sid = '[]'
auth_token = '[]'


def get_min_price_from_zillow(url):
    response = requests.get(url, headers=HEADER)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    clean_prices = []
    all_price_elements = soup.find_all('div', "units-table__text--sectionheading")

    all_prices = [price.get_text() for price in all_price_elements]

    #all_prices = ['$1,302 - $1,352', '$1,433 - $2,003', '$2,067 - $2,592', "$900", "$1,234"]
    print(f'all prices variable is{all_prices}')

    for price in all_prices:
        if len(price) > 6: #means range
            clean_prices.append(price[1:6])
        else:
            clean_prices.append(price[1:])

    print(clean_prices)
    # flat_list = [item for sublist in clean_prices for item in sublist]
    # print(flat_list)

    for i in range(len(clean_prices)):
        clean_prices[i] = clean_prices[i].replace(',','')
        clean_prices[i] = int(clean_prices[i])
    print(clean_prices)

    print(min(clean_prices))
    delay = random.randint(25, 45)
    time.sleep(delay)
    return min(clean_prices)


# ENTER your apartment links and their nick names here
zillow_links = {'standard': "https://www.zillow.com/b/the-standard-at-domain-northside-austin-tx-65fTZt/",
                'gallery': "https://www.zillow.com/b/gallery-at-domain-austin-tx-65Xx3D/",
                'addison': "https://www.zillow.com/b/addison-at-kramer-station-austin-tx-5h5mRJ/"}

zillow_prices = {}

# "https://www.zillow.com/b/residences-at-the-domain-austin-tx-5Xht9M/",
# "https://www.zillow.com/b/the-kenzie-at-the-domain-austin-tx-5g4RfH/",
# "https://www.zillow.com/b/imt-at-the-domain-austin-tx-5Xht35/",
# "https://www.zillow.com/b/flatiron-domain-austin-tx-B6n86c/",

#shuffling the links by first shuffling the list of keys
keys_of_zillow = list(zillow_links.keys())
random.shuffle(keys_of_zillow)

shuffled_zillow_links = dict()
for key in keys_of_zillow:
    shuffled_zillow_links.update({key: zillow_links[key]})

for keys, value in shuffled_zillow_links.items():
    #get_min_price_from_zillow(link)
    zillow_prices[keys] = get_min_price_from_zillow(value)

result = json.dumps(zillow_prices)
print(result)
final_message = f'Minimum rents right now {result}'

client = Client(account_sid, auth_token)
message = client.messages.create(
            body=final_message,
            from_="[ENTER YOUR TWILIO 'FROM' PHONE NUMBER HERE]",
            to='[ENTER YOUR PHONE NUMER WHERE YOU WANT TO SEND ALERTS]'
            )
