import sys

def run_api():
    from src.api.app import app
    app.run(debug=True)

def run_scraper():
    from src.scripts.scraping_app import run_scraping
    run_scraping()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python run.py [api|scraper]")
        sys.exit(1)

    if sys.argv[1] == "api":
        run_api()
    elif sys.argv[1] == "scraper":
        run_scraper()
    else:
        print("Projeto inválido. Use 'api' ou 'scraper'.")
