import sys
import ply.lex as lex
import ply.yacc as yacc

reserved = {

    "array": "ARRAY",
    "as": "AS",
    "break": "BREAK",
    "case": "CASE",
    "class": "CLASS",
    "default": "DEFAULT",
    "die": "DIE",
    "do": "DO",
    "echo": "ECHO",
    "else": "ELSE",
    "elseif": "ELSEIF",
    "empty": "EMPTY",
    "for": "FOR",
    "function": "FUNCTION",
    "$_POST": "POST",
    "$_GET": "GET",
    "if": "IF",
    "include": "INCLUDE",
    "list": "LIST",
    "new": "NEW",
    "print": "PRINT",
    "print_r": "PRINTR",
    "var_dump": "VARDUMP",
    "private": "PRIVATE",
    "protected": "PROTECTED",
    "public": "PUBLIC",
    "require": "REQUIRE",
    "return": "RETURN",
    "static": "STATIC",
    "switch": "SWITCH",
    "try": "TRY",
    "while": "WHILE",
    "xor": "XOR",
    "true": "TRUE",
    "false": "FALSE",




}


tokens = [
    # Open and Close Tag
    'OPENTAG', 'CLOSETAG',
    # symbols
    'PLUS', 'PLUSPLUS', 'PLUSEQUAL', 'MINUS', 'MINUSMINUS', 'MINUSEQUAL', 'TIMES',
    'TIMESTIMES', 'DIVIDE', 'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL', 'EQUAL',
    'DEQUAL', 'DISTINT', 'ISEQUAL', 'SEMI', 'COMMA', 'LPAREN', 'RPAREN', 'LBRACKET',
    'RBRACKET', 'LBLOCK', 'RBLOCK', 'COLON', 'AMPERSANT', 'HASHTAG', 'DOT', 'QUOTES',
    'APOSTROPHE', 'DOT_DOT',

    'IS_IDENTICAL', 'IS_NOT_IDENTICAL',

    # operartors
    'MUL_EQUAL', 'DIV_EQUAL', 'MOD_EQUAL', 'PLUS_EQUAL',
    'MINUS_EQUAL', 'SL_EQUAL', 'SR_EQUAL', 'AND_EQUAL', 'OR_EQUAL',
    'XOR_EQUAL', 'CONCAT_EQUAL',


    # reservadas con definiciones multiples

    "AND", "OR",

    # others
    'ID', 'IDVAR', 'NUM', 'STRING', 'VOID', 'ARROW', 'DARROW'
] + list(reserved.values())


t_ignore = " \t"
# reservadas con definiciones multiples


def t_AND(t):
    r'and|AND|\&\&'
    return t


def t_OR(t):
    r'or|OR|\|\|'
    return t

   # others


def t_VOID(t):
    r'VOID|void'
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print(chr(27)+"[1;31m"+"\t ERROR: Illegal character"+chr(27)+"[0m")
    print("\t\tLine: "+str(t.lexer.lineno)+"\t=> " + t.value[0])
    t.lexer.skip(1)


def t_OPENTAG(t):
    r'(<\?(php)?)'
    return t


def t_CLOSETAG(t):
    r'\?>'
    return t


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_DISTINT = r'!'
t_LESS = r'<'
t_GREATER = r'>'
t_SEMI = r';'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBLOCK = r'{'
t_RBLOCK = r'}'
t_COLON = r':'
t_AMPERSANT = r'\&'
t_HASHTAG = r'\#'
t_DOT = r'\.'
t_QUOTES = r'\"'
t_APOSTROPHE = r'\''


t_MUL_EQUAL = r'\*='
t_DIV_EQUAL = r'/='
t_MOD_EQUAL = r'%='
t_PLUS_EQUAL = r'\+='
t_MINUS_EQUAL = r'-='
t_SL_EQUAL = r'<<='
t_SR_EQUAL = r'>>='
t_AND_EQUAL = r'&='
t_OR_EQUAL = r'\|='
t_XOR_EQUAL = r'\^='
t_CONCAT_EQUAL = r'\.='
t_LESSEQUAL = r'<='
t_IS_NOT_IDENTICAL = r'!=='
t_IS_IDENTICAL = r"==="
t_ISEQUAL = r'=='
t_GREATEREQUAL = r'>='
t_DEQUAL = r'(!=(?!=))|(<>)'
t_ARROW = r'\->'
t_DARROW = r'=>'


def t_MINUSMINUS(t):
    r'--'
    return t


def t_PLUSPLUS(t):
    r'\+\+'
    return t


def t_TIMESTIMES(t):
    r'\*\*'
    return t


def t_DOT_DOT(t):
    r'::'
    return t


# RE OTHERS


def t_COMMENTS(t):
    r'\/\*([^*]|\*[^\/])*(\*)+\/'
    t.lexer.lineno += t.value.count('\n')


def t_COMMENTS_C99(t):
    r'(\/\/|\#)(.)*?\n'
    t.lexer.lineno += 1


def t_IDVAR(t):
    r'\$[a-zA-Z0-9_][a-zA-Z0-9_]*'
    return t


def t_NUM(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t


def t_ID(t):
    r"[a-zA-Z0-9_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, 'ID')

    return t


def t_STRING(t):
    r'(("[^"]*")|(\'[^\']*\'))'
    return t


def t_TRUE(t):
    r'true'
    return t


def t_FALSE(t):
    r'false'
    return t


def get_lexer():
    return lex.lex()


lexer = lex.lex()

if __name__ == '__main__':

    if (len(sys.argv) > 1):
        script = sys.argv[1]

        scriptfile = open(script, 'r')
        scriptdata = scriptfile.read()
        lexer.input(scriptdata)
        out = open("tmp", "w+")

        print(chr(27)+"[0;36m"+"INICIA ANALISIS LEXICO"+chr(27)+"[0m")
        i = 1
        while True:
            tok = lexer.token()
            if not tok:
                break
            print("\t"+str(i)+" - "+"Line: "+str(tok.lineno) +
                  "\t"+str(tok.type)+"\t->  "+str(tok.value))
            out.write("\t" + str(i) + " - " + "Line: " + str(tok.lineno) +
                      "\t" + str(tok.type) + "\t->  " + str(tok.value)+"\n")
            i += 1

        print(chr(27)+"[0;36m"+"TERMINA ANALISIS LEXICO"+chr(27)+"[0m")

    else:
        print(chr(27)+"[0;31m"+"Pase el archivo de script PHP como parametro:")
        print(chr(27)+"[0;36m"+"\t$ python php_lexer.py" +
              chr(27)+"[1;31m"+" <filename>.txt"+chr(27)+"[0m")


def executeFunction(datafile):
    scriptfile = open(datafile, 'r')
    scriptdata = scriptfile.read()
    lexer.input(scriptdata)
    out = open("tmp", "w+")
    i = 1
    while True:
        tok = lexer.token()
        if not tok:
            break
        out.write("\t" + str(i) + " - " + "Line: " + str(tok.lineno) +
                  "\t" + str(tok.type) + "\t->  " + str(tok.value)+"\n")
        i += 1

    return
