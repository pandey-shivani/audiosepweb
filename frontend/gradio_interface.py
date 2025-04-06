import gradio as gr
import requests
import tempfile
import os

from settings import Settings

settings = Settings.load_from_yaml()

API_URL = settings.base_api_url


def gradio_process(audio, query):
    # Save the uploaded audio to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio.read())
        tmp_path = tmp.name

    # POST to the FastAPI endpoint
    files = {"audio_file": open(tmp_path, "rb")}
    data = {"query": query}
    resp = requests.post(f"{API_URL}/process-audio/", files=files, data=data)
    os.unlink(tmp_path)

    if resp.status_code != 200:
        return None, f"Error: {resp.text}"

    result = resp.json()
    # Now GET the processed file
    dl = requests.get(f"{API_URL}/download-processed/", params={"path": result["processed_file_path"]})
    if dl.status_code != 200:
        return None, f"Error downloading: {dl.text}"

    # Save locally so Gradio can play it
    out_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    out_tmp.write(dl.content)
    out_tmp.flush()
    return out_tmp.name, "Processed successfully!"


with gr.Blocks() as demo:
    gr.Markdown("## AudioSepWeb")
    with gr.Row():
        audio_in = gr.Audio(source="upload", type="filepath", label="Upload your audio")
        text_in = gr.Textbox(label="Text Query", placeholder="Describe how to process the audio…")
    with gr.Row():
        btn = gr.Button("Extract")
    with gr.Row():
        audio_out = gr.Audio(type="filepath", label="Processed Audio")
        status = gr.Textbox(label="Status")

    btn.click(
        fn=gradio_process,
        inputs=[audio_in, text_in],
        outputs=[audio_out, status],
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
