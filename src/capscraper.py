import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

def analyzecap(url):

    #URL = "https://www.asa.org.uk/rulings/repsol-sa-a23-1185942-repsol-sa.html"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    
    #with open("demofile2.txt", "w") as file:
    #    file.write(soup.prettify())
    # Extract sections based on headings
    sections = {
        "Background": "",
        "Ad description": "",
        "Issue": "",
        "Response": "",
        "Assessment": "",
        "Action": "",
    }

    mainheading = soup.find('h1', class_='heading')
    mainheadingtext = mainheading.get_text(strip=True).replace('\n', '').replace('\t', '')
    sections["label"] = mainheadingtext
    # Find all sub-headings
    headings = soup.find_all("h2", class_="font-color-grey")
    # Iterate through the headings and extract corresponding text
    for heading in headings:
        section_title = heading.get_text(strip=True)

        if section_title in sections:
            section_content = []
            next_element = heading.find_next_sibling()

            while next_element and next_element.name != "h2":
                section_content.append(next_element.get_text(strip=True))
                #section_content.append(", ")
                next_element = next_element.find_next_sibling()

            sections[section_title] = " ".join(section_content)

    def get_issue_text(soup):
        issue_heading = soup.find("h2", string="Issue")
        if issue_heading:
            issue_text = []
            next_element = issue_heading.next_sibling
            
            # Continue until we hit the next heading
            while next_element and (not isinstance(next_element, Tag) or next_element.name != "h2"):
                if isinstance(next_element, NavigableString):
                    text = next_element.strip()
                    if text:  # Only add non-empty text
                        issue_text.append(text)
                next_element = next_element.next_sibling
                
            return " ".join(issue_text)
        return ""
    if not sections['Issue']:
        sections['Issue'] = get_issue_text(soup)


    sidebar = soup.find("aside", class_="sidebar") #find sidebar
    complaint_ref = "Not Found"
    if sidebar:
        complaint_p = sidebar.find_all("p")
        for p in complaint_p:
            if "Complaint Ref:" in p.get_text():
                complaint_ref = p.find("strong", class_="pull-right").get_text(strip=True)
                break
    sections['id text'] = complaint_ref
    # Extract Related Rulings Links
    related_rulings = []
    for link in soup.select(".sidebar .icon-listing-item.mod-red a"):
        related_rulings.append(link["href"])
    sections['related rulings'] = ', '.join(related_rulings)

    same_comp_related_rulings = []
    for link in soup.select(".sidebar ul.icon-listing li.icon-listing-item h4.heading a"):
        same_comp_related_rulings.append(link["href"])
    sections['same_company_rulings'] = ', '.join(same_comp_related_rulings)

    cap_codes = []
    cap_code_section = soup.find("h2", class_="font-color-grey", string="CAP Code (Edition 12) ")
    if cap_code_section:
        cap_code_links = cap_code_section.find_next("p").find_all("a")
        cap_codes = [link.get_text(strip=True) for link in cap_code_links]


    bcap_codes = []
    bcap_code_section = soup.find("h2", class_="font-color-grey", string="BCAP Code")
    if bcap_code_section:
        bcap_code_links = bcap_code_section.find_next("p").find_all("a")
        bcap_codes = [link.get_text(strip=True) for link in bcap_code_links]
    
    bcap_codes_str = ", ".join(bcap_codes)
    sections['bcap_code'] = bcap_codes_str
    # Join CAP Codes with commas
    cap_codes_str = ", ".join(cap_codes)
    sections['cap_code'] = cap_codes_str
    sections['url'] = url
    return sections





#print(analyzecap("https://www.asa.org.uk/rulings/hurtigruten-uk-ltd-a24-1237378-hurtigruten-uk-ltd.html")['Issue'])