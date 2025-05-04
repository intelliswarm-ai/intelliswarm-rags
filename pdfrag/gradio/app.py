import gradio as gr
import requests

BACKEND_URL = "http://localhost:8000/ask"

def multimodal_chat(message, history, image=None):
    # Prepare the multipart form data
    files = {}
    data = {"question": message}
    if image is not None:
        files["file"] = open(image, "rb")
    try:
        with requests.post(BACKEND_URL, data=data, files=files, stream=True, timeout=180) as resp:
            resp.raise_for_status()
            answer = ""
            # Stream the response line by line
            for chunk in resp.iter_lines(decode_unicode=True):
                if chunk:
                    answer += chunk
                    yield answer
    except Exception as e:
        yield f"Error: {e}"
    finally:
        if files:
            files["file"].close()

with gr.Blocks() as demo:
    chatbot = gr.ChatInterface(
        fn=multimodal_chat,
        additional_inputs=[gr.Image(type="filepath", label="Upload or paste an image (optional)")],
        title="Multimodal Chatbot (Text + Image)",
        description="Ask questions with text and/or images. Powered by Gradio."
    )

demo.launch() 