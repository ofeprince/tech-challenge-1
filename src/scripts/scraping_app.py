from src.shared import *
import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

csv_path = os.path.join(DATA_DIR, "books_category.csv")


def run_scraping():
    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        # Header
        writer.writerow(["Title", "Price", "Rating", "Availability", "Category", "Image source"])

        categories = get_categories()
        for category_name, category_url in categories.items():
            print(f"Scraping category: {category_name}")
            book_list = scrape_category(category_name, category_url)
            for book in book_list:
                writer.writerow([
                    book['title'],
                    book['price'],
                    book['rating'],
                    book['availability'],
                    book['category'],
                    book['image_src']
                ])

    print("Scraping completed! Data were saved in 'books_by_category.csv'.")