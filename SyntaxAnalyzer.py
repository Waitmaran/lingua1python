import enum

from SyntaxException import *

class SyntaxAnalyzer():
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
    
    def set_lexemes(self, lexemes):
        self.lexemes = lexemes
        return self
    
    def check_grammar(self):
        return self.__check_Variables_Declaration() and self.__check_Assignments()
    
    def __check_Variables_Declaration(self):
        return self.__check_Variable_Type() and self.__check_Variable_List()
    
    def __check_Variable_Type(self):
        buffer = None
        wrong_place_flag = False
        for lexema in self.lexemes:
            if lexema.type.name == self.LexemaType.TYPE.name:
                if wrong_place_flag:
                    raise SyntaxExceptionWrongPlace(lexema.line, lexema.lexIndex, lexema.value)
                elif buffer == None:
                    buffer = lexema.value
                    continue
                elif buffer == "Long" and lexema.value == buffer:
                    raise SyntaxExceptionUnexpectedLexem(lexema.line, lexema.lexIndex, lexema.value, ["INTEGER"], lexema.type.name)
                elif buffer == "Integer":
                    raise SyntaxExceptionUnexpectedLexem(lexema.line, lexema.lexIndex, lexema.value, [self.LexemaType.IDENTIFIER.name], lexema.type.name)
            elif lexema.type.name != self.LexemaType.DELIMITER.name:
                wrong_place_flag = True
                
        return True
    
    def __check_Variable_List(self):
        identifier_flag = False
        for lexema in self.lexemes:
            if lexema.type.name == self.LexemaType.IDENTIFIER.name:
                if not identifier_flag:
                    identifier_flag = True
                else:
                    raise SyntaxExceptionUnexpectedLexem(lexema.line, lexema.lexIndex, lexema.value, ["COMMA"], lexema.type.name)
            elif lexema.type.name == self.LexemaType.DELIMITER.name:
                if lexema.value != ",":
                    pass
                elif identifier_flag:
                    identifier_flag = False
                elif not identifier_flag:
                    raise SyntaxExceptionUnexpectedLexem(lexema.line, lexema.lexIndex, lexema.value, [self.LexemaType.IDENTIFIER.name], lexema.type.name)
            elif lexema.type.name == self.LexemaType.KEYWORD.name: 
                if not identifier_flag:
                    raise SyntaxExceptionUnexpectedLexem(lexema.line, lexema.lexIndex, lexema.value, [self.LexemaType.IDENTIFIER.name], lexema.type.name)
                break   
        
        return True

    def __check_Assignments(self):
        buffer = self.lexemes
       
        begin_index = -1
        for i, lexema in enumerate(buffer):
            if lexema.value == "Begin":
                begin_index = i
        
        buffer = buffer[begin_index:len(buffer)]
        buffer = list(filter(lambda lexema: lexema.value != "" and lexema.type.name != self.LexemaType.KEYWORD.name, buffer))
        
        # <Список присваиваний>::= <Присваивание>|<Присваивание> <Список присваиваний>
        # <Присваивание> ::= <Идент> = <Выражение> ;
        # <Выражение> ::= <Ун.оп.> <Подвыражение> | <Подвыражение>
        # <Подвыражение> ::= ( <Выражение> ) | <Операнд> | <Подвыражение> <Бин.оп.> <Подвыражение>
        # <Операнд> ::= <Идент> | <Константа>
        
        expectedType = [self.LexemaType.IDENTIFIER.name]
        
        OPERAND_FLAG = False
        OPEN_BRACKET_FLAG = False
        rule = "Rule: "
        while len(buffer) > 0:
            currentLexema = buffer.pop(0)
            if len(buffer) == 0:
                if currentLexema.type.name != self.LexemaType.SEMICOLOM.name:
                    raise SyntaxExceptionUnexpectedLexem(currentLexema.line, currentLexema.lexIndex, currentLexema.value, [self.LexemaType.SEMICOLOM.name], currentLexema.type.name)
            if currentLexema.type.name not in expectedType:
                raise SyntaxExceptionUnexpectedLexem(currentLexema.line, currentLexema.lexIndex, currentLexema.value, expectedType, currentLexema.type.name)
            else:
                match(currentLexema.type.name):
                    case self.LexemaType.IDENTIFIER.name:
                        if not OPERAND_FLAG:
                            rule += " " + currentLexema.type.name
                            expectedType = [self.LexemaType.ASSIGN.name]
                        else:
                            rule += " OPERAND"
                            expectedType = [self.LexemaType.PLUS.name,
                                            self.LexemaType.MINUS.name,
                                            self.LexemaType.DIVIDE.name,
                                            self.LexemaType.MULTIPLY.name,
                                            self.LexemaType.SEMICOLOM.name,
                                            self.LexemaType.RIGHTBRACKET.name]
                    case self.LexemaType.ASSIGN.name:
                        rule += " " + currentLexema.type.name
                        OPERAND_FLAG = True
                        expectedType = [self.LexemaType.MINUS.name,
                                        self.LexemaType.IDENTIFIER.name, 
                                        self.LexemaType.CONST.name,
                                        self.LexemaType.LEFTBRACKET.name]
                    case self.LexemaType.PLUS.name:
                        rule += " BIN.OPERATOR"
                        expectedType = [self.LexemaType.IDENTIFIER.name, 
                                        self.LexemaType.CONST.name,
                                        self.LexemaType.LEFTBRACKET.name]
                    case self.LexemaType.MINUS.name:
                        rules = rule.split(' ')
                        if rules[len(rules)-1] == "OPERAND":
                            rule += " BINARY.OPERATOR"
                        else:
                            rule += " UNARY.OPERATOR"
                        expectedType = [self.LexemaType.IDENTIFIER.name, 
                                        self.LexemaType.CONST.name,
                                        self.LexemaType.LEFTBRACKET.name]
                    case self.LexemaType.DIVIDE.name:
                        rule += " BIN.OPERATOR"
                        expectedType = [self.LexemaType.IDENTIFIER.name, 
                                        self.LexemaType.CONST.name,
                                        self.LexemaType.LEFTBRACKET.name]
                    case self.LexemaType.MULTIPLY.name:
                        rule += " BIN.OPERATOR"
                        expectedType = [self.LexemaType.IDENTIFIER.name, 
                                        self.LexemaType.CONST.name,
                                        self.LexemaType.LEFTBRACKET.name]
                    case self.LexemaType.CONST.name:
                        rule += " OPERAND"
                        expectedType = [self.LexemaType.SEMICOLOM.name,
                                        self.LexemaType.PLUS.name,
                                        self.LexemaType.MINUS.name,
                                        self.LexemaType.DIVIDE.name,
                                        self.LexemaType.MULTIPLY.name,
                                        self.LexemaType.RIGHTBRACKET.name]
                    case self.LexemaType.SEMICOLOM.name:
                        rule += " " + currentLexema.type.name
                        print(rule)
                        print()  
                        rule = "Rule: " 
                        OPERAND_FLAG = False
                        if OPEN_BRACKET_FLAG:
                            raise SyntaxExceptionRightBracket(currentLexema.line, currentLexema.lexIndex, currentLexema.value)
                        expectedType = [self.LexemaType.IDENTIFIER.name]
                    case self.LexemaType.LEFTBRACKET.name:
                        rule += " " + currentLexema.type.name
                        if OPEN_BRACKET_FLAG:
                            raise SyntaxExceptionRightBracket(currentLexema.line, currentLexema.lexIndex, currentLexema.value)
                        else:
                            OPEN_BRACKET_FLAG = True
                        expectedType = [self.LexemaType.MINUS.name,
                                        self.LexemaType.IDENTIFIER.name, 
                                        self.LexemaType.CONST.name]
                    case self.LexemaType.RIGHTBRACKET.name:
                        rule += " " + currentLexema.type.name
                        if OPEN_BRACKET_FLAG:
                            expectedType = [self.LexemaType.SEMICOLOM.name,
                                            self.LexemaType.PLUS.name,
                                            self.LexemaType.MINUS.name,
                                            self.LexemaType.DIVIDE.name,
                                            self.LexemaType.MULTIPLY.name,]  
                            OPEN_BRACKET_FLAG = False
                        else:
                            raise SyntaxExceptionLeftBracket(currentLexema.line, currentLexema.lexIndex, currentLexema.value)         
        return True
        
    

    
