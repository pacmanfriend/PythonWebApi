import random

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

lab5Router = APIRouter()


@lab5Router.get("/get-block-encrypt")
async def block_encrypt(file_name: str, is_encoding: bool = True) -> JSONResponse:
    m = 9
    n = 3
    key = 8

    file = open(f"files/labs/{file_name}", "rb")
    text = file.read().decode("utf-8")
    result_text = ""

    if is_encoding:
        result_text = encrypt(text, m, n, key)
    else:
        result_text = decrypt(text, m, n, key)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "text": str(text),
            "result": str(result_text)
        }
    )


def get_key(m: int, n: int, key: int) -> tuple[list[int], list[int]]:
    row_key = list()
    column_key = list()

    random.seed(key)

    while len(row_key) < m:
        random_key = random.randrange(0, m)

        if random_key not in row_key:
            row_key.append(random_key)

    while len(column_key) < n:
        random_key = random.randrange(0, n)

        if random_key not in column_key:
            column_key.append(random_key)

    return row_key, column_key


def get_blocks(text: str, m: int, n: int) -> list[list[list[str]]]:
    chars_in_block_count: int = m * n
    blocks_count: int = 0

    if len(text) % chars_in_block_count == 0:
        blocks_count = len(text) // chars_in_block_count
    else:
        blocks_count = len(text) // chars_in_block_count + 1

    blocks = list()
    char_index = 0

    for b in range(blocks_count):
        block = list()

        for i in range(m):
            row = list()

            for j in range(n):
                char_index = m * n * b + i * n + j

                if char_index < len(text):
                    row.append(text[char_index])
                else:
                    row.append(random.choice(text))

            block.append(row)

        blocks.append(block)

    return blocks


def encrypt(text: str, m: int, n: int, key: int) -> str:
    keys = get_key(m, n, key)

    row_key = keys[0]
    column_key = keys[1]

    blocks = get_blocks(text, m, n)

    for block in blocks:
        for i in range(m):
            for j in range(n):
                block[i][j], block[i][column_key[j]] = block[i][column_key[j]], block[i][j]

    for block in blocks:
        for i in range(m):
            for j in range(n):
                block[i][j], block[row_key[i]][j] = block[row_key[i]][j], block[i][j]

    encrypted_list: list[str] = list()

    for block in blocks:
        for i in range(m):
            for j in range(n):
                encrypted_list.append(block[i][j])

    encrypted_text = "".join(encrypted_list)

    lab5File = open("files/results/lab5-result.txt", mode="w", encoding="utf-8")
    lab5File.write(encrypted_text)
    lab5File.close()

    return encrypted_text


def decrypt(text: str, m: int, n: int, key) -> str:
    keys = get_key(m, n, key)

    row_key = keys[0]
    column_key = keys[1]

    # row_key.reverse()
    # column_key.reverse()

    blocks = get_blocks(text, m, n)

    for block in blocks:
        for i in range(m):
            for j in range(n):
                block[row_key[i]][j], block[i][j] = block[i][j], block[row_key[i]][j]

    for block in blocks:
        for i in range(m):
            for j in range(n):
                block[i][column_key[j]], block[i][j] = block[i][j], block[i][column_key[j]]

    decrypted_list: list[str] = list()

    for block in blocks:
        for i in range(m):
            for j in range(n):
                decrypted_list.append(block[i][j])

    decrypted_text = "".join(decrypted_list)

    return decrypted_text
