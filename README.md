# E-Commerce Laptop Data Engineering Pipeline

An automated end-to-end data engineering and analytics pipeline designed to extract, clean, and filter laptop listings from e-commerce GraphQL APIs (Tokopedia) to optimize budget-to-specification purchasing decisions.

## 🛠️ Tech Stack & Core Competencies
- **Data Mining & Extraction:** Reverse-engineering internal GraphQL APIs, handling anti-bot headers, and structural JSON payload manipulation using `requests` and `urllib`.
- **Data Wrangling & Cleaning:** Advanced data cleaning, attribute parsing, structural text conversion (`ast.literal_eval`), and pattern extraction via Regular Expressions (`re`) using `pandas` and `numpy`.
- **Development Environment:** Linux (Ubuntu 26.04 LTS), Virtual Environments (`venv`), Git Version Control, and Interactive Jupyter Notebooks (`.ipynb`).

## 📁 Project Architecture
```text
smart-laptop-finder/
├── data/                 # Stores raw and refined CSV datasets
├── src/
│   ├── engineering/      # Automated API scraper and data mining script
│   └── analytics/        # Interactive Jupyter Notebooks for data wrangling
├── .gitignore            # Excludes virtual environments and cache files
├── requirements.txt      # Project library dependencies
└── README.md             # Project documentation
```

## 🚀 Key Features Implemented
1. **Targeted Data Scraping:** Bypassed frontend rendering by targeting internal GraphQL API endpoints directly to gather product details (ID, title, price, shop, location).
2. **Advanced Regex Parsing:** Automated extraction of unstructured title tokens into explicit hardware attributes: `RAM_GB` and `Storage_Capacity_GB`.
3. **Data Imputation & Integrity:** Automatically resolved ambiguous storage formats and imputed missing types into designated `SSD` features based on capacity tokens.
4. **Noise Reduction Filtering:** Developed string contains matrices to permanently eliminate sponsored ads, accessories, and irrelevant listings, securing a 100% verified unit dataset.
