class Char:
    def __init__(self, symbol, code):
        self.symbol = symbol
        self.code = code

    def __eq__(self, other):
        return self.symbol == other.symbol


def sort_by_symbol(char: Char):
    return char.symbol


def get_chars_with_codes(text: str, encoding: str) -> list[Char]:
    chars: list[Char] = list()

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
