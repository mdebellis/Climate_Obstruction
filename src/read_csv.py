import csv
import uuid
import unicodedata
import re
from src.ag_api import *

csv_path = "apdb.csv"
# file_class is the IRI for the class that the properties in the csv file apply to. I.e.,
# when parsing the file, the system will search for an instance of that class and if one is
# not found, then it will be created.
file_class_str = "https://www.michaeldebellis.com/climate_obstruction/Trade_Association"
file_class = conn.createURI(file_class_str)

def fix_encoding(text):
    if not isinstance(text, str):
        return text  # If not a string, return it as-is
    try:
        # First attempt decoding as UTF-8 (commonly expected encoding)
        return text.encode('utf-8').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        try:
            # Fallback to decoding as Latin-1 if UTF-8 fails
            return text.encode('latin1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            # If both fail, return the original text
            return text

def normalize_text(text):
    if not isinstance(text, str):
        return text
    text = unicodedata.normalize('NFKC', text)
    text = text.replace('\u00A0', ' ')  # Replace non-breaking space
    text = re.sub(r'\s+', ' ', text)    # Collapse extra whitespace
    return text.strip()

# This and previous 3 functions are to remove weird characters resulting from scraping
def clean_text(text):
    return normalize_text(fix_encoding(text))

# Reads a CSV file where the first line is a list of properties
# Each subsequent line is an instance of some class that is the domain for each property
# This function can generalize although for now it assumes that the CSV file contains instances
# of the NGORecpient class. Enhancements: 1) write a function to check that the data property exists
# 2) Find the range of the data property if it exists and coerce the literal into that datatype if the
# data property doesn't exist or the literal can't be coerced signal an error.
def read_csv(path):
    with open(path, mode='r', encoding='utf-8', errors='ignore') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        proplist = []
        for row in csv_reader:
            row_count = len(row)
            i = 0
            if line_count == 0:
                # Process the first row of property names. Convert each word to a property and put the
                # property in proplist in the same order so for the subsequent rows, row[i] goes in proplist[i]
                # the first column is the ID property that uniquely identifies each instance and determines if an
                # individual already exists for that row, in which case add the data to that existing individual
                while i < row_count:
                    p = find_property(row[i])
                    if p:
                        proplist.append(p)
                    else:
                        print(f'unknown property in column: {i}')
                        return
                    i += 1
                line_count += 1
                print(f'prop list: {proplist}')
            else:
                # If the Individual doesn't exist then it will be created
                print(f'New Object Line {line_count}')
                new_iri = conn.createURI(
                    ontology_string + str(uuid.uuid4()))
                conn.add(new_iri, RDF.TYPE, file_class)
                conn.add(new_iri, RDF.TYPE, owl_named_individual)
                print(f'New individual {new_iri}')
                while i < row_count:
                    nextval = row[i]
                    nextval = clean_text(nextval)
                    if nextval != "":
                        conn.add(new_iri, proplist[i], nextval)
                    i += 1
                line_count += 1
        print(f'Processed {line_count} lines.')


read_csv(csv_path)

