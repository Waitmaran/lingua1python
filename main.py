import enum
import LexerExeption
from prettytable import PrettyTable
from SemanticAnalyzer import SemanticAnalyzer

from SyntaxAnalyzer import SyntaxAnalyzer


# Вариант 11

# <Программа> ::= <Объявление переменных> <Описание вычислений>

# <О6ъявление переменных>::= <Тип переменных> <Список переменных>
# <Тип переменных> ::= Integer|Long Integer
# <Список переменных> ::= <Идент>| <Идент>,<Список переменных>

# <Описание вычислений> ::= Begin <Список присваиваний> End
# <Список присваиваний>::= <Присваивание>|<Присваивание> <Список присваиваний>

# <Присваивание> ::= <Идент> = <Выражение> ;
# <Выражение> ::= <Ун.оп.> <Подвыражение> | <Подвыражение>
# <Подвыражение> ::= ( <Выражение> ) | <Операнд> | <Подвыражение> <Бин.оп.> <Подвыражение>

# <Ун.оп.> ::= "-"
# <Бин.оп.> ::= "-" | "+" | "*" | "/"
# <Операнд> ::= <Идент> | <Константа>
# <Константа> ::= <Цифра> <Константа> | <Цифра>
# <Идент> ::= <Буква> <Идент> | <Буква>

class LanguageLexemes:
    binary_operators = ["-", "+", "*", "/"]
    unary_operators = ["-"]
    variable_types = ["Integer", "Long"]
    keywords = ["End", "Begin"]
    delimiters_in_variables = [",", " ", "\n"]
    delimiters_in_assignments = ["(", ")", "=", ";", " ", "\n"]

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


class Lexema:
    def __init__(self, type, value, line, lexIndex):
        self.type = type
        self.value = value
        self.line = line
        self.lexIndex = lexIndex

    def __str__(self):
        return str(self.type) + "|" + str(self.value)


def check_for_undefined_in_variables(variables):
    lines = variables.split("\n")
    for lineIndex, line in enumerate(lines):
        for charIndex, char in enumerate(line):
            if not (char.isalpha()):
                if not (char in LanguageLexemes.delimiters_in_variables or
                        char == "\n"):
                    raise LexerExeption.LexerUndefinedException(lineIndex + 1, charIndex, char)


def check_for_undefined_in_assignments(assignments, variables_lines_count):
    lines = assignments.split("\n")
    for lineIndex, line in enumerate(lines):
        for charIndex, char in enumerate(line):
            if not (char.isdigit() or char.isalpha()):
                if not (char in LanguageLexemes.delimiters_in_assignments or
                        char in LanguageLexemes.binary_operators or
                        char in LanguageLexemes.unary_operators or
                        char == "\n"):
                    raise LexerExeption.LexerUndefinedException(lineIndex + variables_lines_count, charIndex, char)


def stripLexemasVariable(variables):
    preparedText = variables
    lexemas = []
    buffer = ""
    line = 1
    indexOffset = 0
    for charIndex, char in enumerate(preparedText):
        if char in LanguageLexemes.delimiters_in_variables:
            if buffer in LanguageLexemes.variable_types:
                lexemas.append(Lexema(LanguageLexemes.LexemaType.TYPE, buffer, line, charIndex - len(buffer) - indexOffset))
            else:
                if len(buffer) > 0:
                    lexemas.append(Lexema(LanguageLexemes.LexemaType.IDENTIFIER, buffer, line,  charIndex - len(buffer) - indexOffset))
            buffer = ""
            lexemas.append(Lexema(LanguageLexemes.LexemaType.DELIMITER, char.strip(), line, charIndex - len(buffer) - indexOffset))
            if char == "\n":
                line += 1
                indexOffset = charIndex+1
        else:
            buffer += char
    if len(buffer) > 0:
        if buffer in LanguageLexemes.variable_types:
            lexemas.append(Lexema(LanguageLexemes.LexemaType.TYPE, buffer, line, len(preparedText) - len(buffer) - indexOffset))
        else:
            lexemas.append(Lexema(LanguageLexemes.LexemaType.IDENTIFIER, buffer, line, len(preparedText) - len(buffer) - indexOffset))
    return lexemas


def build_and_print_lexemes_table(lexemas):
    my_table = PrettyTable()
    my_table.field_names = ["Type", "Value", "Line", "Index"]
    for lexeme in lexemas:
        my_table.add_row([lexeme.type.value, lexeme.value, lexeme.line, lexeme.lexIndex])
    print(my_table)


def stripLexemasAssignments(assignments, variabbles_lines_count):
    preparedText = assignments
    lexemas = []
    buffer = ""
    line = variabbles_lines_count
    indexOffset = 0
    for charIndex, char in enumerate(preparedText):
        if char in LanguageLexemes.delimiters_in_assignments or char in LanguageLexemes.binary_operators or char in LanguageLexemes.unary_operators:
            if buffer in LanguageLexemes.variable_types:
                lexemas.append(Lexema(LanguageLexemes.LexemaType.TYPE, buffer, line, charIndex - len(buffer) - indexOffset))
            elif buffer in LanguageLexemes.keywords:
                lexemas.append(Lexema(LanguageLexemes.LexemaType.KEYWORD, buffer, line, charIndex - len(buffer) - indexOffset))
            elif buffer.isnumeric():
                lexemas.append(Lexema(LanguageLexemes.LexemaType.CONST, buffer, line, charIndex - len(buffer)- indexOffset))
            else:
                if len(buffer) > 0:
                    lexemas.append(Lexema(LanguageLexemes.LexemaType.IDENTIFIER, buffer, line, charIndex - len(buffer) - indexOffset))
            buffer = ""
            if char.strip() == "(":
                lexemas.append(Lexema(LanguageLexemes.LexemaType.LEFTBRACKET, char.strip(), line, charIndex - len(buffer) - indexOffset))
            elif char.strip() == ")":
                lexemas.append(Lexema(LanguageLexemes.LexemaType.RIGHTBRACKET, char.strip(), line, charIndex - len(buffer) - indexOffset))
            elif char.strip() == "=":
                lexemas.append(Lexema(LanguageLexemes.LexemaType.ASSIGN, char.strip(), line, charIndex - len(buffer) - indexOffset))
            elif char.strip() == ";":
                lexemas.append(Lexema(LanguageLexemes.LexemaType.SEMICOLOM, char.strip(), line, charIndex - len(buffer) - indexOffset))
            elif char.strip() == "+":
                lexemas.append(Lexema(LanguageLexemes.LexemaType.PLUS, char.strip(), line, charIndex - len(buffer) - indexOffset))
            elif char.strip() == "-":
                lexemas.append(Lexema(LanguageLexemes.LexemaType.MINUS, char.strip(), line, charIndex - len(buffer) - indexOffset))
            elif char.strip() == "*":
                lexemas.append(Lexema(LanguageLexemes.LexemaType.MULTIPLY, char.strip(), line, charIndex - len(buffer) - indexOffset))
            elif char.strip() == "/":
                lexemas.append(Lexema(LanguageLexemes.LexemaType.DIVIDE, char.strip(), line, charIndex - len(buffer) - indexOffset))
            if char == "\n":
                line += 1
                indexOffset = charIndex+1
        else:
            buffer += char
    if len(buffer) > 0:
        if buffer in LanguageLexemes.keywords:
            lexemas.append(Lexema(LanguageLexemes.LexemaType.KEYWORD, buffer, line, len(preparedText) - len(buffer) - indexOffset))
        elif buffer in LanguageLexemes.variable_types:
            lexemas.append(Lexema(LanguageLexemes.LexemaType.TYPE, buffer, line, len(preparedText) - len(buffer) - indexOffset))
        elif buffer.isnumeric():
            lexemas.append(Lexema(LanguageLexemes.LexemaType.CONST, buffer, line, len(preparedText) - len(buffer) - indexOffset))
        else:
            lexemas.append(Lexema(LanguageLexemes.LexemaType.IDENTIFIER, buffer, line, len(preparedText) - len(buffer) - indexOffset))
    return lexemas


if __name__ == '__main__':
    text = open("./program.txt").read()
    if "Begin" in text and "End" in text and ";" in text and ("Integer" in text or "Long Integer" in text):
        variables = text[0:text.index("Begin")]
        assignments = text[text.index("Begin"):text.index("End") + 3]
        check_for_undefined_in_variables(variables)
        check_for_undefined_in_assignments(assignments, len(variables.split("\n")))
        lexemes = stripLexemasVariable(variables)
        lexemes.extend(stripLexemasAssignments(assignments, len(variables.split("\n"))))
        build_and_print_lexemes_table(lexemes)
        
        forSemantic = SyntaxAnalyzer().set_lexemes(lexemes).check_grammar()
        semAnalyzer = SemanticAnalyzer(forSemantic)
        if (semAnalyzer.Analyze()):
            print("УСПЕШНО")
            
        semAnalyzer.ToTargetLanguage()
        
    else:
        if "Begin" not in text:
            raise LexerExeption.LexerMissingLexem("Begin")
        elif ";" not in text:
            raise LexerExeption.LexerMissingLexem(";")
        elif "End" not in text:
            raise LexerExeption.LexerMissingLexem("End")
        elif "Integer" not in text:
            raise LexerExeption.LexerMissingLexem("Integer или Long Integer")
