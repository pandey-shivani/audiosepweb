from pydantic import BaseModel, Field

class SeparateAudioRequest(BaseModel):
    text_query: str

class SeparateAudioResponse(BaseModel):
    file_path: str
