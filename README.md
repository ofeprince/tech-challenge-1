# Tech Challenge 1

A Flask-based web application that provides an API for managing books and categories, along with a web scraping system to collect book data from an external source. The project demonstrates a modular architecture with authentication, database integration, and data scraping capabilities.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Scraper System](#scraper-system)
- [Architecture Plan](#architecture-plan)
- [License](#license)

## Features

### API Features
- **User Authentication**: JWT-based authentication with login and token refresh endpoints.
- **Book Management**: Retrieve books, search by title or category, and get individual book details.
- **Category Management**: List all available book categories.
- **Scraping Integration**: Trigger web scraping via API endpoint.
- **Health Check**: Database connectivity verification.
- **Swagger Documentation**: Interactive API documentation at `/apidocs/`.

### Scraper Features
- **Automated Data Collection**: Scrapes book data from an external website, including titles, prices, ratings, availability, and images.
- **Category-Based Scraping**: Processes multiple categories and saves data to CSV.
- **Data Persistence**: Outputs structured CSV file for further analysis or import.

## Project Structure

The project follows a modular architecture organized as follows:

```
src/
├── api/                    # Flask application core
│   ├── app.py             # Main Flask app with configurations and blueprints
│   ├── config.py          # Application configuration (database, JWT, etc.)
│   ├── extensions.py      # Flask extensions (SQLAlchemy, JWT, Swagger)
│   └── routes/            # API route handlers
│       ├── auth.py        # Authentication endpoints
│       ├── books.py       # Book-related endpoints
│       ├── categories.py  # Category endpoints
│       └── scraping.py    # Scraping trigger endpoint
├── data/
│   ├── db/               # Database files (SQLite)
│   └── raw/              # Raw data storage (CSV outputs)
├── models/               # SQLAlchemy models
│   ├── book.py           # Book model
│   ├── category.py       # Category model
│   └── user.py           # User model
├── scripts/              # Standalone scripts
│   └── scraping_app.py   # Web scraping script
└── shared/               # Shared utilities
    └── scraper.py        # Scraping functions
```

This structure separates concerns: API logic in `api/`, data models in `models/`, scripts in `scripts/`, and shared code in `shared/`. The `data/` directory handles both database and raw data outputs.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ofeprince/tech-challenge-1.git
   cd tech-challenge-1
   ```
2. Create a python virtual environment and active it
    ```bash
    # Windows sample. Search for how to do it on Mac
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure you have Python 3.8+ installed.

## Running the Application

The application can be run in two modes: API server or scraper script. Use the `run.py` script with the appropriate argument.

### Running the API
Create a .env file in the root folder to configure environment variables. Check the .env-sample file:
```code
USER_ADMIN=ADM_USER_FOR_TESTING_JWT_AUTH
PASS_ADMIN=USER_PASSWORD
JWT_SECRET=JWT_SECRET
SECRET_KEY=KEY_SECRET
SWAGGER_TITLE=SWAGGER_TITLE_FOR_API_PROJECT
```

To start the Flask API server:
```bash
python run.py api
```

The server will start on `http://127.0.0.1:5000` (default Flask port). Access the API documentation at `http://127.0.0.1:5000/apidocs/`.

### Running the Scraper
To execute the web scraping script:
```bash
python run.py scraper
```

This will scrape book data and save it to `data/raw/books_category.csv`.

## API Endpoints

The API uses JWT authentication for protected endpoints. Obtain a token via the login endpoint and include it in the `Authorization` header as `Bearer <token>`.

### Authentication Endpoints
- **POST /api/v1/auth/login**
  - Authenticates a user and returns access and refresh tokens.
  - Body: `{"username": "string", "password": "string"}`

- **POST /api/v1/auth/refresh**
  - Refreshes the access token using a refresh token.
  - Requires refresh token in Authorization header.

### Book Endpoints
- **GET /api/v1/books/**
  - Returns a list of all books.
  - Response: Array of book objects with id, title, price, rating, availability, image_src, category_id.

- **GET /api/v1/books/search**
  - Searches books by title or category.
  - Query params: `title` (string), `category` (string).
  - Response: Filtered array of book objects.

- **GET /api/v1/books/{book_id}**
  - Returns details of a specific book by ID.
  - Response: Single book object.

### Category Endpoints
- **GET /api/v1/categories/**
  - Returns a list of all categories.
  - Response: Array of category objects.

### Scraping Endpoints
- **POST /api/v1/scraping/execute**
  - Triggers the web scraping process.
  - Requires authentication.

### Health Check
- **GET /api/v1/health**
  - Checks database connectivity.
  - Response: `{"status": "healthy", "database": "connected"}`

## Scraper System

The scraper system collects book data from an external website and saves it to a CSV file.

### How to Run
Execute the scraper using:
```bash
python run.py scraper
```

### Process
1. Retrieves available categories from the target website.
2. For each category, scrapes book details including title, price, rating, availability, and image source.
3. Saves all data to `data/raw/books_category.csv` with the following columns:
   - Title
   - Price
   - Rating
   - Availability
   - Category
   - Image source

### Output Location
The generated CSV file is located at `data/raw/books_category.csv`. This file can be used for data analysis, import into the database, or further processing.

## Architecture Plan

This section outlines a data pipeline leveraging the API and scraper components, demonstrating how a data scientist can utilize the system for data collection, processing, and analysis.

### Data Pipeline Overview

The architecture follows an ETL (Extract, Transform, Load) pattern:

1. **Extract**: The scraper collects raw book data from external sources.
2. **Transform**: Data is structured and stored in CSV format, with potential for database integration.
3. **Load**: The API provides programmatic access to processed data for consumption.

### Data Scientist Workflow

A data scientist can benefit from this solution in several ways:

- **Data Collection**: Use the scraper to gather large datasets of book information without manual effort.
- **API Integration**: Build automated pipelines that query the API for real-time data access.
- **Data Analysis**: Combine scraped data with API responses for comprehensive analysis.
- **Machine Learning**: Use collected data for training models (e.g., price prediction, recommendation systems).
- **Monitoring**: Leverage the health check endpoint for pipeline reliability monitoring.


### Pipeline Benefits

- **Scalability**: Scraper can handle multiple categories and large volumes of data.
- **Flexibility**: API allows for custom queries and integrations.
- **Automation**: Scheduled scraping jobs can keep data fresh.
- **Security**: JWT authentication protects API endpoints.
- **Documentation**: Swagger provides clear API specifications for integration.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
