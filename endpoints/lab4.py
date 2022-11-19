from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import random
import pickle

lab4Route: APIRouter = APIRouter()


@lab4Route.get('/get-gamma-encryption')
async def get_gamma_encryption(file_name: str, is_encoding: bool = True) -> JSONResponse:
    file = open(f"files/labs/{file_name}", "rb")

    text = ""
    n = 3

    key = 10 * n + n

    if is_encoding:
        text = file.read()
        text = text.decode("utf-8")
        gamma_encrypt(text, key)
    else:
        text = pickle.load(file)
        decoded_text = gamma_decrypt(text, key)
        text = decoded_text

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'text': str(text)
        })


def gamma_encrypt(text, key: int):
    text_bites = text.encode(encoding="utf-8")

    random.seed(key)

    rand_list: list[int] = list()

    for i in text_bites:
        a = random.randrange(0, 256, key)

        res = i ^ a

        rand_list.append(res)

    encoded_text = bytes(rand_list)

    lab4_file = open("files/results/lab4-res.txt", "wb")
    pickle.dump(encoded_text, lab4_file)
    lab4_file.close()


def gamma_decrypt(text, key: int) -> str:
    random.seed(key)

    # res_list: list[bytes] = list()

    res_bytes: bytearray = bytearray()

    for i in text:
        a = random.randrange(0, 256, key)

        res = i ^ a

        res_bytes.append(res)

    return res_bytes.decode()
