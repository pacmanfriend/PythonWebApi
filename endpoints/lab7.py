from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

lab7Router = APIRouter()


@lab7Router.get("/get-vigenere-encrypt")
def vigenere_encrypt(file_name: str, is_encoding: bool = True) -> JSONResponse:
    file = open(f"files/labs/{file_name}", "rb")
    text = file.read().decode("utf-8")
    result_text = ""

    key = "КОД"

    if is_encoding:
        result_text = encrypt(text, key)

        lab7File = open("files/results/lab7-result.txt", mode="w", encoding="utf-8")
        lab7File.write(result_text)
        lab7File.close()
    else:
        result_text = decrypt(text, key)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "text": str(text),
            "result": str(result_text)
        }
    )


def encrypt(text: str, key: str) -> str:
    result: str = ""

    key *= len(text) // len(key) + 1

    A_code = ord('А')
    YA_code = ord('Я')

    a_code = ord('а')
    ya_code = ord('я')

    for index, char in enumerate(text):
        if char.isalpha():
            if char.isupper():
                result += chr(A_code + (ord(char) - A_code + ord(key[index])) % (YA_code - A_code + 1))
            else:
                result += chr(a_code + (ord(char) - a_code + ord(key[index])) % (ya_code - a_code + 1))
        else:
            result += char

    return result


def decrypt(text: str, key: str) -> str:
    result: str = ""

    key *= len(text) // len(key) + 1

    A_code = ord('А')
    YA_code = ord('Я')

    a_code = ord('а')
    ya_code = ord('я')

    for index, char in enumerate(text):
        if char.isalpha():
            if char.isupper():
                result += chr(A_code + (ord(char) - A_code - ord(key[index])) % (YA_code - A_code + 1))
            else:
                result += chr(a_code + (ord(char) - a_code - ord(key[index])) % (ya_code - a_code + 1))
        else:
            result += char

    return result
