from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
import shutil
import uvicorn
import os

from .schema import SeparateAudioRequest, SeparateAudioResponse


app = FastAPI(title="Separate audio using text query")

@app.post(
    "/process-audio/",
    response_model=SeparateAudioResponse,
    summary="Process an uploaded audio file with a text query",
)
async def process_audio(
    request: SeparateAudioRequest,
    audio_file: UploadFile = File(...)
):
    """
    Receives an audio file and a text query, does some processing
    (placeholder), and returns a path to the processed file.
    """

    text_query = request.text_query

    # 1) Save the incoming file to a temp location
    suffix = os.path.splitext(audio_file.filename)[1]
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_in:
        shutil.copyfileobj(audio_file.file, tmp_in)
        input_path = tmp_in.name

    # 2) "Process" the file (for demo, we just copy it; replace with your logic)
    with NamedTemporaryFile(delete=False, suffix=suffix) as tmp_out:
        output_path = tmp_out.name
    shutil.copy(input_path, output_path)

    # 3) Return the path
    return dict(file_path=output_path)


@app.get("/download-processed/")
async def download_processed(path: str):
    """
    Given a path returned by /process-audio/, returns the file for download/playback.
    """
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="audio/wav", filename=os.path.basename(path))



