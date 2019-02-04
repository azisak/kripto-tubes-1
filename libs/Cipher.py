from string import ascii_lowercase
from random import shuffle
import numpy as np


class VigenereStandard:
    def __init__(self, key="vigenere"):
        self.key = key.lower()

    def changeKey(self, newKey):
        """
        Set a new key (auto-lowered case) to the cipher class
        """
        self.key = newKey.lower()

    def encrypt(self, text):
        """
        Encrypt text data to text data, limitation: only encrypt alphabets
        """
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        cipherText = map(lambda p: chr(
            (p[0] + p[1]) % 26 + ord('a')), zip(text, key))
        cipherText = ''.join(list(cipherText))
        return cipherText.upper()

    def decrypt(self, text):
        """
        Decrypt text data to text data, limitation: only decrypt alphabets
        """
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        plainText = map(lambda p: chr(
            (p[0] - p[1]) % 26 + ord('a')), zip(text, key))
        plainText = ''.join(list(plainText))
        return plainText.lower()

    def __normalizeTextKey(self, text, key):
        if (text.__len__() == key.__len__()):
            return text, key
        elif (text.__len__() > key.__len__()):
            key = (key * (text.__len__()//key.__len__())) + \
                key[0:text.__len__() % key.__len__()]
            return text, key
        else:  # text.length < key.length
            key = key[0:text.__len__()]
            return text, key


class VigenereFull(VigenereStandard):
    def __init__(self, key="vigenere", matrixName=None):
        self.key = key
        if (matrixName == None):
            self.matrix = self.createMatrix()
        else:
            self.matrix = np.load("./matrix/"+matrixName+".npy")

    def changeKey(self, newKey):
        self.key = newKey.lower()

    def encrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        cipherText = map(lambda p: chr(
            (self.matrix[p[1]][p[0]]) % 26 + ord('a')), zip(text, key))
        cipherText = ''.join(list(cipherText))
        return cipherText.upper()

    def decrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        plainText = map(lambda p: chr(
            (np.where(self.matrix[p[1]] == p[0])[0].item()) % 26 + ord('a')), zip(text, key))
        plainText = ''.join(list(plainText))
        return plainText.lower()

    def __normalizeTextKey(self, text, key):
        if (text.__len__() == key.__len__()):
            return text, key
        elif (text.__len__() > key.__len__()):
            key = (key * (text.__len__()//key.__len__())) + \
                key[0:text.__len__() % key.__len__()]
            return text, key
        else:  # text.length < key.length
            key = key[0:text.__len__()]
            return text, key

    def createMatrix(self):
        mat = np.arange(26)
        shuffle(mat)
        mat = np.array([np.roll(mat, i) for i in range(26)])
        return mat

    def saveMatrix(self, matrixName):
        if (self.matrix.any()):
            np.save("./matrix/"+matrixName, self.matrix)
        else:
            print("Error, matrix empty")


class VigenereExtended(VigenereStandard):
    ENCODING = "utf-8"

    def encrypt(self, data):
        """
        Encrypt bytes data to bytes data
        """
        if (type(data) == str):  # Safe checking if the type is string
            data = data.encode(self.ENCODING)
        data, key = self.__normalizeTextKey(data, self.key)
        data = list(data)
        key = list(key.encode(self.ENCODING))
        cipherText = map(lambda p: (p[0] + p[1]) % 256, zip(data, key))
        cipherText = bytes(list(cipherText))
        return cipherText

    def decrypt(self, data):
        """
        Decrypt bytes data to bytes data
        """
        if (type(data) == str):  # Safe checking if the type is string
            data = data.encode(self.ENCODING)
        data, key = self.__normalizeTextKey(data, self.key)
        data = list(data)
        key = list(key.encode(self.ENCODING))
        plainText = map(lambda p:
                        (p[0] - p[1]) % 256, zip(data, key))
        plainText = bytes(list(plainText))
        return plainText

    def __normalizeTextKey(self, text, key):
        if (len(text) == len(key)):
            return text, key
        elif (len(text) > len(key)):
            key = (key * (len(text)//len(key))) + key[0:len(text) % len(key)]
            return text, key
        else:  # text.length < key.length
            key = key[0:len(text)]
            return text, key


class VigenereAutoKey(VigenereStandard):
    def encrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        cipherText = map(lambda p: chr(
            (p[0] + p[1]) % 26 + ord('a')), zip(text, key))
        cipherText = ''.join(list(cipherText))
        return cipherText.upper()

    def decrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        text, key = self.__normalizeTextKey(text, self.key)
        text = list(map(lambda p: ord(p) % ord('a'), list(text)))
        key = list(map(lambda p: ord(p) % ord('a'), list(key)))
        plainText = map(lambda p: chr(
            (p[0] - p[1]) % 26 + ord('a')), zip(text, key))
        plainText = ''.join(list(plainText))
        return plainText.lower()

    def __normalizeTextKey(self, text, key):
        if (text.__len__() == key.__len__()):
            return text, key
        elif (text.__len__() > key.__len__()):
            key = key + text[0:text.__len__()-key.__len__()]
            return text, key
        else:  # text.length < key.length
            key = key[0:text.__len__()]
            return text, key


class VigenereRunningKey(VigenereStandard):
    def __init__(self, key="kemanusiaanyangadildanberadab"):
        self.key = key.lower()


class Playfair:
    def __init__(self, key="JALAN GANESHA SEPULUH", escape_char='j', replace_char='i', padding_char='x'):
        self.escape_char = escape_char
        self.replace_char = replace_char
        self.padding_char = padding_char
        self.key = self.__createMatrixKey(
            "".join([c for c in key.lower() if c.isalpha()]))

    def changeKey(self, newKey):
        self.key = self.__createMatrixKey(newKey.lower())

    def encrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        text = text.replace(self.escape_char, self.replace_char)
        bi_gram = self.__createBigram(text)
        newChars = []
        for leftChar, rightChar in bi_gram:
            posLeft = np.where(self.key == leftChar)
            posRight = np.where(self.key == rightChar)
            newChar = ""
            if (posLeft[0].item() == posRight[0].item()):  # Same row
                newChar = self.key[posLeft[0].item(), (posLeft[1].item(
                )+1) % 5] + self.key[posRight[0].item(), (posRight[1].item()+1) % 5]
            elif (posLeft[1].item() == posRight[1].item()):  # Same Column
                newChar = self.key[(posLeft[0].item()+1) % 5, posLeft[1].item()] + \
                    self.key[(posRight[0].item()+1) % 5, posRight[1].item()]
            else:
                newChar = self.key[posLeft[0].item(), posRight[1].item(
                )] + self.key[posRight[0].item(), posLeft[1].item()]
            newChars.append(newChar)
        return ''.join(newChars).upper()

    def decrypt(self, text):
        text = "".join([c for c in text.lower() if c.isalpha()])
        bi_gram = self.__createBigram(text)
        newChars = []
        for leftChar, rightChar in bi_gram:
            posLeft = np.where(self.key == leftChar)
            posRight = np.where(self.key == rightChar)
            newChar = ""
            if (posLeft[0].item() == posRight[0].item()):  # Same row
                newChar = self.key[posLeft[0].item(), (posLeft[1].item(
                )-1) % 5] + self.key[posRight[0].item(), (posRight[1].item()-1) % 5]
            elif (posLeft[1].item() == posRight[1].item()):  # Same Column
                newChar = self.key[(posLeft[0].item()-1) % 5, posLeft[1].item()] + \
                    self.key[(posRight[0].item()-1) % 5, posRight[1].item()]
            else:
                newChar = self.key[posLeft[0].item(), posRight[1].item(
                )] + self.key[posRight[0].item(), posLeft[1].item()]
            newChars.append(newChar)
        plainText = ''.join(newChars)
        plainText = plainText.replace(self.padding_char, '')
        return plainText.lower()

    def __createBigram(self, text):
        li = list(text)
        # Padding the similar neighbour
        li = [li[i]+self.padding_char if li[i] == li[i+1] else li[i]
              for i in range(len(li)-1)]
        li = ''.join(li) + text[-1]
        if (len(li) % 2 != 0):
            li = li + self.padding_char
        return [li[i:i+2] for i in range(0, len(li), 2)]

    def __uniqueString(self, text):
        uniqueList = []
        for x in list(text):
            if (x not in uniqueList):
                uniqueList.append(x)
        return ''.join(uniqueList)

    def __createMatrixKey(self, key):
        uniqueStr = self.__uniqueString(key).replace(self.escape_char, '')

        chars = ascii_lowercase[:26]
        chars = chars.replace(self.escape_char, '')
        chars = [c for c in list(chars) if c not in list(uniqueStr)]

        key = np.array(list(uniqueStr) + chars).reshape(5, -1)
        return key
