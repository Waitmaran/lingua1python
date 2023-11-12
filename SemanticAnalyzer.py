import enum

from SemanticException import SemanticExceptionDuplicate, SemanticExceptionUndefined

class Lexema:
    def __init__(self, type, value, line, lexIndex):
        self.type = type
        self.value = value
        self.line = line
        self.lexIndex = lexIndex

    def __str__(self):
        return str(self.type) + "|" + str(self.value)

class SemanticAnalyzer:
    def Analyze(lexemas):
        identifierBuffer = []
        for lexema in lexemas:
            if(lexema.type.name == "DECLARATION"):
                if any([i.value == lexema.value for i in identifierBuffer]): 
                    #print("NOT OK DOUBLE DECLARATION", lexema.value)
                    raise(SemanticExceptionDuplicate(lexema.line, lexema.lexIndex, lexema.value))
                identifierBuffer.append(lexema)
            if(lexema.type.name == "OPERAND" or lexema.type.name == "IDENTIFIER"):
                if not any([i.value == lexema.value for i in identifierBuffer]):            
                    #print("NOT OK", lexema.value)
                    raise(SemanticExceptionUndefined(lexema.line, lexema.lexIndex, lexema.value))
        return True