from src.ag_api import *
import uuid
import document_parser as dp
import os
import csv
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options


# Create a connection object and bind to conn. The conn object is used to connect with an AllegroGraph repository


# Set up variables bound to various classes and properties needed for this file
document_class = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/Document")
text_prop = conn.createURI("https://www.michaeldebellis.com/climate_obstruction/text")
iri_prop = conn.createURI("http://purl.org/ontology/bibo/uri")
heading_prop = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#heading")
source_document = conn.createURI(
    "http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#SearchUsingLLMAndOntology")
test_document1 = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#25ecc441-690e-4743-8350-cf5e177fa696")
test_document2 = conn.createURI("http://www.semanticweb.org/ontologies/2022/titutuli/nivedita/drmo#642d4db4-25a0-41fa-a635-3b722c533f1e")
test_document3 = conn.createURI("https://www.sciencedirect.com/science/article/pii/S0109564123000209")

directory_path = 'Corpus/Processed Corpus Docs/'

sciencedirect_link_pattern = re.compile(r'https?://www\.sciencedirect\.com/science/article/pii/\S+')


 # Enables headless mode


service = Service(ChromeDriverManager().install())



def get_url_for_document(document):
    url_string = get_value(document, iri_prop)
    if url_string is None:
        return None
    else:
        return convert_to_string(url_string)


# This iterates over all documents and checks if the document has sub sections or a value for the text field
# Note: need to run the reasoner to make sure this works because most doccuments are instances of JournalArticle
# or some other subclass of Document. To get all the actual documents the reasoner needs to run to assert those additional
# instance links. I.e., without the reasoner the graph only knows that an instance of JournalArticle is an instance of JournalArticle
# to know that it is also an instance of Document (superclass of JournalArticle) we need the reasoner
def add_sections_for_documents():
    doc_statements = conn.getStatements(None, RDF.TYPE, document_class)
    with doc_statements:
        for doc_statement in doc_statements:
            next_document = doc_statement.getSubject()
            doc_text = get_value(next_document, text_prop)
            doc_segments = conn.getStatements(next_document, sub_section_prop, None)
            if doc_text is None and len(doc_segments) == 0:
                driver = webdriver.Chrome(service=service)
                build_sections_for_document(driver,next_document)
                
                
            else:
                print("Document already has content:", next_document)


def extract_sciencedirect_links_from_directory(directory_path):
    all_links = []
    # List all files in the specified directory
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):  # Check for .csv extension
            # Construct full file path
            file_path = os.path.join(directory_path, file_name)
            # Extract links from this CSV file
            links = extract_sciencedirect_links(file_path)
            # Extend the list of all links with links from this file
            all_links.extend(links)
    return all_links

# Function to extract ScienceDirect links from a single CSV file
def extract_sciencedirect_links(csv_file_path):
    links = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            for cell in row:
                links.extend(sciencedirect_link_pattern.findall(cell))
    return links

def create_sub_section(document, heading=None, text=None):
    sub_section = conn.createURI(domain_ont_str + str(uuid.uuid4()))
    conn.add(sub_section, RDF.TYPE, section_class)
    if heading is not None:
        conn.add(sub_section, heading_prop, heading)
        conn.add(sub_section, rdfs_label_prop, heading)
    if text is not None:
        conn.add(sub_section, text_prop, text)
    conn.add(document, sub_section_prop, sub_section)
    return sub_section

# This function is used to build the sections for a document. It uses the document parser to get the sections

def build_sections_for_document(driver, documentObject):
    counter = 0
    start_time = time.time()
    document_url = get_url_for_document(documentObject)
    document_url = document_url[1:]
    documentDict = dp.parseDocuments(document_url,driver) 
    
    if(documentDict != False):
        doc_secs_texts = list(documentDict.values())
        doc_secs = list(documentDict.keys())
        for i in range(len(doc_secs)):
            section = create_sub_section(documentObject, doc_secs[i], doc_secs_texts[i])
        end_time = time.time()
        duration = end_time - start_time
        print(duration)
        print("Esimtated time remaining: ", ((duration*1000) - (counter*8)) / 60, " minutes")
    else:
        print("Skipped parsing")

   
    driver.quit()
    




add_sections_for_documents()
