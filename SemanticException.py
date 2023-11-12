class SemanticException(Exception):
    def __init__(self, line, index_of_undefined, value):
        self.line = line
        self.index_of_undefined = index_of_undefined
        self.value = value

    def __str__(self):
        return repr(
            "Ошибка в строке " + str(self.line) + " по индексу " + str(self.index_of_undefined) + ": " + str(self.value))
        
class SemanticExceptionDuplicate(SemanticException):
    def __init__(self, line, index_of_undefined, value):
        super().__init__(line, index_of_undefined, value)

    def __str__(self):
        return repr(super().__str__() + " / Дублированное определение")
    
class SemanticExceptionUndefined(SemanticException):
    def __init__(self, line, index_of_undefined, value):
        super().__init__(line, index_of_undefined, value)

    def __str__(self):
        return repr(super().__str__() + " / Переменная не определена")