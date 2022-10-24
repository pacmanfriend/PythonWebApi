import re
from typing import BinaryIO

from fastapi import APIRouter

lab1Router: APIRouter = APIRouter()

win1251 = [192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212,
           213, 214, 215, 216, 217, 220, 219, 218, 221, 222, 223]

doc866 = [128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148,
          149, 150, 151, 152, 153, 156, 155, 154, 157, 158, 159]

unicode = [255, 254, 16, 4, 17, 4, 18, 4, 19, 4, 20, 4, 21, 4, 22, 4, 23, 4, 24, 4, 25, 4, 26, 4, 27, 4, 28, 4, 29,
           4, 30, 4, 31, 4, 32, 4, 33, 4, 34, 4, 35, 4, 36, 4, 37, 4, 38, 4, 39, 4, 40, 4, 41, 4, 44, 4, 43, 4, 42,
           4, 45, 4, 46, 4, 47, 4]

myEncoding = {" ": 0, "А": 2, "Б": 3, "В": 5, "Г": 7, "Д": 11, "Е": 13, "Ё": 17, "Ж": 19, "З": 23, "И": 29, "Й": 31,
              "К": 37, "Л": 41, "М": 43, "Н": 47, "О": 53, "П": 59, "Р": 61, "С": 67, "Т": 71, "У": 73, "Ф": 79,
              "Х": 83, "Ц": 89, "Ч": 97, "Ш": 101, "Щ": 103, "Ъ": 107, "Ы": 109, "Ь": 113, "Э": 127, "Ю": 131, "Я": 137}


@lab1Router.get("/get-file-encoding")
async def get_file_encoding(file_name: str):
    file = open(f"files/labs/{file_name}", mode="br")

    encoding: str = get_encoding(file)
    text = file.read().decode(encoding)

    chars = get_chars_with_codes(text, encoding)
    formText = get_format_text(text)

    custom_encoding(formText)

    return {"encodingType": encoding, "chars": chars, "rawText": text, "formatText": formText}


def get_encoding(file: BinaryIO) -> str:
    encodingType = ""

    for c in file.read():
        if c in win1251:
            encodingType = "cp1251"
            break
        elif c in doc866:
            encodingType = "cp866"
            break
        elif c in unicode:
            encodingType = "utf-16-be"
            break

    file.seek(0, 0)

    return encodingType


class Char:
    def __init__(self, symbol, code):
        self.symbol = symbol
        self.code = code

    def __eq__(self, other):
        return self.symbol == other.symbol


def sort_by_symbol(char: Char):
    return char.symbol


def get_chars_with_codes(text: str, encoding: str) -> list:
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


def get_format_text(text: str) -> str:
    res = re.sub(r'[^\w\s]', '', text)

    return " ".join(res.split())


def custom_encoding(text: str):
    encodedChars = list()

    for c in text:
        encodedChars.append(str(myEncoding[c]))

    encodedStr = str.join(" ", encodedChars)

    lab1_file = open(file="files/results/lab1.txt", mode="w")
    lab1_file.write(encodedStr)
    lab1_file.close()
