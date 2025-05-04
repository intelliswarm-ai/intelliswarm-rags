# PDF RAG System

This project implements a RAG (Retrieval-Augmented Generation) system for processing and querying PDF documents.

## Prerequisites

- Python 3.8 or higher
- Java 11 or higher (for the frontend)
- Maven (for the frontend)
- Ollama (for the LLM)

## Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Install Ollama and pull the Mistral model:
```bash
ollama pull mistral
```

## Usage

### Processing PDFs

1. Place your PDF files in the `data` directory
2. Process the PDFs to create the vector store:
```bash
cd backend
python process_pdfs.py
```

### Running the System

1. Start the FastAPI backend:
```bash
cd backend
uvicorn main:app --reload
```

2. In a separate terminal, start the JavaFX frontend:
```bash
cd frontend
mvn clean javafx:run
```

### Using the System

1. The frontend will open a window with:
   - A text field for entering questions
   - A button to submit questions
   - A text area to display answers

2. Enter your question and click "Ask" to get answers based on the content of your PDFs.

## Project Structure

- `backend/`: FastAPI server and RAG implementation
- `frontend/`: JavaFX user interface
- `data/`: Directory for PDF files
- `vectorstore/`: Directory for the FAISS vector store

## Troubleshooting

- If you encounter any issues with PDF processing, check the logs in the terminal
- Make sure Ollama is running and the Mistral model is available
- Ensure all dependencies are properly installed 