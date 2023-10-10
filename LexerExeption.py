class LexerException(Exception):
    def __init__(self, line, index_of_undefined, value):
        self.line = line
        self.index_of_undefined = index_of_undefined
        self.value = value

    def __str__(self):
        return repr(
            "Ошибка в строке " + str(self.line) + " по индексу " + str(self.index_of_undefined) + ": " + str(self.value))

class LexerUndefinedException(LexerException):
    def __init__(self, line, index_of_undefined, value):
        super().__init__(line, index_of_undefined, value)

    def __str__(self):
        return repr(super().__str__() + " / Лексема не определена")

class LexerMissingLexem(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr("Отсутсвует обязательная лексема " + self.value)
