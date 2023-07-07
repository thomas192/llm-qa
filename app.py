import streamlit as st
import os

from handler import handle_links
from vect_store import create_vect_db
from prompt import make_prompt

DB_DIR = "db"

def main():
    st.set_page_config(page_title="QA", page_icon="❓")
    
    with st.sidebar:
        st.header("Database management")
        
        st.subheader("Existing databases")
        try:
            existing_dbs = os.listdir(DB_DIR)
            if existing_dbs:
                dbs_string = '\n'.join([f"- {db}" for db in existing_dbs if not db.endswith(".parquet")])
                st.code(dbs_string)
            else:
                st.code("No existing databases.")
        except FileNotFoundError:
            st.code("No existing databases.")
        
        st.subheader("Create or use an existing database")
        db_name = st.text_input("Name:")
        links = st.text_area("URLs:")
        if st.button("Process"):
            if os.path.isdir(os.path.join(DB_DIR, db_name)):
                st.info(f"Database '{db_name}' is selected.")
            else:
                with st.spinner("Processing URLs..."):
                    pass
                    # handle_links(links, db_name)
                with st.spinner("Embedding..."):
                    create_vect_db(db_name)
                st.info(f"Database '{db_name}' was created.")
    
    st.header("Youtube QA")
    question = st.text_input("Ask a question:")
    if st.button("Send"):
        with st.spinner("Making prompt..."):
            prompt = make_prompt(question, db_name)
        st.code(prompt)

if __name__ == '__main__':
    main()
