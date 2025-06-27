import csv
import uuid
import unicodedata
import re
from src.ag_api import *
from franz.openrdf.vocabulary import RDF, OWL
from franz.openrdf.vocabulary import RDF, RDFS
from franz.openrdf.model import URI, Literal

def get_expected_datatype(prop_iri):
    """
    Returns the expected datatype (as a URI) for a property if it's an owl:DatatypeProperty
    and the ontology defines an rdfs:range for it.
    Otherwise, returns None.
    """
    # Check if it's declared as a DatatypeProperty
    for _ in conn.getStatements(prop_iri, RDF.TYPE, conn.createURI("http://www.w3.org/2002/07/owl#DatatypeProperty"), None):
        # If it has a declared rdfs:range, return it
        for stmt in conn.getStatements(prop_iri, RDFS.RANGE, None, None):
            return stmt.getObject()

    return None  # Means it's either an object property or no range declared


csv_path = r"ci7.csv"
# file_class is the IRI for the class that the properties in the csv file apply to. I.e.,
# when parsing the file, the system will search for an instance of that class and if one is
# not found, then it will be created.
file_class_str = "https://www.michaeldebellis.com/climate_obstruction/Report"
file_class = conn.createURI(file_class_str)

def is_object_property(prop_iri):
    """
    Returns True if the given IRI is rdf:type or declared as an owl:ObjectProperty in the AllegroGraph repo.
    """
    if prop_iri == RDF.TYPE:
        return True
    # Correct constant is OWL.OBJECTPROPERTY (not OWL.OBJECT_PROPERTY)
    for _ in conn.getStatements(prop_iri, RDF.TYPE, OWL.OBJECTPROPERTY, None):
        return True
    return False

# Remove weird characters resulting from scraping
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

# Remove weird characters resulting from scraping
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

# Reads a CSV file where the first row defines property IRIs
# Each subsequent row describes an instance with values for those properties
# This function currently assumes all individuals are new (i.e., created with UUIDs)
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
                # If any header does not map to a known property, print an error and abort
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
                print(f'New Object Line {line_count}')
                new_iri = conn.createURI(
                    ontology_string + str(uuid.uuid4()))
                # conn.add(new_iri, RDF.TYPE, file_class)
                conn.add(new_iri, RDF.TYPE, owl_named_individual)
                print(f'New individual {new_iri}')
                while i < row_count:
                    nextval = row[i]
                    # if next value is empty go to the next column
                    if nextval == "":
                        i += 1
                        continue
                    property_iri = proplist[i]
                    # If the property is an object property, convert the value to an IRI
                    if is_object_property(property_iri):
                        nextval = conn.createURI(nextval)
                    else:
                        # If we get here, it's a data property. If a datatype is defined, convert the value accordingly, otherwise the default is treat as a string
                        if "^^xsd" in nextval:
                            # Assume it's already a properly typed literal, add as-is
                            pass  # nextval stays unchanged
                        else:
                            datatype = get_expected_datatype(property_iri)
                            if datatype:
                                print(f'coercing {nextval} to datatype {datatype}')
                                nextval = conn.createLiteral(nextval, datatype=datatype)
                            # If we get here it's a string and we want to remove crud that makes it hard to read
                            else:
                                nextval = clean_text(nextval)
                    conn.add(new_iri, property_iri, nextval)
                    i += 1
                line_count += 1
        print(f'Processed {line_count} lines.')


read_csv(csv_path)

