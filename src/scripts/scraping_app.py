import requests
from bs4 import BeautifulSoup
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

csv_path = os.path.join(DATA_DIR, "books_category.csv")

BASE_URL = "https://books.toscrape.com/"

def parse_rating(rating_class):
    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return ratings.get(rating_class, None)

def get_categories():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    categories = soup.select("div.side_categories ul li ul li a")
    category_links = {}
    for cat in categories:
        name = cat.get_text(strip=True)
        link = BASE_URL + cat["href"]
        category_links[name] = link
    return category_links

def scrape_category(category_name, category_url, writer):
    page_url = category_url
    while True:
        response = requests.get(page_url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.select("article.product_pod")
        if not books:
            break

        for book in books:
            title = book.h3.a["title"]
            price = book.select_one("p.price_color").get_text(strip=True)
            availability = book.select_one("p.availability").get_text(strip=True)
            rating_class = book.select_one("p.star-rating")["class"][1]
            rating = parse_rating(rating_class)
            image_url = BASE_URL + book.img["src"].replace("../", "")

            writer.writerow([title, price, rating, availability, category_name, image_url])
            
        next_page = soup.select_one("li.next a")
        if next_page:
            page_url = category_url.replace("index.html", "") + next_page["href"]
        else:
            break

def run_scraping():
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        # Header
        writer.writerow(["Título", "Preço", "Rating", "Disponibilidade", "Categoria", "Imagem"])

        categories = get_categories()
        for category_name, category_url in categories.items():
            print(f"Scraping categoria: {category_name}")
            scrape_category(category_name, category_url, writer)

    print("Scraping concluído! Os dados foram salvos em 'books_by_category.csv'.")