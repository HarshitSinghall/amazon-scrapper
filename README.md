# 🛒 Amazon Product Scraper

A powerful web scraping tool built with Python and Streamlit that extracts product information from Amazon India and exports data to Excel, CSV, or JSON formats.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)

## 📋 Features

- **Automated Scraping**: Extract product data from multiple Amazon pages
- **Flexible Data Extraction**: Choose which fields to extract (name, price, rating, links, images)
- **Multiple Export Formats**: Download data as Excel (.xlsx), CSV, or JSON
- **Data Preview**: View and filter extracted data in an interactive table
- **User-Friendly Interface**: Clean Streamlit interface with intuitive controls
- **Progress Tracking**: Real-time progress indicators during scraping
- **Error Handling**: Robust error handling with detailed error logs

## 🖼️ Screenshots

### Main Interface
The scraper tab allows you to configure and initiate scraping operations.

### Data Viewer
Preview extracted data with filtering and search capabilities.

### Download Options
Export your data in multiple formats with one click.

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- ChromeDriver (automatically managed by Selenium)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/HarshitSinghall/amazon-scrapper.git
cd amazon-product-scraper
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 📦 Dependencies

```txt
streamlit>=1.28.0
selenium>=4.15.0
beautifulsoup4>=4.12.0
pandas>=2.0.0
openpyxl>=3.1.0
```

## 🎯 Usage

### Quick Start

1. **Launch the application**:
   ```bash
   streamlit run app.py
   ```

2. **Configure scraping settings** in the sidebar:
   - Enter product keyword (e.g., "Laptops", "Mobile_Phones")
   - Set number of pages to scrape (1-20)
   - Select data fields to extract

3. **Scrape data**:
   - Click "🔍 Scrape & Extract" to collect new data
   - Or click "📊 Extract from Existing Files" to process saved HTML files

4. **View and download**:
   - Switch to the "Data Viewer" tab
   - Preview extracted products
   - Download in your preferred format

### Configuration Options

#### Sidebar Settings

- **Product Keyword**: Search term for Amazon products
- **Number of Pages**: How many result pages to scrape (1-20)
- **Data Fields**: Toggle which fields to extract:
  - Product Name
  - Price
  - Rating
  - Product Link
  - Image Link

### Data Extraction

The scraper extracts the following information:

| Field | Description |
|-------|-------------|
| Product Name | Full product title |
| Price | Product price in INR |
| Rating | Customer rating (out of 5 stars) |
| Product URL | Direct link to Amazon product page |
| Image URL | Product image link |
| Source File | Original HTML file name |

## 📂 Project Structure

```
amazon-product-scraper/
│
├── app.py              # Main Streamlit application
├── collector.py        # Web scraping functionality (Selenium)
├── extractor.py        # HTML parsing and data extraction (BeautifulSoup)
├── requirements.txt    # Project dependencies
├── README.md          # Project documentation
│
└── data/              # Scraped HTML files (auto-created)
    ├── Laptops_1.html
    ├── Laptops_2.html
    └── ...
```

## 🔧 How It Works

### 1. Data Collection (`collector.py`)
- Uses Selenium WebDriver to navigate Amazon pages
- Runs in headless Chrome mode for efficiency
- Extracts HTML content from product listings
- Saves individual product HTML files to `data/` folder
- Filters out empty or incomplete product entries

### 2. Data Extraction (`extractor.py`)
- Parses saved HTML files using BeautifulSoup
- Extracts product information based on user selection
- Handles missing data gracefully with "N/A" placeholders
- Compiles data into pandas DataFrame
- Tracks extraction statistics

### 3. User Interface (`app.py`)
- Provides intuitive Streamlit interface
- Manages scraping and extraction workflows
- Displays data in interactive tables
- Generates downloadable files in multiple formats
- Shows real-time progress and statistics

## ⚙️ Advanced Configuration

### Customizing Scraping Behavior

Edit `collector.py` to modify:
- Page load wait time (default: 3 seconds)
- Minimum HTML content size (default: 2500 characters)
- Browser options (e.g., add proxy, change user agent)

```python
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
```

### Customizing Data Extraction

Edit `extractor.py` to modify:
- HTML parsing selectors
- Data validation rules
- Output format

## 📊 Statistics Tracking

The application tracks:
- Total files processed
- Total products extracted
- Complete vs. incomplete records
- Missing data breakdown (names, prices, ratings, links, images)
- Processing errors

## 🐛 Troubleshooting

### Common Issues

**Issue**: ChromeDriver not found
```bash
Solution: Selenium 4+ manages ChromeDriver automatically. Ensure Chrome is installed.
```

**Issue**: Connection timeout
```bash
Solution: Increase sleep time in collector.py or check internet connection.
```

**Issue**: No products extracted
```bash
Solution: Amazon's HTML structure may have changed. Update CSS selectors in extractor.py.
```

**Issue**: Permission denied on data folder
```bash
Solution: Ensure write permissions for the project directory.
```

## ⚠️ Legal Disclaimer

This tool is for educational purposes only. Always review and comply with:
- Amazon's Terms of Service
- Amazon's robots.txt file
- Local laws regarding web scraping
- Data privacy regulations

**Responsible Usage**:
- Respect rate limits
- Don't overload Amazon's servers
- Use for personal research only
- Don't violate Amazon's Terms of Service

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 To-Do

- [ ] Add proxy support
- [ ] Implement rate limiting
- [ ] Add support for other Amazon domains (.com, .co.uk, etc.)
- [ ] Export to database (SQLite/PostgreSQL)
- [ ] Add scheduling for automated scraping
- [ ] Implement data visualization charts
- [ ] Add email notifications on completion



## 👤 Author

Harshit Singhal
- GitHub: [@HarshitSinghall](https://github.com/HarshitSinghall)
- Email: harshitsinghal822@gmail.com

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - For the amazing web framework
- [Selenium](https://www.selenium.dev/) - For browser automation
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - For HTML parsing
- [Pandas](https://pandas.pydata.org/) - For data manipulation


---

⭐ If you find this project helpful, please give it a star on GitHub!

**Note**: This tool is intended for educational purposes. Please use responsibly and ethically.

