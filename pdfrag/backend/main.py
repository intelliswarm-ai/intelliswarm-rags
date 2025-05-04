import logging
from fastapi import FastAPI, UploadFile, File, Form
from rag import load_files, query_rag
from fastapi.responses import StreamingResponse
import httpx
import base64
import json

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
    image_b64 = None
    if file is not None:
        image_data = await file.read()
        image_b64 = base64.b64encode(image_data).decode("utf-8")
        logger.info(f"Received image file: {file.filename}, size: {len(image_data)} bytes")

    ollama_url = "http://127.0.0.1:11434/api/generate"
    data = {
        "model": "llava",
        "prompt": question,
    }
    if image_b64:
        data["images"] = [image_b64]

    async def stream_ollama():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", ollama_url, json=data) as response:
                async for line in response.aiter_lines():
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            if "response" in chunk:
                                yield chunk["response"] + "\n"
                        except Exception:
                            pass

    return StreamingResponse(stream_ollama(), media_type="text/plain")