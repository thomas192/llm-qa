import os

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings

QUESTION = 'How can skinny people develop type 2 diabetes?'

PERSIST_DIR = 'db'

embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
retriever = vectordb.as_retriever()

docs = retriever.get_relevant_documents(QUESTION)

docs_page_content = " ".join([d.page_content for d in docs])

template = """
    You are an assistant tasked to write reels and shorts scripts. You specialize into breaking down health and metabolic concepts by answering specific questions.
    There's a common thread that drives the content creator which is about slowing our aging speed.
    Each short video tries to answer a technical question related to how our body works.
    
    Today's question is: {question}
    
    You must answer the question based on the following information: {transcript}
    
    The script must be around 120 words. It's short so you can't answer the question using all the material provided.
    Focus on one or two key ideas to articulate.
    The script is delivered by a young doctor so the vibe is professinal but still entertaining. The goal is to inspire trust.
    Answer only using the factual information provided.
    Do not introduce yourself and do not speak directly to the viewer, start right away like if you were a guest on a podcast and someone started recording you while you were talking.
    Be direct to the point but don't make shortcuts when it comes to breaking down the ideas.
    Your answer only focuses on the actual text that will be delivered. Do not bother with stage direction.
    If you feel you don't have enough information to answer the question, say you don't know.
"""

filename = QUESTION[0:-1].replace(' ', '_')
os.makedirs('./prompts/', exist_ok=True)
with open(f'./prompts/{filename}.txt', 'w') as f:
    f.write(template.format(transcript=docs_page_content, question=QUESTION))