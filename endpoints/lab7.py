from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

lab7Router = APIRouter()

upper_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т',
                 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']

lower_letters = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

upper_codes = {'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ё': 6, 'Ж': 7, 'З': 8, 'И': 9, 'Й': 10, 'К': 11,
               'Л': 12, 'М': 13, 'Н': 14, 'О': 15, 'П': 16, 'Р': 17, 'С': 18, 'Т': 19,
               'У': 20, 'Ф': 21, 'Х': 22, 'Ц': 23, 'Ч': 24, 'Ш': 25, 'Щ': 26, 'Ъ': 27, 'Ы': 28, 'Ь': 29, 'Э': 30,
               'Ю': 31, 'Я': 32}

lower_codes = {'а': 0, 'б': 1, 'в': 2, 'г': 3, 'д': 4, 'е': 5, 'ё': 6, 'ж': 7, 'з': 8, 'и': 9, 'й': 10, 'к': 11,
               'л': 12, 'м': 13, 'н': 14, 'о': 15, 'п': 16, 'р': 17, 'с': 18, 'т': 19,
               'у': 20, 'ф': 21, 'х': 22, 'ц': 23, 'ч': 24, 'ш': 25, 'щ': 26, 'ъ': 27, 'ы': 28, 'ь': 29, 'э': 30,
               'ю': 31, 'я': 32}

upper_table = []

lower_table = []


@lab7Router.get("/get-vigenere-encrypt")
def vigenere_encrypt(file_name: str, is_encoding: bool = True) -> JSONResponse:
    file = open(f"files/labs/{file_name}", "rb")
    text = file.read().decode("utf-8")
    result_text = ""

    key = "АНТВЛА"

    global upper_table
    global lower_table

    upper_table = get_table(upper_letters)
    lower_table = get_table(lower_letters)

    if is_encoding:
        result_text = encrypt(text, key)

        lab7File = open("files/results/lab7-result.txt", mode="w", encoding="utf-8")
        lab7File.write(result_text)
        lab7File.close()
    else:
        result_text = encrypt(text, key)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "text": str(text),
            "result": str(result_text)
        }
    )


def encrypt(text: str, key: str) -> str:
    global upper_table
    global lower_table

    global upper_codes
    global lower_codes

    result: str = ""

    key *= len(text) // len(key) + 1

    for index, char in enumerate(text):
        if char.isalpha():
            if char.isupper():
                col_index = upper_codes[char]

                row_index: int = 0

                for i in range(33):
                    if upper_table[i][col_index] == key[index]:
                        row_index = i
                        break

                result += upper_table[row_index][0]
            else:
                col_index = lower_codes[char]

                row_index: int = 0

                for i in range(33):
                    if upper_table[i][col_index] == key[index]:
                        row_index = i
                        break

                result += lower_table[row_index][0]
        else:
            result += char

    return result


def decrypt(text: str, key: str) -> str:
    global upper_table
    global lower_table
    global upper_codes
    global lower_codes

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


def get_table(letters: list[str]) -> [list[list[str]]]:
    offset = 0

    letters_len: int = len(letters)

    table: list[list[str]] = [["" for _ in range(letters_len)] for _ in range(letters_len)]

    for i in range(letters_len):
        for j in range(letters_len):
            index = j + offset

            if index >= letters_len:
                index -= letters_len

            table[i][j] = letters[index]

        offset += 1

    return table
