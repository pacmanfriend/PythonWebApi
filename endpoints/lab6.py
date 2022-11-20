from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

lab6Router = APIRouter()


@lab6Router.get("/get-cesar-encrypt")
def cesar_encrypt(file_name: str, is_encoding: bool = True) -> JSONResponse:
    key = 4

    file = open(f"files/labs/{file_name}", "rb")
    text = file.read().decode("utf-8")
    result_text = ""

    if is_encoding:
        result_text = encrypt_func(text, key)

        lab6File = open("files/results/lab6-result.txt", mode="w", encoding="utf-8")
        lab6File.write(result_text)
        lab6File.close()
    else:
        result_text = decrypt_func(text, key)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "text": str(text),
            "result": str(result_text)
        }
    )

    pass


def encrypt_func(txt, key) -> str:
    result: str = ""

    A_code = ord('А')
    YA_code = ord('Я')

    a_code = ord('а')
    ya_code = ord('я')

    for i in range(len(txt)):
        char = txt[i]

        if char.isalpha():
            if char.isupper():
                result += chr(A_code + (ord(char) - A_code + key) % (YA_code - A_code + 1))
            else:
                result += chr(a_code + (ord(char) - a_code + key) % (ya_code - a_code + 1))
        else:
            result += char

    return result


def decrypt_func(txt, key) -> str:
    result: str = ""

    A_code = ord('А')
    YA_code = ord('Я')

    a_code = ord('а')
    ya_code = ord('я')

    for i in range(len(txt)):
        char = txt[i]

        if char.isalpha():
            if char.isupper():
                result += chr(A_code + (ord(char) - A_code - key) % (YA_code - A_code + 1))
            else:
                result += chr(a_code + (ord(char) - a_code - key) % (ya_code - a_code + 1))
        else:
            result += char

    return result
