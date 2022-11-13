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

    encrypted_blocks = replace_rows_in_blocks(replace_columns_in_blocks(blocks, m, n, column_key), m, n, row_key)

    encrypted_list: list[str] = list()

    for block in encrypted_blocks:
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

    decrypt_row_key: list[int] = [0 for _ in range(m)]
    decrypt_column_key: list[int] = [0 for _ in range(n)]

    for i in range(m):
        decrypt_row_key[row_key[i]] = i

    for i in range(n):
        decrypt_column_key[column_key[i]] = i

    blocks = get_blocks(text, m, n)

    encrypted_blocks = replace_columns_in_blocks(replace_rows_in_blocks(blocks, m, n, decrypt_row_key), m, n,
                                                 decrypt_column_key)

    decrypted_list: list[str] = list()

    for block in encrypted_blocks:
        for i in range(m):
            for j in range(n):
                decrypted_list.append(block[i][j])

    decrypted_text = "".join(decrypted_list)

    return decrypted_text


def replace_columns_in_blocks(blocks: list[list[list[str]]], m: int, n: int, col_key: list[int]) \
        -> list[list[list[str]]]:
    replaced_blocks: list[list[list[str]]] = list()

    for block in blocks:
        rep_block: list[list[str]] = [["" for _ in range(n)] for _ in range(m)]

        for i in range(m):
            for j in range(n):
                rep_block[i][col_key[j]] = block[i][j]

        replaced_blocks.append(rep_block)

    return replaced_blocks


def replace_rows_in_blocks(blocks: list[list[list[str]]], m: int, n: int, row_key: list[int]) -> list[list[list[str]]]:
    replaced_blocks: list[list[list[str]]] = list()

    for block in blocks:
        rep_block: list[list[str]] = [["" for _ in range(n)] for _ in range(m)]

        for j in range(n):
            for i in range(m):
                rep_block[row_key[i]][j] = block[i][j]

        replaced_blocks.append(rep_block)

    return replaced_blocks
