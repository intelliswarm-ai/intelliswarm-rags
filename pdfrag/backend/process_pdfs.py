import os
import logging
from rag import load_files

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_all_pdfs():
    # Look for data directory one level up
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    logger.info(f"Looking for PDFs in directory: {os.path.abspath(data_dir)}")
    
    if not os.path.exists(data_dir):
        logger.error(f"Data directory does not exist: {data_dir}")
        return
    
    pdf_files = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
    logger.info(f"Found {len(pdf_files)} PDF files: {pdf_files}")
    
    for filename in pdf_files:
        try:
            logger.info(f"Processing {filename}...")
            file_path = os.path.join(data_dir, filename)
            logger.info(f"Full path: {os.path.abspath(file_path)}")
            
            if not os.path.exists(file_path):
                logger.error(f"File does not exist: {file_path}")
                continue
                
            with open(file_path, 'rb') as f:
                content = f.read()
                logger.info(f"Read {len(content)} bytes from {filename}")
                result = load_files(filename, content)
                logger.info(f"Result: {result}")
        except Exception as e:
            logger.error(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    process_all_pdfs() 