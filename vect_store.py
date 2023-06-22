import os

from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader

from langchain.embeddings import HuggingFaceInstructEmbeddings

DATA_DIR = "data"
DB_DIR = "db"
os.makedirs(DB_DIR, exist_ok=True)

def create_vect_db(db_name):
    documents = DirectoryLoader(
        os.path.join(DATA_DIR, db_name), 
        glob="./*.txt", 
        loader_cls=TextLoader
        ).load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

    vectordb = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings, 
        persist_directory=os.path.join(DB_DIR, db_name)
        )
    
    vectordb.persist()
