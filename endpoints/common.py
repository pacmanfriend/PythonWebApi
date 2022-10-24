import os

from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import aiofiles

from pydantic import BaseModel

commonRouter: APIRouter = APIRouter()


@commonRouter.post('/upload-file')
async def upload_file(file: UploadFile):
    try:
        async with aiofiles.open(f"files/labs/{file.filename}", "wb") as out_file:
            content = file.file.read()
            await out_file.write(content)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'message': 'Произошла ошибка при сохранении файла',
                'error': str(e)
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'message': 'Файл успешно сохранен',
                'error': None
            }
        )


class File(BaseModel):
    FileName: str


@commonRouter.get('/get-files')
async def get_files() -> JSONResponse:
    try:
        filesFromDir = os.listdir('files/labs')

        files = list()

        for f in filesFromDir:
            file = File(FileName=f)

            files.append(file)

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'message': 'Произошла ошибка',
                'error': str(e)
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'files': jsonable_encoder(files),
                'message': 'Успешно',
                'error': None
            }
        )
