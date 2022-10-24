from fastapi import APIRouter, UploadFile
import heapq
from heapq import heappop, heappush

lab2Router: APIRouter = APIRouter()


@lab2Router.post("/upload-file")
async def upload_file(file: UploadFile):
    text = file.file.read().decode("utf-8")
    chars = getCharsWithCodes(text, "utf-8")

    res = buildHuffmanTree(text)

    totalMainSize = 0
    totalHuffmanSize = 0

    for c in chars:
        c.huffmanCode = res[0][c.symbol]
        c.huffmanSize = len(c.huffmanCode)
        c.commonSize = len(c.code) * 8

        totalMainSize += c.commonSize
        totalHuffmanSize += c.huffmanSize

    entropy1 = totalMainSize / len(chars)
    entropy2 = totalHuffmanSize / len(chars)

    compressionRatio = totalMainSize / totalHuffmanSize

    encodedText = res[1]

    lab2_file = open("files/results/lab2.txt", "w")

    lab2_file.write(encodedText)

    return {"chars": chars, "encodedText": encodedText, "entropy1": entropy1, "entropy2": entropy2,
            "compression": compressionRatio}


class Char:
    def __init__(self, symbol, code):
        self.symbol = symbol
        self.code = code
        self.count = 0
        self.huffmanCode = '',
        self.commonSize = 0
        self.huffmanSize = 0

    def __eq__(self, other):
        return self.symbol == other.symbol


def sortBySymbol(char: Char):
    return char.symbol


def sortByCount(char: Char):
    return char.count


def getCharsWithCodes(text: str, encoding: str) -> list:
    chars = list()
    charsCounter = dict()

    for c in text:
        if c in charsCounter:
            charsCounter[c] += 1
        else:
            charsCounter[c] = 1

        byt = c.encode(encoding=encoding)
        bytesList = list()

        for b in byt:
            bytesList.append(b)

        char = Char(c, bytesList)

        if char not in chars:
            chars.append(char)

    for c in chars:
        c.count = charsCounter[c.symbol]

    chars.sort(key=sortByCount)

    return chars


# Узел дерева
class Node:
    def __init__(self, ch, freq, left=None, right=None):
        self.ch = ch
        self.freq = freq
        self.left = left
        self.right = right

    # Переопределить функцию `__lt__()`, чтобы заставить класс `Node` работать с приоритетной очередью.
    # таким образом, что элемент с наивысшим приоритетом имеет наименьшую частоту
    def __lt__(self, other):
        return self.freq < other.freq


def isLeaf(root: Node):
    return root.left is None and root.right is None


# Пройти по дереву Хаффмана и сохранить коды Хаффмана в словаре
def encode(root, s, huffman_code):
    if root is None:
        return

    # обнаружил листовой узел
    if isLeaf(root):
        huffman_code[root.ch] = s if len(s) > 0 else '1'

    encode(root.left, s + '0', huffman_code)
    encode(root.right, s + '1', huffman_code)


# Пройти по дереву Хаффмана и декодировать закодированную строку
def decode(root, index, s):
    if root is None:
        return index

    # обнаружил листовой узел
    if isLeaf(root):
        print(root.ch, end='')
        return index

    index = index + 1
    root = root.left if s[index] == '0' else root.right

    return decode(root, index, s)


# строит дерево Хаффмана и декодирует заданный входной текст
def buildHuffmanTree(text: str):
    # Базовый случай: пустая строка
    if len(text) == 0:
        return

    # подсчитывает частоту появления каждого символа
    # и сохраните его в словаре
    freq = {i: text.count(i) for i in set(text)}

    # Создайте приоритетную очередь для хранения активных узлов дерева Хаффмана.
    pq = [Node(k, v) for k, v in freq.items()]
    heapq.heapify(pq)

    # делать до тех пор, пока в queue не окажется более одного узла
    while len(pq) != 1:
        # Удалить два узла с наивысшим приоритетом
        # (самая низкая частота) из queue

        left = heappop(pq)
        right = heappop(pq)

        # создает новый внутренний узел с этими двумя узлами в качестве дочерних и
        # с частотой, равной сумме частот двух узлов.
        # Добавьте новый узел в приоритетную очередь.

        total = left.freq + right.freq
        heappush(pq, Node(None, total, left, right))

    # `root` хранит указатель на корень дерева Хаффмана.
    root = pq[0]

    # проходит по дереву Хаффмана и сохраняет коды Хаффмана в словаре.
    huffmanCode = {}
    encode(root, '', huffmanCode)

    # распечатать закодированную строку
    s = ''
    for c in text:
        s += huffmanCode.get(c)

    if isLeaf(root):
        # Особый случай: для ввода типа a, aa, aaa и т. д.
        while root.freq > 0:
            print(root.ch, end='')
            root.freq = root.freq - 1
    else:
        # снова пересекают дерево Хаффмана, и на этот раз
        # декодирует закодированную строку
        index = -1
        while index < len(s) - 1:
            index = decode(root, index, s)

    return huffmanCode, s
