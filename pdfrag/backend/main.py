import logging
from fastapi import FastAPI, UploadFile, File
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
async def ask_question(payload: dict):
    logger.info(f"Received question: {payload.get('question')}")
    question = payload.get("question")
    image_data = payload.get("image")  # base64 image or path
    answer = query_rag(question, image_data)
    logger.info("Question answered")
    return {"answer": answer}