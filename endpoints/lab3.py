import math

from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from core import encodingUtils

lab3Route: APIRouter = APIRouter()


@lab3Route.get("/get-arithmetic-encoding")
async def arithmetic_encoding(file_name: str, is_encoding: bool = True) -> JSONResponse:
    file = open(f"files/labs/{file_name}", "rb")

    text: str = file.read().decode("utf-8")

    chars: [encodingUtils.Char] = encodingUtils.get_chars_with_codes(text, "utf-8")

    letters: list[Letter] = get_letters_frequency(text)
    letters.sort(key=sort_letters_by_probability, reverse=True)

    text_len = len(text)

    segments: dict[str, Segment] = define_segments(letters)

    res_codes: list[float] = list()
    codes_for_output: list[str] = list()

    block_size: int = 10
    current: int = 0

    while current < text_len:
        text_block = ""

        if current + block_size < text_len:
            text_block = text[current:current + block_size]
        else:
            text_block = text[current:]

        res_code: float = arithmetic_coding(segments, text_block)
        res_codes.append(res_code)
        codes_for_output.append(str(res_code))

        current += block_size

    res_codes_str = " ".join(codes_for_output)

    res_text = ""

    current = 0

    for code in res_codes:
        if current < text_len:
            current = block_size
        else:
            current = text_len - (text_len // block_size) * block_size

        res_block: str = arithmetic_decoding(segments, code, current)

        res_text += res_block

    res_text = res_text[:text_len]

    segments_list: list[Segment] = list(segments.values())

    for letter in letters:
        segments[letter.char].frequency = letter.frequency
        segments[letter.char].probability = letter.probability

    code_to_str = str(res_codes[0])[2:]

    bites = math.log2(len(code_to_str) / 8 * 10)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'result': str(res_codes_str),
            'text': str(text),
            'restext': str(res_text),
            'bites': str(bites),
            'chars': jsonable_encoder(chars),
            'segments': jsonable_encoder(segments_list)
        })


class Letter:
    def __init__(self, char: str):
        self.char: str = char
        self.frequency: int = 0
        self.probability: float = 0.0

    def __eq__(self, other):
        return self.char == other.char


def sort_letters_by_probability(letter: Letter):
    return letter.probability


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

    lettersLen = len(text)

    for letter in letters:
        letter.frequency = lettersCounter[letter.char]
        letter.probability = letter.frequency / lettersLen

    return letters


class Segment:
    def __init__(self, left: float, right: float, char: str):
        self.left: float = left
        self.right: float = right
        self.character: str = char
        self.char_code: float = 0.0
        self.interval: str = f"{self.left} - {self.right}"
        self.frequency: int = 0
        self.probability: float = 0.0

    def __eq__(self, other):
        return self.character == other.character


def define_segments(letters: list[Letter]) -> dict[str, Segment]:
    segments: dict[str, Segment] = dict()
    left: float = 0

    for letter in letters:
        segment = Segment(left=left, right=left + letter.probability, char=letter.char)
        segments[letter.char] = segment
        left = segment.right

    return segments


def arithmetic_coding(segments: dict[str, Segment], text: str) -> float:
    left: float = 0
    right: float = 1

    for c in text:
        newRight = left + (right - left) * segments[c].right
        newLeft = left + (right - left) * segments[c].left
        right = newRight
        left = newLeft

    res = (right + left) / 2

    return res


def arithmetic_decoding(segments: dict[str, Segment], code: float, text_size: int):
    res_text: str = ""

    for i in range(text_size):
        for s in segments:
            if segments[s].left <= code < segments[s].right:
                res_text += segments[s].character
                segments[s].char_code = code
                code = (code - segments[s].left) / (segments[s].right - segments[s].left)
                break

    return res_text


def get_encoded_text(text: str, segments: list[Segment]) -> str:
    encoded_chars: list[str] = list()

    for s in segments:
        encoded_chars.append(str(s.char_code))

    return " ".join(encoded_chars)
