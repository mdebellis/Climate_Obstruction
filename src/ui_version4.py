import streamlit as st

# Set page title and layout
st.set_page_config(page_title="Climate Obstruction", layout="wide")

# Main title and subheader
st.title("Climate Obstruction")
st.subheader("An Example Use Case")

# Create two columns: left for question and generated answer, right for supporting documents
col_left, col_right = st.columns([2, 1])

# Let the user type in a question
user_question = col_left.text_input("Enter your question:")

if user_question:
    # Placeholder for the generated answer
    generated_answer = f"This is a generated answer for your question: '{user_question}'"
    col_left.markdown("**Generated Answer:**")
    col_left.write(generated_answer)

    # Placeholder for generated supporting documents
    generated_docs = f"""
    **Supporting Documents for: {user_question}**

    - **Document 1:** Detailed analysis and methodology.
    - **Document 2:** Data, statistics, and relevant graphs.
    - **Document 3:** Additional insights and further reading.
    """
    col_right.markdown(generated_docs)
else:
    col_left.write("Please enter a question to generate an answer.")
    col_right.write("Supporting documents will appear here once a question is entered.")

