import os

from fastapi import APIRouter, UploadFile
import shutil

from pydantic import BaseModel

commonRouter: APIRouter = APIRouter()


@commonRouter.post('/upload-file')
async def upload_file(file: UploadFile):
    with open(f"files/{file.filename}.txt", "w") as textFile:
        shutil.copyfileobj(file.file, textFile)


class File(BaseModel):
    FileName: str


@commonRouter.get('/get-files')
async def get_files() -> list:
    filesFromDir = os.listdir('files/labs')

    files = list()

    for f in filesFromDir:
        file = File(FileName=f)

        files.append(file)

    a = 0

    return files
