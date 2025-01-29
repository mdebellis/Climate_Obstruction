import uuid
from src.ag_api import *

last_name_prop = find_property(make_ontology_iri("last_name"))
first_name_prop = find_property(make_ontology_iri("first_name"))
middle_name_prop = find_property(make_ontology_iri("middle_name"))
person_class = find_class(make_gist_iri("Person"))

def create_author(last_name, first_name=None, middle_name=None):
    if last_name is None: print("Error New person must have a last name") # This should exit the function
    author_iri = make_instance(str(uuid.uuid4()), person_class)
    put_value(author_iri, last_name_prop, last_name)
    put_value(author_iri, first_name_prop, first_name)
    if middle_name is not None: put_value(author_iri, middle_name_prop, middle_name)
    if first_name is not None: put_value(author_iri, first_name_prop, first_name)
    return author_iri


def parse_authors(authors_string):
    # Just a basic start, ignoring middle names and many alternative patterns
    authors = authors_string.split(";")  # Split authors by semicolon
    author_list = []
    for author in authors:
        name_parts = author.split(",")  # Split each author by comma
        last = name_parts[0].strip()  # Get the last name and strip whitespace
        first = name_parts[1].strip()
        author_iri = create_author(last_name=last, first_name=first)
        author_list.append(author_iri)  # Add the created author's IRI to the list
    return author_list




