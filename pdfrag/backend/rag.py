import os
import logging
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
VECTOR_STORE_DIR = os.path.join(PROJECT_ROOT, "vectorstore")

# Initialize embedding model
logger.info("Initializing embedding model...")
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
logger.info("Embedding model initialized")

# Initialize or load FAISS index
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
if not os.path.exists(os.path.join(VECTOR_STORE_DIR, "index.faiss")):
    logger.info("Creating new FAISS index...")
    # Create an empty FAISS index if it doesn't exist
    empty_docs = [Document(page_content="")]
    faiss_index = FAISS.from_documents(empty_docs, embedding_model)
    faiss_index.save_local(VECTOR_STORE_DIR)
    logger.info("New FAISS index created and saved")
else:
    logger.info("Loading existing FAISS index...")
    faiss_index = FAISS.load_local(VECTOR_STORE_DIR, embedding_model, allow_dangerous_deserialization=True)
    logger.info("FAISS index loaded")

# Initialize LLM
logger.info("Initializing LLM...")
llm = OllamaLLM(model="mistral")  # or llava for multimodal
logger.info("LLM initialized")

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

def process_pdf(file_path):
    logger.info(f"Processing PDF file: {file_path}")
    # Read PDF file
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    logger.info(f"Extracted {len(text)} characters from PDF")
    return text

def load_files(filename, content):
    logger.info(f"Processing file: {filename}")
    # Save to disk
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(content)
    logger.info(f"File saved to: {file_path}")
    
    # Process the file based on its extension
    if filename.endswith('.txt'):
        logger.info("Processing text file...")
        # For text files, read and split into chunks
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    elif filename.endswith('.pdf'):
        logger.info("Processing PDF file...")
        # For PDF files, extract text and split into chunks
        text = process_pdf(file_path)
    else:
        logger.warning(f"Unsupported file format: {filename}")
        return f"File {filename} saved but not processed (unsupported format)"
    
    # Split text into chunks
    logger.info("Splitting text into chunks...")
    chunks = text_splitter.split_text(text)
    logger.info(f"Created {len(chunks)} chunks")
    
    # Create documents from chunks
    documents = [Document(page_content=chunk) for chunk in chunks]
    logger.info(f"Created {len(documents)} documents")
    
    # Add to vector store
    logger.info("Adding documents to vector store...")
    global faiss_index
    try:
        faiss_index.add_documents(documents)
        logger.info("Documents added to vector store")
        
        # Save the updated vector store
        logger.info("Saving vector store...")
        faiss_index.save_local(VECTOR_STORE_DIR)
        logger.info("Vector store saved successfully")
        
        return f"Processed {len(documents)} chunks from {filename}"
    except Exception as e:
        logger.error(f"Error adding documents to vector store: {str(e)}")
        return f"Error processing {filename}: {str(e)}"


def query_rag(question, image_data=None):
    logger.info(f"Processing question: {question}")
    retriever = faiss_index.as_retriever()
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa.run(question)
    logger.info("Question processed")
    return result
