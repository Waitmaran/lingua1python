class SyntaxException(Exception):
    def __init__(self, line, index_of_undefined, value):
        self.line = line
        self.index_of_undefined = index_of_undefined
        self.value = value

    def __str__(self):
        return repr(
            "Ошибка в строке " + str(self.line) + " по индексу " + str(self.index_of_undefined) + ": " + str(self.value))
        
class SyntaxExceptionLeftBracket(SyntaxException):
    def __init__(self, line, index_of_undefined, value):
        super().__init__(line, index_of_undefined, value)

    def __str__(self):
        return repr(super().__str__() + " / Отсутствует открывающая скобка")
    
            
class SyntaxExceptionRightBracket(SyntaxException):
    def __init__(self, line, index_of_undefined, value):
        super().__init__(line, index_of_undefined, value)

    def __str__(self):
        return repr(super().__str__() + " / Отсутствует закрывающая скобка")
    
class SyntaxExceptionUnexpectedLexem(SyntaxException):
    def __init__(self, line, index_of_undefined, value, expected, lexType):
        self.expected = expected
        self.lexType = lexType
        super().__init__(line, index_of_undefined, value)

    def __str__(self):
        buildStr =  "/ Ожидалось встретить " + str(self.expected) + ", встречено " + str(self.lexType)
        return repr(super().__str__() + str(buildStr))

class SyntaxExceptionWrongPlace(SyntaxException):
    def __init__(self, line, index_of_undefined, value):
        super().__init__(line, index_of_undefined, value)

    def __str__(self):
        buildStr =  "/ Неожиданная встреча "
        return repr(super().__str__() + str(buildStr))