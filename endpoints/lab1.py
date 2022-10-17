import re

from fastapi import APIRouter, UploadFile, status
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

testRouter: APIRouter = APIRouter()

win1251 = [192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212,
           213, 214, 215, 216, 217, 220, 219, 218, 221, 222, 223]

doc866 = [128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148,
          149, 150, 151, 152, 153, 156, 155, 154, 157, 158, 159]

unicode = [255, 254, 16, 4, 17, 4, 18, 4, 19, 4, 20, 4, 21, 4, 22, 4, 23, 4, 24, 4, 25, 4, 26, 4, 27, 4, 28, 4, 29,
           4, 30, 4, 31, 4, 32, 4, 33, 4, 34, 4, 35, 4, 36, 4, 37, 4, 38, 4, 39, 4, 40, 4, 41, 4, 44, 4, 43, 4, 42,
           4, 45, 4, 46, 4, 47, 4]

myEncoding2 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
               107, 109, 113, 127, 131, 137]

myEncoding = {"А": 2, "Б": 3, "В": 5, "Г": 7, "Д": 11, "Е": 13, "Ё": 17, "Ж": 19, "З": 23, "И": 29, "Й": 31, "К": 37,
              "Л": 41, "М": 43, "Н": 47, "О": 53, "П": 59, "Р": 61, "С": 67, "Т": 71, "У": 73, "Ф": 79}


class Person(BaseModel):
    name: str
    age: int
    weight: float


@testRouter.get("/test-route", response_model=Person)
async def test_func():
    newPerson = Person(name="IVAN", age=20, weight=72.5)

    jsonObject = jsonable_encoder(newPerson)

    return jsonObject


@testRouter.post("/upload-file")
async def upload_file(file: UploadFile):
    encoding: str = getEncoding(file)

    text = file.file.read().decode(encoding)
    chars = getCharsWithCodes(text, encoding)

    formText = getFormatText(text)

    return {"encodingType": encoding, "chars": chars, "rawText": text, "formatText": formText}


def getEncoding(file: UploadFile) -> str:
    encodingType = ""

    for c in file.file.read():
        if c in win1251:
            encodingType = "cp1251"
            break
        elif c in doc866:
            encodingType = "cp866"
            break
        elif c in unicode:
            encodingType = "utf-16-be"
            break

    file.file.seek(0, 0)

    return encodingType


class Char:
    def __init__(self, symbol, code):
        self.symbol = symbol
        self.code = code

    def __eq__(self, other):
        return self.symbol == other.symbol


def sort_by_symbol(char: Char):
    return char.symbol


def getCharsWithCodes(text: str, encoding: str) -> list:
    chars = list()

    for c in text:
        byt = c.encode(encoding=encoding)

        bytesList = list()

        for b in byt:
            bytesList.append(b)

        char = Char(c, bytesList)

        if char not in chars:
            chars.append(char)

    chars.sort(key=sort_by_symbol)

    return chars


def getFormatText(text: str) -> str:
    res = re.sub(r'[^\w\s]', '', text)

    return res