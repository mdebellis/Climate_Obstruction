import streamlit as st
import pyperclip
from franz.openrdf.query.query import QueryLanguage
from ag_api import *



# Using pyperclip to copy the generated query to copy/paste stack. A hack until (someday!) will get Gruff link working
def do_query(user_question):
    if user_question == "":
        return ""
    else:
        query_string = build_query(str(user_question))
        pyperclip.copy(query_string)
        tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        result = tuple_query.evaluate()
        with result:
            for binding_set in result:
                response = binding_set.getValue("response")
                st.session_state.content = binding_set.getValue("content")
                return response

def build_query(user_question):
    if user_question == "":
        return ""
    else:
        query_string1 = "PREFIX franzOption_openaiApiKey: <franz:***********************************> "
        query_string1 = query_string1 + "PREFIX : <https://www.michaeldebellis.com/climate_obstruction/> "
        query_string1 = query_string1 + "PREFIX llm: <http://franz.com/ns/allegrograph/8.0.0/llm/> "
        query_string1 = query_string1 + "SELECT  * WHERE {bind(\"" + user_question
        query_string2 = "\" as ?query) "
        query_string2 = query_string2 + "(?response ?score ?citation ?content) llm:askMyDocuments (?query \"climate_obstruction\" 4 0.7).} "
        query_string = query_string1 + query_string2
        return query_string

st.set_page_config(layout="wide")
if "content" not in st.session_state:
    st.session_state.content = ""
# Safe session state initialization

st.title('Climate Obstruction Portal')
col1, col2 = st.columns(2)


with col1:
    question = st.text_area("Enter question here:", value="", height=None, max_chars=None,
             key=None, help=None, on_change=None, args=None,
             kwargs=None, placeholder="Type question here. Hit control-enter when done.", disabled=False,
             label_visibility="visible")
    sparqlQuery = st.text_area("Answer:", value=do_query(question), height=300, max_chars=None,
             key=None, help=None, on_change=None, args=None,
             kwargs=None, placeholder="Answer will be displayed here." + str(question), disabled=False,
             label_visibility="visible")
with col2:
    st.text_area("Supporting Documents:",height=445, placeholder="Supporting Documents will be displayed here.", value= "")    #  value= st.session_state.content)

st.page_link("http://localhost:10035", label="View answer graph in Gruff", icon=None, help=None, disabled=False, use_container_width=None)

#st.write("This is what the first text box entered " + str(dentistInput))
#st.write("This is what the second box wrote " + str(sparqlQuery))
#print(do_query("Does AB restorative in Class II cavities without adhesive system, result in an acceptable failure frequency after a one-year period?"))

# streamlit run C:\Users\mdebe\Documents\GitHub\Climate_Obstruction\src\ui_md.py