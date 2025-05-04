import logging
from fastapi import FastAPI, UploadFile, File, Form
from rag import load_files, query_rag

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/upload")
async def upload_files(file: UploadFile = File(...)):
    logger.info(f"Received file upload request for: {file.filename}")
    content = await file.read()
    logger.info(f"File content read, size: {len(content)} bytes")
    result = load_files(file.filename, content)
    logger.info(f"File processing result: {result}")
    return {"status": "uploaded", "details": result}

@app.post("/ask")
async def ask_question(
    question: str = Form(...),
    file: UploadFile = File(None)
):
    logger.info(f"Received question: {question}")
    image_data = None
    if file is not None:
        image_data = await file.read()
        logger.info(f"Received image file: {file.filename}, size: {len(image_data)} bytes")
    answer = query_rag(question, image_data)
    logger.info("Question answered")
    return {"answer": answer}