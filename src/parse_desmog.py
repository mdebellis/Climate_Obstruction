import requests
from bs4 import BeautifulSoup
import json

def scrape_air_pollution_lobbying_database():
    base_url = "https://www.desmog.com"
    main_url = f"{base_url}/air-pollution-lobbying-database/"

    results = {}
    
    r = requests.get(main_url)
    soup = BeautifulSoup(r.text, "html.parser")
    
    entry_divs = soup.select(
        "div.display-view-entries.grid-view-entries.active div.display-view-entry.grid-view-entry.type-organization"
    )
    
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
        
        detail_response = requests.get(href)
        detail_soup = BeautifulSoup(detail_response.text, "html.parser")
        
        article = detail_soup.find("article")
        if not article:
            article = detail_soup
        
        company_details = {}
        
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
    
    return results

if __name__ == "__main__":
    data = scrape_air_pollution_lobbying_database()
    with open("scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
