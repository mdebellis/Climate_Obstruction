from src.parse_authors import *
from src.ag_api import *

authors_string = "Chomsky, Noam; Turing, Allen"
fs_fitzgerald = create_author("Fitzgerald", "F.", "Scott")
print(fs_fitzgerald)
print(get_value(fs_fitzgerald,last_name_prop))
print(get_value(fs_fitzgerald,first_name_prop))
author_list = parse_authors(authors_string)
first_author = author_list[0]
print(get_value(first_author,last_name_prop))
print(get_value(first_author,first_name_prop))
second_author = author_list[1]
print(get_value(second_author,last_name_prop))
print(get_value(second_author,first_name_prop))
