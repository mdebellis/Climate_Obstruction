import sys
import os
import uuid
# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from src.ag_api import *

asa_ruling = find_instance(make_ontology_iri("ASA_Ruling_on_Repsol_SA"))
print(asa_ruling)
gist_text_prop = find_property(make_gist_iri("containedText"))
print(gist_text_prop)
asa_text = get_values(asa_ruling,gist_text_prop)
print(asa_text)
sd_class = find_class(make_ontology_iri("Selective_Disclosure"))
print(sd_class)
sd_instances = find_instances_of_class(sd_class)
print(sd_instances)
new_instance_name = str(uuid.uuid4())
new_instance = make_instance(new_instance_name, sd_class)
print(new_instance)
print(object_to_string(asa_ruling))
brulle = find_instance(make_ontology_iri("ROBERT_J_BRULLE"))
print(brulle)
last_name_prop = find_property(make_ontology_iri("last_name"))
print(get_value(brulle, last_name_prop))
put_value(asa_ruling, gist_text_prop, "Foo")
asa_text = get_values(asa_ruling,gist_text_prop)
print(asa_text)
co_book = find_instance(make_ontology_iri("Climate_Obstruction_in_Europe"))
print(co_book)
put_value(co_book, rdfs_label_property, "Climate Obstruction in Europe")
co_book2 = find_object_from_label("Climate Obstruction in Europe")
print(co_book2)
print(object_to_string(co_book2))
delete_value(asa_ruling, gist_text_prop, "Foo")
asa_text = get_values(asa_ruling,gist_text_prop)
print(asa_text)
person_class = find_class(make_gist_iri("Person"))
print(person_class)
print(find_property(make_ontology_iri("last_name")))
print(find_property(make_ontology_iri("first_name")))
print(find_property(make_ontology_iri("middle_name")))



