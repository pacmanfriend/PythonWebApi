from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

lab8Router = APIRouter()


@lab8Router.get("/get-rsa-encrypt")
def vigenere_encrypt(file_name: str, is_encoding: bool = True) -> JSONResponse:
    file = open(f"files/labs/{file_name}", "rb")
    text = file.read().decode("utf-8")
    result_text = ""

    p = 53
    q = 59

    n = p * q
    f = (p - 1) * (q - 1)
    e = 3
    d = 0

    i = 1
    while True:
        if (i * e) % f == 1:
            d = i
            break
        else:
            i += 1

    if is_encoding:
        result_text = encrypt(text, n, e)

        lab8File = open("files/results/lab8-result.txt", mode="w", encoding="utf-8")
        lab8File.write(result_text)
        lab8File.close()
    else:
        result_text = decrypt(text, n, d)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "text": str(text),
            "result": str(result_text)
        }
    )


def encrypt(text: str, n: int, e: int) -> str:
    result: list[str] = list()

    for char in text:
        c = ord(char) ** e % n

        result.append(str(c))

    return " ".join(result)


def decrypt(text: str, n: int, d: int) -> str:
    # Массив закодировнных символов
    chars: list[str] = text.split()

    result: list[str] = list()

    for char in chars:
        c = int(char) ** d % n

        result.append(chr(c))

    return "".join(result)
