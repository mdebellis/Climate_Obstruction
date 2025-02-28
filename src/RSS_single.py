import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

#with open("rsssample.txt", "w") as file:
#    file.write(soup.prettify())


def extract_rss_case_details(url):
    #url = "https://climatecasechart.com/non-us-case/youth-climate-case-japan-for-tomorrow/"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    
    #title
    title = soup.find('h1', class_='entry-title').text.strip() if soup.find('h1', class_='entry-title') else None
    
    #filing data
    filing_date = soup.find('span', class_='label', string='Filing Date: ')
    filing_date = filing_date.find_next_sibling('span', class_='highlight').text.strip() if filing_date else None
    
    #reporter info
    reporter_info = soup.find('span', class_='label', string='Reporter Info: ')
    reporter_info = reporter_info.find_next_sibling('span', class_='highlight').text.strip() if reporter_info else None
    
    #status
    status = soup.find('span', class_='label', string='Status: ')
    status = status.find_next_sibling('span', class_='highlight').text.strip() if status else None
    
    #case categories
    case_categories = [a.text.strip() for a in soup.select('.entry-taxonomy.non_us_case_category .taxonomy-box a')]
    #jurisdictions
    jurisdictions = [a.text.strip() for a in soup.select('.entry-taxonomy.jurisdiction .taxonomy-box a')]
    
    #principal laws
    principal_laws = [a.text.strip() for a in soup.select('.entry-taxonomy.non_us_principal_law .taxonomy-box a')]
    
    #summary
    summary_div = soup.find('span', class_='label', string='Summary: ')
    summary = summary_div.find_next_sibling('p').text.strip() if summary_div else None
    
    #at issue
    at_issue_div = soup.find('span', class_='label', string='At Issue: ')
    at_issue = at_issue_div.find_next_sibling(text=True).strip() if at_issue_div else None
    
    #case documents
    case_documents_div = soup.find('div', class_='entry-documents')
    #print(case_documents_div)
    case_documents_p = case_documents_div.find('p') if case_documents_div else None
    case_documents = case_documents_p.text.strip() if case_documents_p else None
    def case_documents_allinfo():
        case_documents = []
        documents_section = soup.select_one('.entry-documents')
        
        if documents_section:
            if documents_section.find('em') and 'No case documents are available' in documents_section.find('em').text:
                case_documents = []
            else:
                for row in soup.select('.entry-documents tbody tr'):
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        case_documents.append({
                            'filing_date': cols[0].text.strip(),
                            'type': cols[1].text.strip(),
                            'file_link': cols[2].find('a')['href'].strip() if cols[2].find('a') else None,
                            'summary': cols[3].text.strip() if len(cols) > 3 else None
                        })
    
    
    if not case_documents or 'No case documents are available' not in case_documents:
        case_documents = []
        documents_section = soup.select_one('.entry-documents')
        
        if documents_section:
            if not (documents_section.find('em') and 'No case documents are available' in documents_section.find('em').text):
                for row in soup.select('.entry-documents tbody tr'):
                    link = row.find_all('td')[2].find('a')['href'].strip() if row.find_all('td')[2].find('a') else None
                    if link:
                        case_documents.append(link)
    
    
    return {
        'label': title,
        'year': filing_date,
        'reporter_info': reporter_info,
        'status': status,
        'case_categories': ', '.join(case_categories),
        'jurisdictions': ', '.join(jurisdictions),
        'principal_laws': ', '.join(principal_laws),
        'summary': summary,
        'at_issue': at_issue,
        'case_documents': ', '.join(case_documents) if type(case_documents) == list else case_documents,
        'url': url
    }

if __name__ == "__main__":
    print(extract_rss_case_details("https://climatecasechart.com/non-us-case/federal-environmental-agency-ibama-v-silmar-gomes-moreira/"))
    pass