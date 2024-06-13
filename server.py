import os
from tempfile import TemporaryDirectory
from typing import Optional

import aiofiles
from fastapi import FastAPI, UploadFile, Form
from pydantic import BaseModel

from transcriber import Transcriber

model_name = os.getenv("MODEL", "small")


class Audio(BaseModel):
    file: UploadFile
    start: Optional[float] = None
    end: Optional[float] = None


app = FastAPI()
transcriber = Transcriber(model_name)


@app.get("/status/")
async def status():
    import torch

    return {
        "status": "ok",
        "gpu": torch.cuda.is_available()
    }


@app.post("/transcribe/")
async def transcribe(
        file: UploadFile,
        start: Optional[float] = Form(None),
        end: Optional[float] = Form(None)
):
    with TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, file.filename)

        async with aiofiles.open(file_path, "wb") as fp:
            await fp.write(await file.read())

        transcript = transcriber.transcribe_file(file_path, start=start, end=end)

    return {"transcript": transcript}
