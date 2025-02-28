import uuid
from src.ag_api import *
from src.ag_api import find_property

last_name_prop = find_property(make_ontology_iri("last_name"))
first_name_prop = find_property(make_ontology_iri("first_name"))
middle_name_prop = find_property(make_ontology_iri("middle_name"))
person_class = find_class(make_gist_iri("Person"))
document_class = find_class(make_ontology_iri("Document"))
author_string_property = find_property(make_ontology_iri("author_string"))
author_property = find_property(make_ontology_iri("has_author"))


def create_author(last_name, first_name=None, middle_name=None):
    #This assumes that last_name is always bound
    if last_name is None: print("Error New person must have a last name") # This should exit the function
    author_iri = make_instance(str(uuid.uuid4()), person_class)
    put_value(author_iri, last_name_prop, last_name)
    if middle_name is not None: put_value(author_iri, middle_name_prop, middle_name)
    if first_name is not None:
        put_value(author_iri, first_name_prop, first_name)
        put_value(author_iri, rdfs_label_property,  first_name + " " + last_name)
    else:
        put_value(author_iri, rdfs_label_property, last_name)
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

# Checks if there are already author objects for the document
# and if there is a value for the author string, if there is an author string
# and there are no author objects then return the author string, otherwise return false
def find_author_string(document):
    document_author_string = get_value(document, author_string_property)
    document_authors = get_values(document, author_property)
    if document_author_string is None:
        return False
    elif document_authors:
        return False
    else: return document_author_string

def make_author_objects():
    documents = find_instances_of_class(document_class)
    for document in documents:
        document_authors = find_author_string(document)
        print(document_authors)
        if document_authors: parse_authors(convert_to_string(document_authors))


#make_author_objects()
#parse_authors("Justin Farrell")




