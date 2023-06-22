import os

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings

DB_DIR = "db"
PROMPT_DIR = "prompts"

TEMPLATE = """
    You are an assistant that answers specific questions about youtube videos based on the video's transcript:
    {transcript}
    
    The question is: {question}
    
    Only answer using the factual information provided.
    
    If you feel you don't have enough information to answer the question, say you don't know.
    
    Your answers are verbose and detailed.
"""

def make_prompt(question, db_name):
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    
    vectordb = Chroma(
        persist_directory=os.path.join(DB_DIR, db_name), 
        embedding_function=embeddings
        )
    retriever = vectordb.as_retriever()

    docs = retriever.get_relevant_documents(question)

    docs_page_content = " ".join([d.page_content for d in docs])

    filename = question[0:-1].replace(' ', '_')
    os.makedirs(os.path.join(PROMPT_DIR, db_name), exist_ok=True)
    with open(os.path.join(PROMPT_DIR, db_name, f'{filename}.txt'), 'w') as f:
        prompt = TEMPLATE.format(transcript=docs_page_content, question=question)
        f.write(prompt)

    return prompt
