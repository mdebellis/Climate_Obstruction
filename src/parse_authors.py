import uuid

from src.ag_api import *
last_name_prop = find_property(make_ontology_iri("last_name"))
first_name_prop = find_property(make_ontology_iri("first_name"))
middle_name_prop = find_property(make_ontology_iri("middle_name"))

def create_author(last_name, first_name=None, middle_name=None):
    if last_name is None: print("Error New person must have a last name") # This should exit the function
    author_iri = conn.createURI(make_ontology_iri(uuid.uuid4()))
    person_class = find_class(make_gist_iri("Person"))
    put_value(author_iri, last_name_prop, last_name)
    put_value(author_iri, first_name_prop, first_name)
    if middle_name is not None: put_value(author_iri, middle_name_prop, middle_name)
    if first_name is not None: put_value(author_iri, first_name_prop, first_name)
    return author_iri