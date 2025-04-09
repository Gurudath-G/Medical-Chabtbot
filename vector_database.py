from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

pdf_directory='pdfsss/'
def upload_pdf():
    with open(pdf_directory+file.name,"wb") as f:
        f.write(file.getbuffer())

def load_pdf(file_path):
    loader=PDFPlumberLoader(file_path)
    documents=loader.load()
    return documents
file_path="pdfsss/B5084.pdf"
documents=load_pdf(file_path)
#print(len(documents))

#create chunks
def create_chunks(documents): 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 160,
        add_start_index = True
    )
    text_chunks = text_splitter.split_documents(documents)
    return text_chunks
text_chunks=create_chunks(documents)
#print(len(text_chunks))

ollama_model_name="deepseek-r1:1.5b"
def get_embedding_model(ollama_model_name):
    embeddings = OllamaEmbeddings(model=ollama_model_name)
    return embeddings

FAISS_DB_PATH="vectorstore/db_faissss"
faiss_db=FAISS.from_documents(text_chunks, get_embedding_model(ollama_model_name))
faiss_db.save_local(FAISS_DB_PATH)