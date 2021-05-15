# Problem Set 4B
# Name: Michael Sargsyan
# Collaborators:
# Time Spent: 4 hours

import string

def load_words(file_name):
    inFile = open(file_name, 'r')
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    return wordlist

def is_word(word_list, word):
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        valWords = self.valid_words.copy()
        return valWords

    def build_shift_dict(self, shift):
        asciiLowercase = string.ascii_lowercase
        text = (self.message_text).lower()
        messageMap = {}
        for i in range(0, len(text)):
            if text[i] in asciiLowercase:
                if asciiLowercase.index(text[i]) >= 0 and 26 - asciiLowercase.index(text[i]) > shift:
                    if text[i] == self.message_text[i]:
                        value = asciiLowercase[asciiLowercase.index(text[i]) + shift]
                    else:
                        value = (asciiLowercase[asciiLowercase.index(text[i]) + shift]).upper()
                elif 26 - asciiLowercase.index(text[i]) <= shift:
                    if text[i] == self.message_text[i]:
                        value = asciiLowercase[shift - (26 - asciiLowercase.index(text[i]))]
                    else:
                        value = (asciiLowercase[shift - (26 - asciiLowercase.index(text[i]))]).upper()
                else:
                    continue
                messageMap[self.message_text[i]]= value
        return messageMap

    def apply_shift(self, shift):
        string = ""
        dictionary = Message.build_shift_dict(self, shift)
        for i in range(len(self.message_text)):
            if self.message_text[i] not in dictionary.keys():
                string += self.message_text[i]
            else:
                string += dictionary[self.message_text[i]]
        return string

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        return self.shift

    def get_encryption_dict(self):
        encryptionDict = self.encryption_dict.copy()
        return encryptionDict

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.shift = shift
        self.encrypting_dict = PlaintextMessage(self.message_text, self.shift).build_shift_dict(shift)
        self.message_text_encrypted = PlaintextMessage(self.message_text, self.shift).apply_shift(shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text)

    def decrypt_message(self):
        count = 0
        maxCount = 0
        for i in range(26):
            strToList = CiphertextMessage(self.message_text).apply_shift(i).split(' ')
            for j in strToList:
                if is_word(self.valid_words, j):
                    count += 1
                else:
                    break
            if count > maxCount:
                maxCount = count
                shift = i
                a = CiphertextMessage(self.message_text).apply_shift(shift)
        return (shift, a)

if __name__ == '__main__':
    a = Message('Hello, World!')
    print("---------Message class---------")
    print("Using build_shift_dict method")
    print("Expected output: {'H': 'L', 'e': 'i', 'l': 'p', 'o': 's', 'W': 'A', 'r': 'v', 'd': 'h'}")
    print('Actual output:', a.build_shift_dict(4))
    print("Using apply_shift method")
    print("Expected output: Lipps, Asvph!")
    print('Actual output:', a.apply_shift(4))
    print("----PlaintextMessage class-----")
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print('Now I change shift!!')
    plaintext.change_shift(3)
    print('Expected Output: khoor')
    print('Actual Output:', plaintext.get_message_text_encrypted())
    print("---CiphertextMessage class----")
    ciphertext = CiphertextMessage(get_story_string())
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())
    print("------------------------------")
