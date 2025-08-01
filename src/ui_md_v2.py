import streamlit as st
import pyperclip
from franz.openrdf.query.query import QueryLanguage
from ag_api import *
from keys import oaik #Open AI Key stored in file ignored by GitHub
import re
st.set_page_config(layout="wide")

def clean_question(text):
    # Replace newlines and tabs with spaces, and strip extra whitespace
    return text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()


def do_query(user_question):
    if user_question == "":
        return ""
    else:
        user_question = clean_question(str(user_question))
        query_string = build_query(user_question)
        pyperclip.copy(query_string)
        tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
        result = tuple_query.evaluate()
        all_responses = []
        content_text = ""
        with result:
            for i, binding_set in enumerate(result, start=1):
                response = str(binding_set.getValue("response"))
                content = str(binding_set.getValue("content"))
                #Remove "(citation-id:<...>)" chunks from the response
                cleaned_response = re.sub(r"\(citation-id:<.*?>\)", "", response)
                all_responses.append(f"**Result {i}:**\n{cleaned_response.strip()}\n")
                content_text += f"\n---\nDocument {i}:\n{content.strip()}\n"
        st.session_state.content = content_text.strip()
        return "\n".join(all_responses)


def build_query(user_question):
    if user_question == "":
        return ""
    else:
        query_string1 = "PREFIX franzOption_openaiApiKey: " + oaik
        query_string1 = query_string1 + "PREFIX : <https://www.michaeldebellis.com/climate_obstruction/> "
        query_string1 = query_string1 + "PREFIX llm: <http://franz.com/ns/allegrograph/8.0.0/llm/> "
        query_string1 = query_string1 + "PREFIX vdbp: <http://franz.com/vdb/prop/> "
        query_string1 = query_string1 + "SELECT  * WHERE {bind(\"" + user_question
        query_string2 = "\" as ?query) "
        query_string2 += f"(?response ?score ?vec ?content) llm:askMyDocuments (?query \"climate_obstruction\" {num_results} {threshold}). "
        query_string2 = query_string2 + " ?doc ?prop ?content. FILTER(isIRI(?doc)) OPTIONAL { ?doc :has_Topic ?topic} OPTIONAL {?doc  :has_direct_part ?super_part} OPTIONAL {?doc  :has_author ?author}}"
        query_string = query_string1 + query_string2
        return query_string

if "content" not in st.session_state:
    st.session_state.content = ""
# Safe session state initialization

st.title('Climate Obstruction Portal')
col1, col2 = st.columns(2)


with col1:
    num_results = st.number_input(
        "Number of Results to Show",
        min_value=1,
        max_value=20,
        value=5,
        step=1
    )
    threshold = st.number_input(
        "Relevance Threshold",
        min_value = 0.0,
        max_value = 1.0,
        value = 0.5,
        step = 0.05
    )
    question = st.text_area("Enter question here:", value="", height=None, max_chars=None,
             key=None, help=None, on_change=None, args=None,
             kwargs=None, placeholder="Type question here. Hit control-enter when done.", disabled=False,
             label_visibility="visible")
    sparqlQuery = st.text_area("Answer:", value=do_query(question), height=300, max_chars=None,
             key=None, help=None, on_change=None, args=None,
             kwargs=None, placeholder="Answer will be displayed here." + str(question), disabled=False,
             label_visibility="visible")
with col2:
    st.text_area("Supporting Documents:",height=445, placeholder="Supporting Documents will be displayed here.", value = st.session_state.get("content", ""))

st.page_link("http://localhost:10035", label="View answer graph in Gruff", icon=None, help=None, disabled=False, use_container_width=None)
st.page_link("https://github.com/mdebellis/Climate_Obstruction/wiki/Climate-Obstruction-Help", label="Help", icon=None, help=None, disabled=False, use_container_width=None)

#st.write("This is what the first text box entered " + str(dentistInput))
#st.write("This is what the second box wrote " + str(sparqlQuery))

# streamlit run C:\Users\mdebe\Documents\GitHub\Climate_Obstruction\src\ui_md_v2.py
# streamlit run C:\Users\mdebe\Documents\GitHub\Climate_Obstruction\src\ui_md_test.py
# print(build_query("Who are major supporters of climate obstruction"))