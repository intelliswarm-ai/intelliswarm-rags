# Gradio Multimodal UI

This folder contains a Gradio-based multimodal chatbot UI, inspired by the official Gradio guide: https://www.gradio.app/guides/creating-a-chatbot-fast

## Purpose

- Provide a web-based interface for interacting with a multimodal (text + image) model, such as LLaVA via Ollama or Hugging Face.
- Support both text and image inputs, and display streamed responses from the model.

## Quickstart

1. Install dependencies:
   ```bash
   pip install gradio openai requests
   ```
2. Make sure your FastAPI backend is running at `http://localhost:8000/ask` and supports streaming responses.
3. Run the Gradio app:
   ```bash
   python app.py
   ```
4. Open the provided local URL in your browser to use the chatbot UI.

## Features
- Text and image input (drag-and-drop or upload)
- Streams responses from your backend as they arrive
- Easy to extend for more advanced multimodal or chat features

## Reference
- [Gradio: Creating a Chatbot Fast](https://www.gradio.app/guides/creating-a-chatbot-fast) 