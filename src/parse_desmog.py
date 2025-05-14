import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import os

def scrape_desmog_database(database_url):
    """
    Scrape a DeSmog database and return the structured data
    
    Args:
        database_url: URL path of the database to scrape
        
    Returns:
        tuple: (data dictionary, full database URL)
    """
    print(f"Scraping database: {database_url}")
    base_url = "https://www.desmog.com"
    
    # Ensure the URL is complete
    if not database_url.startswith("http"):
        full_url = base_url + database_url
    else:
        full_url = database_url
    
    results = {}
    
    try:
        r = requests.get(full_url)
        r.raise_for_status()  # Raise exception for 4XX/5XX responses
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Find all organization entries
        entry_divs = soup.select(
            "div.display-view-entries.grid-view-entries.active div.display-view-entry.grid-view-entry.type-organization"
        )
        
        print(f"Found {len(entry_divs)} organizations")
        
        for entry in entry_divs:
            link_tag = entry.find("a")
            if not link_tag:
                continue
            
            href = link_tag.get("href")
            if href and not href.startswith("http"):
                href = base_url + href
            
            company_name = link_tag.get_text(strip=True)
            if not company_name:
                company_name = "Unknown"
            
            print(f"Processing: {company_name}")
            
            try:
                detail_response = requests.get(href)
                detail_response.raise_for_status()
                detail_soup = BeautifulSoup(detail_response.text, "html.parser")
                
                article = detail_soup.find("article")
                if not article:
                    article = detail_soup
                
                company_details = {}
                # Add the organization's URL to the details
                company_details["URL"] = href
                
                headers = article.find_all(["h2", "h3"])
                
                for header in headers:
                    header_text = header.get_text(strip=True)
                    
                    paragraph_texts = []
                    sibling = header.find_next_sibling()
                    
                    while sibling and sibling.name not in ["h2", "h3"]:
                        if sibling.name == "p":
                            paragraph_texts.append(sibling.get_text(strip=True))
                        sibling = sibling.find_next_sibling()
                    
                    combined_paragraphs = "\n".join(paragraph_texts)
                    
                    if header_text:
                        company_details[header_text] = combined_paragraphs
                
                results[company_name] = company_details
                
                # Be nice to the server with a small delay
                time.sleep(1)
            
            except Exception as e:
                print(f"Error processing {company_name}: {str(e)}")
        
        return results, full_url
    
    except Exception as e:
        print(f"Error scraping database {database_url}: {str(e)}")
        return {}, full_url

def save_to_csv(data, database_url, output_file):
    """
    Save the scraped data to a CSV file
    
    Args:
        data: Dictionary of organization data
        database_url: URL of the source database
        output_file: Path to output CSV file
    """
    # Get all possible field names from all entries
    all_fields = set()
    for org_data in data.values():
        all_fields.update(org_data.keys())
    
    # Create fieldnames list with 'Organization' first, then all other fields sorted, and 'Source_URL' last
    fieldnames = ['Organization'] + sorted(list(all_fields)) + ['Source_URL']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Write each organization's data
        for org_name, org_data in data.items():
            row = {'Organization': org_name, 'Source_URL': database_url}
            for field, value in org_data.items():
                row[field] = value
            writer.writerow(row)
    
    print(f"Data saved to {output_file}")

def get_all_desmog_databases():
    """
    Get a list of all DeSmog database URLs by scraping the main databases page
    
    Returns:
        list: List of database URL paths
    """
    try:
        response = requests.get("https://www.desmog.com/databases/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all database links
        database_links = []
        
        # Find database links in the page (actual selector might need to be adjusted)
        links = soup.select("a.database-link")  # Adjust this selector based on actual page structure
        
        for link in links:
            href = link.get("href")
            if href and "/database/" in href:
                database_links.append(href)
        
        # Fallback to hardcoded list if nothing found
        if not database_links:
            database_links = [
                "/air-pollution-lobbying-database/",
                "/agribusiness-database/",
                "/climate-disinformation-database/",
                "/net-zero-scrutiny-group-database/",
                "/conservatives-net-zero-research-group-database/",
                "/cost-of-net-zero-database/"
            ]
        
        return database_links
    
    except Exception as e:
        print(f"Error getting database list: {str(e)}")
        # Return default list in case of error
        return [
            "/air-pollution-lobbying-database/",
            "/agribusiness-database/",
            "/climate-disinformation-database/",
            "/net-zero-scrutiny-group-database/",
            "/conservatives-net-zero-research-group-database/",
            "/cost-of-net-zero-database/"
        ]

def convert_json_to_csv(json_file, output_csv, database_url=None):
    """
    Convert an existing JSON file to CSV format
    
    Args:
        json_file: Path to input JSON file
        output_csv: Path to output CSV file
        database_url: URL of the source database (optional)
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # If URL is not provided, use a default
        if not database_url:
            database_url = "https://www.desmog.com/databases/"
        
        # For existing JSON data, we need to add the URL field for each organization
        # Extract domain/country from the company name if it exists
        base_url = "https://www.desmog.com"
        for org_name, org_data in data.items():
            # Add URL field if it doesn't exist
            if "URL" not in org_data:
                # Remove potential country suffix from organization name to create URL slug
                clean_name = org_name
                if "United Kingdom" in org_name:
                    clean_name = org_name.replace("United Kingdom", "").strip()
                
                # Convert organization name to URL slug format
                slug = clean_name.lower().replace(" ", "-")
                # Strip any non-alphanumeric/hyphen characters
                slug = ''.join(c for c in slug if c.isalnum() or c == '-')
                
                # Create a plausible URL (this is an approximation)
                org_url = f"{base_url}/air-pollution-{slug}/"
                org_data["URL"] = org_url
        
        save_to_csv(data, database_url, output_csv)
        return True
    
    except Exception as e:
        print(f"Error converting JSON to CSV: {str(e)}")
        return False

def main():
    # Create output directory if it doesn't exist
    os.makedirs("desmog_data", exist_ok=True)
    
    # Get all databases to scrape
    databases = get_all_desmog_databases()
    print(f"Found {len(databases)} databases to scrape")
    
    # Process each database
    for index, db_url in enumerate(databases):
        # Create safe filename from the URL
        db_name = db_url.strip('/').split('/')[-1]
        if not db_name:
            db_name = f"database_{index+1}"
        
        output_base = os.path.join("desmog_data", db_name)
        
        # Scrape the database
        data, full_url = scrape_desmog_database(db_url)
        
        if data:
            # Save as CSV
            save_to_csv(data, full_url, f"{output_base}.csv")
            
            # Also save raw JSON for backup/debugging
            with open(f"{output_base}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"Saved data for {db_name}")
        else:
            print(f"No data found for {db_name}")
        
        # Pause between databases to be nice to the server
        if index < len(databases) - 1:
            print("Pausing before next database...")
            time.sleep(5)
    
    print("All databases processed.")

# For converting an existing JSON file
def convert_existing_json():
    convert_json_to_csv(
        "scraped_data.json", 
        "air_pollution_database.csv",
        "https://www.desmog.com/air-pollution-lobbying-database/"
    )
    print("Converted existing JSON to CSV")

if __name__ == "__main__":
    # Uncomment one of the following based on what you want to do:
    
    # Option 1: Process all databases from scratch
    main()
    
    # Option 2: Convert an existing JSON file to CSV
    #convert_existing_json()