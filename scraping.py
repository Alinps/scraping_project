import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

url = "https://books.toscrape.com/"



data = []
page = 1

    

while url:

    response = requests.get(url)

    response.encoding = "utf-8"

    if response.status_code == 200:
        print(f"fetched page {page} successfully")
    else:
        print(f"cant connect\nfailed url: {url}")
        page+=1
        break

    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article", class_="product_pod")

    print(f"processing page: {page}")

    for article in articles:

        book_title = article.find("h3").find("a")["title"] # type: ignore
        price =  article.find("p", class_="price_color").text # type: ignore
        rating = article.find("p", class_="star-rating")["class"][1] # type: ignore

        data.append({
            "title":book_title,
            "price":price,
            "rating":rating
        })

    next_button = soup.find("li",class_="next")

    if next_button:

        next_page = next_button.find("a")["href"] # type: ignore

        url = urljoin(url, next_page) # type: ignore
        page +=1

    else:

        url = None
        print("Scrapping finished...")

with open("products.json","w", encoding="utf-8") as file:
    json.dump(data, file, indent=4)
print("Data saved to products.json")


    



