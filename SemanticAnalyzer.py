# ЦЕЛЕВОЙ
# <Описание вычислений> ::= Begin <Список присваиваний> End.
# <Объявление переменных>::= Var <Список переменных> : <Тип переменных>
# <Список переменных> ::= <Идент>| <Идент>;<Список переменных>
# <Присваивание> ::= <Идент> := <Выражение> 

# ВХОДНОЙ
# <Описание вычислений> ::= Begin <Список присваиваний> End
# <О6ъявление переменных>::= <Тип переменных> <Список переменных>
# <Список переменных> ::= <Идент>| <Идент>,<Список переменных>
# <Присваивание> ::= <Идент> = <Выражение> ;
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

class SemanticAnalyzer():
    class LexemaType(enum.Enum):
        TYPE = 'Variable type'
        IDENTIFIER = 'Identifier'
        KEYWORD = 'Keyword'
        DELIMITER = 'Delimiter'
        LEFTBRACKET = 'Left bracket'
        RIGHTBRACKET = 'Right bracket'
        ASSIGN = 'assign'
        SEMICOLOM = 'Semicolon'
        MINUS = 'Minus'
        PLUS = 'Plus'
        DIVIDE = "Divide"
        MULTIPLY = "Multiply"
        CONST = "Const"
        LETTER = "Letter"
        OPERAND = "Operand"
        DECLARATION = "Declaration"
        DOT = "Dot"
    
    def __init__(self, lexemas):
        self.lexemas = lexemas
    
    def Analyze(self):
        identifierBuffer = []
        for lexema in self.lexemas:
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
    
    def ToTargetLanguage(self):
        typeBuffer = []
        newProgramBuffer = [Lexema(self.LexemaType.KEYWORD, "Var", 0, 0)]
        text = open("./output.txt", "w")
        for lexema in self.lexemas:
            newProgramBuffer.append(lexema)
            if(lexema.type.name == self.LexemaType.SEMICOLOM.name):
                newProgramBuffer.pop()
                newProgramBuffer.append(Lexema(self.LexemaType.DELIMITER, "\n", 0, 0))
            if(lexema.type.name == self.LexemaType.TYPE.name):
                typeBuffer.append(newProgramBuffer.pop())
            if(lexema.type.name == self.LexemaType.ASSIGN.name):
                assign = newProgramBuffer.pop()
                newProgramBuffer.append(Lexema(self.LexemaType.DELIMITER, ":", lexema.line, lexema.lexIndex+len(lexema.value)+1))
                newProgramBuffer.append(assign)
            if(lexema.type.name == self.LexemaType.KEYWORD.name and lexema.value == "End"):
                end = newProgramBuffer.pop()
                newProgramBuffer.pop()
                newProgramBuffer.append(end)
                newProgramBuffer.append(Lexema(self.LexemaType.DOT, ".", lexema.line, lexema.lexIndex+len(lexema.value)+1))
            if(lexema.type.name == self.LexemaType.KEYWORD.name and lexema.value == "Begin"):
                begin = newProgramBuffer.pop()
                newProgramBuffer.pop()
                newProgramBuffer.append(Lexema(self.LexemaType.DELIMITER, ":", lexema.line, lexema.lexIndex+len(lexema.value)+1))
                newProgramBuffer += typeBuffer
                newProgramBuffer.append(begin)
            if(lexema.type.name == self.LexemaType.DECLARATION.name):
                newProgramBuffer.append(Lexema(self.LexemaType.SEMICOLOM, ";", lexema.line, lexema.lexIndex+len(lexema.value)+1))
        for lexema in newProgramBuffer:
            if lexema.type.name == self.LexemaType.TYPE.name:
                text.write(" ")
            if lexema.value == "Begin" or lexema.value == "End":
                text.write("\n")
            text.write(lexema.value)
            if lexema.type.name == self.LexemaType.KEYWORD.name:
                text.write(" ")
            if lexema.value == "Begin":
                text.write("\n")
        text.close()