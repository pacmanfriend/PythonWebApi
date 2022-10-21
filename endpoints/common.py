from fastapi import APIRouter, UploadFile
import shutil

commonRouter: APIRouter = APIRouter()


@commonRouter.post('/upload-file')
async def upload_file(file: UploadFile):
    with open(f"files/{file.filename}.txt", "w") as textFile:
        shutil.copyfileobj(file.file, textFile)
