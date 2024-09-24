import os
from langchain import SQLDatabase
from langchain_mistralai import ChatMistralAI
from langchain.prompts import PromptTemplate
from pydantic import Field, BaseModel
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import time
from langchain_together import TogetherEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv


def get_chain():
    load_dotenv()
    db = SQLDatabase.from_uri("sqlite:///database.db")
    model = ChatMistralAI(model='mistral-small-latest', temparture=0.4)
    emb_model = TogetherEmbeddings(model='togethercomputer/m2-bert-80M-8k-retrieval')
    examples_db = Chroma('sql_examples', embedding_function=emb_model, persist_directory='query_examples')
    retriever = examples_db.as_retriever(search_kwargs={'k': 2})

    class Tables(BaseModel):
        table_names_to_use: list[str] = Field(description='List of names of selected database tables')

    parser = JsonOutputParser(pydantic_object=Tables)

    with open(os.getenv('QUEST_PROMPT_PATH'), 'r') as f:
        template = f.read()

    question_prompt = PromptTemplate.from_template(template=template)

    with open(os.getenv('DOC_PROMPT_PATH'), 'r') as f:
        template = f.read()

    document_prompt = PromptTemplate.from_template(template=template)

    with open(os.getenv('SELECT_PROMPT_PATH'), 'r') as f:
        template = f.read()

    prompt = PromptTemplate.from_template(template=template,
                                          partial_variables={'table_info': db.get_context()['table_info'],
                                                             'format': parser.get_format_instructions()}
                                          )

    with open(os.getenv('SQL_PROMPT_PATH'), 'r') as f:
        template = f.read()

    sql_prompt = PromptTemplate.from_template(template,
                                              partial_variables={'top_k': 5})

    def format_documents(docs):
        formatted_docs = ""
        for doc in docs:
            formatted_doc = document_prompt.format(page_content=doc.page_content, sql=doc.metadata['sql'])
            formatted_docs += formatted_doc
        return formatted_docs

    question_chain = question_prompt | model | StrOutputParser()
    retriever_chain = question_chain | retriever | (lambda x: format_documents(x))

    select_chain = prompt | model | parser | (lambda x: x['table_names_to_use'])

    sql_chain = create_sql_query_chain(model, db, prompt=sql_prompt)

    chain = RunnablePassthrough.assign(table_names_to_use=select_chain) \
            | RunnablePassthrough(lambda _: time.sleep(1)) \
            | RunnablePassthrough.assign(context=retriever_chain) \
            | RunnablePassthrough(lambda _: time.sleep(1)) \
            | sql_chain

    return chain