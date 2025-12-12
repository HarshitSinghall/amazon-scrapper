from bs4 import BeautifulSoup
import os
import html
import pandas as pd

def extract_data(data_folder, is_name=True, is_price=True, is_link=True, is_rating=True, is_img=True):
    """Extract product data from HTML files and return as DataFrame"""
    
    products = []
    stats = {
        'missing_names': 0,
        'missing_prices': 0,
        'missing_ratings': 0,
        'missing_links': 0,
        'missing_images': 0,
        'errors': 0,
        'complete_records': 0,
        'total_files': 0
    }
    
    for file in os.listdir(data_folder):
        try:
            if file.endswith(".html"):
                stats['total_files'] += 1
                
                with open(f"{data_folder}/{file}", 'r', encoding='utf-8', errors='ignore') as f:
                    html_content = f.read()
                
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Initialize variables
                name = "N/A"
                price = "N/A"
                rating = "N/A"
                full_url = "N/A"
                img_link = "N/A"
                
                # Extract name
                if is_name:
                    t = soup.find("h2")
                    name = t.get_text().strip() if t else "N/A"
                
                # Extract price
                if is_price:
                    div = soup.find("div", attrs={"data-csa-c-price-to-pay": True})
                    price = div.get("data-csa-c-price-to-pay") if div else "N/A"
                
                # Extract rating
                if is_rating:
                    div = soup.find("div", class_="a-row a-size-small")
                    rating = div.get_text().strip() if div else "N/A"
                
                # Extract link
                if is_link:
                    link_tag = soup.find("a", class_="a-link-normal s-no-outline")
                    if link_tag:
                        href = link_tag.get("href")
                        clean_href = html.unescape(href)
                        full_url = f"https://www.amazon.in{clean_href}"
                
                # Extract image
                if is_img:
                    img = soup.find("img", class_="s-image")
                    img_link = img.get("src") if img else "N/A"
                
                # Track missing data
                if name == "N/A":
                    stats['missing_names'] += 1
                if price == "N/A":
                    stats['missing_prices'] += 1
                if rating == "N/A":
                    stats['missing_ratings'] += 1
                if full_url == "N/A":
                    stats['missing_links'] += 1
                if img_link == "N/A":
                    stats['missing_images'] += 1
                
                # Check if record is complete
                if all([name != "N/A", price != "N/A", rating != "N/A", 
                       full_url != "N/A", img_link != "N/A"]):
                    stats['complete_records'] += 1
                    # Add to products list
                    products.append({
                        'Product Name': name,
                        'Price': price,
                        'Rating': rating,
                        'Product URL': full_url,
                        'Image URL': img_link,
                        'Source File': file
                    })
                
                
                
        except Exception as e:
            stats['errors'] += 1
            print(f"Error processing file {file}: {e}")
    
    # Convert to DataFrame
    df = pd.DataFrame(products)
    
    # Print statistics
    print("\n" + "="*50)
    print("EXTRACTION STATISTICS")
    print("="*50)
    print(f"Total files processed: {stats['total_files']}")
    print(f"Total products extracted: {len(df)}")
    print(f"Complete records: {stats['complete_records']}")
    print(f"\nMissing Data:")
    print(f"  - Names: {stats['missing_names']}")
    print(f"  - Prices: {stats['missing_prices']}")
    print(f"  - Ratings: {stats['missing_ratings']}")
    print(f"  - Links: {stats['missing_links']}")
    print(f"  - Images: {stats['missing_images']}")
    print(f"  - Errors: {stats['errors']}")
    print("="*50 + "\n")
    
    return df, stats