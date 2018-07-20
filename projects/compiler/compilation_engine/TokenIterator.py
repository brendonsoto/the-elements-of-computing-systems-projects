class TokenIterator():
    def __init__(self, tokens):
        self.tokens = tokens
        self.currentIndex = 0

    def next(self):
        self.currentIndex += 1

    def getCurrentToken(self):
        return self.tokens[self.currentIndex]

    def getNextToken(self):
        self.next()
        if self.currentIndex >= len(self.tokens):
            raise ValueError('Error: Out of bounds. No next token exists.')
        return self.getCurrentToken()

    def isThereNextToken(self):
        return self.currentIndex < len(self.tokens) - 1
