import re
from random import sample

class chatBot:

    def __init__(self):
        self.textBuffer = []
        self.startWord = set()
        self.wordDict = {}
        self.conversationKeyWord = set()

    def text2sentence(self, filePath):

        self.textBuffer = []

        # reading sentences from text and adding them to the text buffer
        with open(filePath, "r") as f:
            dataBlock = f.read()

            pattern = re.compile(r'[A-Z](\w|\s|,|#|\(|\)|:|\[|\]|-|\"|\')*[.?!;\s]*')

            # use this to break text into sentences
            matches = pattern.finditer(dataBlock)

            for elem in matches:
                self.textBuffer.append(elem.group())

        return self.textBuffer

    def sentence2dict(self):

        # selecting words from sentences and adding them  to the dictionary

        wordPattern = re.compile(r'[a-zA-Z]*(\')?([a-zA-Z]|[0-9]|-)*')
        #wordPattern = re.compile(r'^\s')

        for sentence in self.textBuffer:

            matches = wordPattern.finditer(sentence)

            struct = []

            for elem in matches:

                word = elem.group()
                if word is not "":
                    struct.append(word)

            for i in range(len(struct) - 1):

                word = struct[i]
                nextWord = struct[i + 1]

                if i == 0:
                    if word not in self.startWord:
                        self.startWord.add(word)

                if self.wordDict.get(word) == None:
                    self.wordDict[word] = set()

                self.wordDict[word].add(nextWord)

            # redirecting last element to end point

            lastWord = struct[len(struct) - 1]

            if self.wordDict.get(lastWord) == None:
                self.wordDict[lastWord] = set()

            self.wordDict[lastWord].add('.')

    def newRandomSentence(self):

        # create new random sentences
        sentence = curWord = sample(self.startWord, 1)[0]

        while curWord != '.':
            curWord = sample(self.wordDict[curWord], 1)[0]

            if curWord == ".":
                sentence += curWord
            else:
                sentence += " " + curWord

        return sentence

    def newResponseSentence(self, question):
        pass

lilith = chatBot()

lilith.text2sentence("text.txt")
lilith.sentence2dict()

#for i in range(100):
#    print(lilith.newRandomSentence())