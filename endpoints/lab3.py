import math

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

lab3Route: APIRouter = APIRouter()


@lab3Route.get("/get-arithmetic-encoding")
async def arithmetic_encoding(file_name: str) -> JSONResponse:
    file = open(f"files/labs/{file_name}", "rb")

    text = file.read().decode("utf-8")

    letters = get_letters_frequency(text)

    res = arithmetic_coding(letters, text)

    bites = math.log2(res)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'result': str(res),
            'text': str(text),
            'bites': str(bites)
        })


class Letter:
    def __init__(self, char: str):
        self.char = char
        self.count: int = 0
        self.frequency: float = 0.0

    def __eq__(self, other):
        return self.char == other.char


def get_letters_frequency(text: str) -> list[Letter]:
    letters: list[Letter] = list()
    lettersCounter = dict()

    for c in text:
        if c in lettersCounter:
            lettersCounter[c] += 1
        else:
            lettersCounter[c] = 1

        letter = Letter(char=c)

        if letter not in letters:
            letters.append(letter)

    lettersLen = len(letters)

    for letter in letters:
        letter.count = lettersCounter[letter.char]
        letter.frequency = letter.count / lettersLen

    return letters


class Segment:
    def __init__(self, left: float, right: float, char: str):
        self.left: float = left
        self.right: float = right
        self.character = char


def define_segments(letters: list[Letter]) -> dict[str, Segment]:
    segments: dict[str, Segment] = dict()
    left: float = 0

    for letter in letters:
        segment = Segment(left=left, right=left + letter.frequency, char=letter.char)
        segments[letter.char] = segment
        left = segment.right

    return segments


def arithmetic_coding(letters: list[Letter], text: str) -> float:
    segments: dict[str, Segment] = define_segments(letters)
    left: float = 0
    right: float = 1

    for c in text:
        newRight = left + (right - left) * segments[c].right
        newLeft = left + (right - left) * segments[c].left
        left = newLeft
        right = newRight

    res: float = (left + right) / 2

    return res
