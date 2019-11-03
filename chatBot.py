import re
from random import sample, choice

class rules:
    def __init__(self):
        self.searchLimit = 100
        self.personConverter = {
                                "i": "you",
                                "you": "i",
                                "we": "you",
                                "am": "are",
                                "are": "am",
                                "me": "you",
                                "us": "you"
                                }

class chatBot(rules):

    def __init__(self):

        super().__init__()

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

    def questionCurater(self, question):

        question = question.lower()

        wordPattern = re.compile(r'[a-zA-Z]*(\')?([a-zA-Z]|[0-9]|-)*')

        matches = wordPattern.finditer(question)

        question = []

        for elem in matches:
            if elem.group() != '':
                question.append(elem.group())

        question.append('.')

        for i in range(len(question)):
            word = question[i]
            if self.personConverter.get(word) != None:
                question[i] = self.personConverter[word]

        return question

    def words2sentence(self, wordSet, startWord, sentence):

        needsToBeInSet = choice([True])
        curWord = sample(self.wordDict[startWord], 1)[0]

        if needsToBeInSet:

            cnt = 0
            while curWord not in wordSet and cnt <= self.searchLimit:
                curWord = sample(self.wordDict[startWord], 1)[0]
                cnt += 1

        if curWord is ".":
            return sentence + choice([".", "!", "?", "."])
        else:
            sentence += " " + curWord
            return self.words2sentence(wordSet, curWord, sentence)

    def newResponseSentence(self, question):

        question = self.questionCurater(question)

        #searching for the words into the start set

        startAnswer = ""

        for word in question:

            if word in self.startWord:
                startAnswer = word
                break
            else:

                capitalizeVar = word.capitalize()

                if capitalizeVar in self.startWord:
                    startAnswer = capitalizeVar
                    break
                else:

                    capsVar = word.upper()

                    if capsVar in self.startWord:
                        startAnswer = capsVar
                        break

        question = set(question)

        if startAnswer != "":
            question.remove(startAnswer.lower())
        else:
            startAnswer = sample(self.startWord, 1)[0]

        return self.words2sentence(question, startAnswer, startAnswer).capitalize()


lilith = chatBot()
lilith.text2sentence("text.txt")
lilith.sentence2dict()

question = "This shuttle needs to be destroyed."

print(lilith.newResponseSentence(question))

"""""
response = lilith.newResponseSentence(question)

for i in range(100):
    response += " " + lilith.newResponseSentence(question)

print(response)"""