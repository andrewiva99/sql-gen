import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from chain import get_chain
from dotenv import set_key, load_dotenv
import os

def update_key():
    st.session_state.uploader_key += 1


def save_table(doc, name):
    engine = create_engine("sqlite:///database.db")
    df = pd.read_csv(doc)
    df.to_sql(name, con=engine)


def main():
    load_dotenv()
    st.set_page_config(
        page_title="SQLite Query Generator",
    )
    conn = st.connection(
        "database",
        type="sql",
        url="sqlite:///database.db"
    )
    st.header('SQLite Query Generator')

    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = 0

    with st.sidebar:
        with st.expander("Upload files"):
            doc = st.file_uploader(label='CSV uploader',
                                   type='csv',
                                   accept_multiple_files=False,
                                   key=f'uploader_{st.session_state.uploader_key}')
            name = st.text_input('Name')
            if st.button('Save') and doc is not None and name != '':
                save_table(doc, name)
                update_key()
                st.rerun()

        with st.expander("API Keys"):
            st.markdown("[Get your Mistral API KEY](https://console.mistral.ai/api-keys/)")
            new_key_mistral = st.text_input("Enter Mistral API KEY")
            if new_key_mistral is not None and st.button("Save Mistral API key"):
                set_key(".env", "MISTRAL_API_KEY", new_key_mistral)
                os.environ["MISTRAL_API_KEY"] = new_key_mistral

            st.markdown("[Get your Together API KEY](https://api.together.xyz/)")
            new_key_together = st.text_input("Enter Together API KEY")
            if new_key_together is not None and st.button("Save Together API key"):
                set_key(".env", "TOGETHER_API_KEY", new_key_together)
                os.environ["TOGETHER_API_KEY"] = new_key_together

    mistral_key_unavailable = os.environ['MISTRAL_API_KEY'] == ""
    together_key_unavailable = os.environ['TOGETHER_API_KEY'] == ""

    if mistral_key_unavailable:
        st.warning("Enter your Mistral API Key in the 'API Keys' section")
    if together_key_unavailable:
        st.warning("Enter your Together API Key in the 'API Keys' section")

    question = st.text_input('Question')

    chain = None
    if not mistral_key_unavailable and not together_key_unavailable:
        chain = get_chain()

    if st.button('Enter') and chain is not None:
        res = chain.invoke({'question': question})

        st.code(res, language='sql')

        df = conn.query(res)
        st.dataframe(df)


if __name__ == "__main__":
    main()
