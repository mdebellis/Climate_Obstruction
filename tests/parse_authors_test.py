from src.parse_authors import create_author, last_name_prop, first_name_prop
from src.ag_api import *

fs_fitzgerald = create_author("Fitzgerald", "F.", "Scott")
print(fs_fitzgerald)
print(get_value(fs_fitzgerald,last_name_prop))
print(get_value(fs_fitzgerald,first_name_prop))