import uuid
from src.ag_api import *
from nameparser import HumanName

last_name_prop = find_property(make_ontology_iri("last_name"))
first_name_prop = find_property(make_ontology_iri("first_name"))
middle_name_prop = find_property(make_ontology_iri("middle_name"))
person_class = find_class(make_gist_iri("Person"))
document_class = find_class(make_ontology_iri("Document"))
author_string_property = find_property(make_ontology_iri("author_string"))
author_property = find_property(make_ontology_iri("has_author"))

class Author:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
    def __eq__(self, other):
        return isinstance(other, Author) and self.first_name == other.first_name and self.last_name == other.last_name
    def __repr__(self):
        return f"Author('{self.first_name}', '{self.last_name}')"

def create_author(last_name, first_name=None, middle_name=None):
    #This assumes that last_name is always bound
    if last_name is None:
        print("Error New person must have a last name") # This should exit the function
        return None
    author_iri = make_instance(str(uuid.uuid4()), person_class)
    put_value(author_iri, last_name_prop, last_name)
    if middle_name is not None: put_value(author_iri, middle_name_prop, middle_name)
    if first_name is not None:
        put_value(author_iri, first_name_prop, first_name)
        put_value(author_iri, last_name_prop, last_name)
        put_value(author_iri, rdfs_label_property,  first_name + " " + last_name)
    else:
        put_value(author_iri, last_name_prop, last_name)
        put_value(author_iri, rdfs_label_property, last_name)
    return author_iri


def parse_authors(authors_string):
    print(authors_string) #Debugging
    authors = authors_string.split(";")   #split the authors by semi-colon
    author_list = []
    for author in authors:
        name = HumanName(author.strip())  #use name parser to parse the names
        first_name = name.first
        last_name = name.last
        #create an append author object
        author_obj = Author(first_name=first_name, last_name=last_name)
        author_list.append(author_obj)
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

#Loops through all the instances of Document
#if the Document has an author_string and has no values for the object property
#author_property then it creates a new object for each author (unless one already exists)
#and sets the author property to the appropriate (new or existing) OWL author object
def make_author_objects():
    documents = find_instances_of_class(document_class)
    for document in documents:
        document_authors = find_author_string(document)
        existing_authors = get_values(document, author_property)
        print(document_authors)
        if document_authors and not existing_authors:
            author_list = parse_authors(convert_to_string(document_authors))
            for author_pobject in author_list:
                find_or_create_author(author_pobject, document)

def get_author_label(author_pobject):
    first_name = author_pobject.first_name
    last_name = author_pobject.last_name
    if first_name is None:
        return last_name
    else:
        return first_name + " " + last_name

def find_or_create_author(author_pobject, document):
    author_label = get_author_label(author_pobject)
    author_object = find_object_from_label(author_label)
    if author_object:
        put_value(document, author_property, author_object)
    else:
        author_object = create_author(author_pobject.last_name, author_pobject.first_name, author_pobject.middle_name)
        put_value(document, author_property, author_object)



#make_author_objects()
#parse_authors("Justin Farrell")




