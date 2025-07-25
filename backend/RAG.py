# WICHTIGER HINWEIS
# DIESE METHODE WURDE MIT CHATGPT ERSTELLT
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def dataframes_to_documents(source_dict):
    documents = []
    for name, df in source_dict.items():
        text = df.to_string(index=False)
        metadata = {"source": name}
        documents.append(Document(page_content=text, metadata=metadata))
    return documents

def build_vectorstore(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(documents, embeddings)

def retrieve_relevant_context(question, vectordb, k=4):
    return vectordb.similarity_search(question, k=k)