from franz.openrdf.connect import ag_connect
from franz.openrdf.vocabulary import RDF
import os

# Utilities to make and query AllegroGraph objects
# Note that functions to retrieve values need to be sent a complete IRI
# because we may be retrieving values from SKOS, Gist, or other properties
# However functions to create objects and set values assume all new objects go in
# the main ontology so only need to pass them the last part of the IRI and they complete the
# iri in the function using make_ontology_iri
conn = ag_connect('climate_obstruction', host='localhost', port=10035, user='mdebellis', password='df1559')

owl_named_individual = conn.createURI("http://www.w3.org/2002/07/owl#NamedIndividual")
owl_datatype_property = conn.createURI("http://www.w3.org/2002/07/owl#DatatypeProperty")
owl_annotation_property = conn.createURI("http://www.w3.org/2002/07/owl#AnnotationProperty")
owl_object_property = conn.createURI("http://www.w3.org/2002/07/owl#ObjectProperty")
owl_class = conn.createURI("http://www.w3.org/2002/07/owl#Class")
rdfs_label_property = conn.createURI("http://www.w3.org/2000/01/rdf-schema#label")
rdfs_is_defined_by_property = conn.createURI("http://www.w3.org/2000/01/rdf-schema#isDefinedBy")
skos_pref_label_property = conn.createURI("http://www.w3.org/2004/02/skos/core#prefLabel")
ontology_string = "https://www.michaeldebellis.com/climate_obstruction/"
gist_string = "https://w3id.org/semanticarts/ns/ontology/gist/"

# Function to check in case any http rather than https sneak into ontologies
def find_http_iris(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            if 'http://www.michaeldebellis.com/climate_obstruction/' in line:
                print(f"[Line {i}]: {line.strip()}")

# Given the last part of an IRI will return the full IRI string
# E.g., given "Green_Washing" returns "https://www.michaeldebellis.com/climate_obstruction/Green_Washing"
def make_ontology_iri (iri_name):
    return ontology_string + iri_name

# Same as make_ontology_iri but for Gist IRI
def make_gist_iri (gist_name):
    return gist_string + gist_name

# Finds a class with the the IRI class_name
# If no such class exists, returns None
# Note: when we refer to "IRI name" we mean last part of the IRI after the ontology prefix
# E.g., IRI name of "http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/Person" is "Person"
def find_class (iri_str):
    class_object = conn.createURI(iri_str)
    for _ in conn.getStatements(class_object, RDF.TYPE, owl_class):
        return class_object
    print(f'Error {iri_str} is not a class')
    return None

# Returns a set with all the instances of the class where the class is specified by name
# Note wherever it says X_name it means the IRI name of X If no class with that IRI name returns None
# If the class has no instances returns an empty list.
def find_instances_of_class(class_object):
    class_set = set()
    statements = conn.getStatements(None, RDF.TYPE, class_object)
    with statements:
        for statement in statements:
            class_set.add(statement.getSubject())
    return class_set


# Finds a property (annotation, object, or datatype) from the IRI name
# Need some special tests up front for things like rdfs:label that aren't
# OWL properties
def find_property(prop_str):
    if prop_str == "label":
        return rdfs_label_property
    prop = conn.createURI(prop_str)
    if prop == rdfs_label_property:
        return prop
    if prop == skos_pref_label_property:
        return prop
    if prop == rdfs_is_defined_by_property:
        return prop
    for _ in conn.getStatements(prop, RDF.TYPE, owl_datatype_property):
        return prop
    for _ in conn.getStatements(prop, RDF.TYPE, owl_annotation_property):
        return prop
    for _ in conn.getStatements(prop, RDF.TYPE, owl_object_property):
        return prop
    print(f'Error {prop} is not a property')
    return None

# Finds an instance from the IRI name
def find_instance(iri_name):
    instance_iri = conn.createURI(iri_name)
    statements = conn.getStatements(instance_iri, RDF.TYPE, owl_named_individual)
    with statements:
        for statement in statements:
            if len(statements) > 1:
                print(f'Warning two or more Individuals with ID: {instance_iri} using first one')
                return statement.subject()
            elif len(statements) == 1:
                return statement.getSubject()
    return None

# Finds an object based on its rdfs:label. Note this will also work for prefLabel and altLabel
# as long as the reasoner has run because they are sub-properties of rdfs:label
# If no object with that label, returns None
def find_object_from_label(label_string):
    statements = conn.getStatements(None, rdfs_label_property, label_string)
    with statements:
        for statement in statements:
            kg_object = statement.getSubject()
            return kg_object
    statements = conn.getStatements(None, skos_pref_label_property, label_string)
    with statements:
        for statement in statements:
            kg_object = statement.getSubject()
            return kg_object
    return None


# Gets the value of a single valued property using the IRI name of the instance and the IRI name of the property
# If the property has multiple values prints a warning and returns the first one
# If the property has no value returns None Note: if not sure whether property has multiple values, best to use get_values
def get_value(instance, owl_property):
    statements = conn.getStatements(instance, owl_property, None)
    with statements:
        for statement in statements:
            if len(statements) > 1:
                print(f'Warning: two or more values for property: {owl_property}. Using first one.')
                return statement.getObject()
            elif len(statements) == 1:
                return statement.getObject()
    print(f'Warning: No property value for: {instance, owl_property}.')
    return None

# Returns the values of a the property of an instance in a set if no values returns an empty set
def get_values(instance, owl_property):
    values = set()
    statements = conn.getStatements(instance, owl_property, None)
    with statements:
        for statement in statements:
            next_value = statement.getObject()
            values.add(next_value)
    return values

# Creates a new instance of a class and returns the new instance
def make_instance (instance_name, instance_class):
    instance_iri = conn.createURI(make_ontology_iri(instance_name))
    conn.add(instance_iri, RDF.TYPE, owl_named_individual)
    conn.add(instance_iri, RDF.TYPE, instance_class)
    return instance_iri

# Get the label from an object. Looks in skos:prefLabel first (which currently is usually empty)
# Then uses first value it finds in rdfs:label. If no label string returns empty string
def object_to_string(kg_object):
    pref_statements = conn.getStatements(kg_object, skos_pref_label_property, None)
    with pref_statements:
        for statement in pref_statements:
            return statement.getObject()
    l_statements = conn.getStatements(kg_object, rdfs_label_property, None)
    with l_statements:
        for statement in l_statements:
            return statement.getObject()
    print("Error: object has no label string: {kg_object}")
    return ""

# When getting values that are datatypes there is all sorts of extra stuff we usually want to strip out
# E.g., in the dest data below the result of get_value("MichaelDeBellis", "email") will be: "mdebellissf@gmail.com"^^<http://www.w3.org/2001/XMLSchema#anyURI>
# this should strip out the datatype and extra string characters so will return mdebelissf@gmail.com
def convert_to_string (literal):
        literal = str(literal)
        literal = literal.replace(literal[literal.find("^") + len("^"):], '') #remove the datatype
        literal = literal[1:len(literal) - 2] # remove the string characters and the remaining ^
        return literal

# Adds a new value to an instance of a property.
# Note this takes as input the actual instance and property (i.e., their IRIs) so if needed use find_instance and find_property
# Did this for efficiency, there will be times then we already have a handle on the object and property
def put_value(instance, kg_property, new_value):
    conn.add(instance, kg_property, new_value)

# Deletes a value for an instance of a property.
# Note this takes as input the actual instance and property (i.e., their IRIs) so if needed use find_instance and find_property
# Did this for efficiency, there will be times then we already have a handle on the object and property
def delete_value(instance, kg_property, old_value):
    conn.removeTriples(instance, kg_property, old_value)

"""
#Test data, in each case the comment below is what should be returned (with the current ontology)
print(find_instance_from_iri("SanFrancisco"))
# <http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/SanFrancisco>
print(get_values(find_instance_from_iri("USA"), find_property("contains")))
# [<http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/SanFrancisco>, <http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/CA>,... ]
print(get_value(find_instance_from_iri("MichaelDeBellis"), find_property("email")))
# "mdebellissf@gmail.com"^^<http://www.w3.org/2001/XMLSchema#anyURI>
print(convert_to_string(get_value(find_instance_from_iri("MichaelDeBellis"), find_property("email"))))
# mdebellissf@gmail.com
print(find_class("Agent"))
# <http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/Agent>
print(find_class("Foo"))
# Error Foo is not a class
# None
print(find_instances_of_class("Person"))
# [<http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/DanielDuffy>, <http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/RyanMcGranaghan>,...]
print(object_to_string(find_class("Organization")))
# "Organization"
put_value(find_instance_from_iri("USA"), find_property("contains"), make_instance("Alaska", "State"))
conn.deleteDuplicates("spo")   # So we can run the test data without creating lots of Alaskas
print(get_values(find_instance_from_iri("USA"), find_property("contains")))
# List should include Alaska
delete_value(find_instance_from_iri("USA"), find_property("contains"),find_instance_from_iri("Alaska"))
print(get_values(find_instance_from_iri("USA"),find_property("contains")))
# List should not include Alaska
print(find_object_from_label("Adam Kellerman"))
# <http://www.semanticweb.org/ontologies/2022/1/CfHA_Ontology/AdamKellerman>
# find_http_iris("path/to/your_ontology.owl")
"""

