from fastapi import FastAPI, UploadFile, HTTPException, Form, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
import shutil
import uvicorn
import os

from schema import SeparateAudioResponse
from dependencies import separation_model


import torch
from pathlib import Path

from services.decomposition.audiosep_core.pipeline import build_audiosep, seperate_audio
from settings import Settings

core_dir = Path(__file__).joinpath("services/decomposition/audiosep_core/")
api_settings = Settings.load_from_yaml()

if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

separation_model = build_audiosep(
        config_yaml=core_dir.parent.joinpath('config/audiosep_base.yaml'), 
        checkpoint_path=core_dir.joinpath('checkpoint/audiosep_base_4M_steps.ckpt'), 
        device=device
    )



app = FastAPI(title="Audio Separattion API")

@app.post(
    "/separate-audio/",
    response_model=SeparateAudioResponse,
    summary="Process an uploaded audio file with a text query",
)
async def process_audio(
    text_query: str = Form(...),
    audio_file: UploadFile = File(...)
):

    suffix = os.path.splitext(audio_file.filename)[1]
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
        shutil.copyfileobj(audio_file.file, tmp_in)
        input_path = tmp_in.name

    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_out:
        output_path = tmp_out.name

    separate_audio(separation_model, input_path, text_query, output_path)

    return dict(file_path=output_path)


@app.get("/download-processed/")
async def download_processed(path: str):
    """
    Given a path returned by /process-audio/, returns the file for download/playback.
    """
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="audio/wav", filename=os.path.basename(path))



