from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader

from langchain.embeddings import HuggingFaceInstructEmbeddings

PERSIST_DIR = 'db'

documents = DirectoryLoader('./data/', glob="./*.txt", loader_cls=TextLoader).load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(documents)

embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")

vectordb = Chroma.from_documents(documents=texts, embedding=embeddings, persist_directory=PERSIST_DIR)
vectordb.persist()
