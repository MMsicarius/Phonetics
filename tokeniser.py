import functions
import errors
import classes

file = open("code.txt", "r")

code = file.read()

#print(code)

lexeme = ''
#for i, char in enumerate(input):
#    lexeme += char
#    if (i+1 < len(input)):
#        if input [i+1] == whiteSpace:
#            print(lexeme)
#            lexeme = ''
#print(lexeme)

#for i, char in enumerate(input):
#    if char != whiteSpace:
#        lexeme += char
#    if (i + 1 < len(input)):
#        if input [i + 1] == whiteSpace:
#            print(lexeme)
#            lexeme = ''
#print(lexeme)

def tokenKey(dictionary, value):
    key = []
    for keys in dictionary:
        if dictionary[key] == value:
            key.append(key)
    return key


lineScanner = code.split('\n')
#print(scanner)

wordScanner = []
wordBroken = []
tokeniser = []

for i in lineScanner:
    result = i.split(' ')
    wordScanner.append(result)

# print(wordScanner)

for i in wordScanner:
    for words in i:
        wordBroken.append(words)
    wordBroken.append("NEWLINE")

# print(wordBroken)

counter = 0
line_counter = 1

# [TOKEN, VALUE]
for i in wordBroken:
    if functions.is_keyword(i) != "false":
        tokeniser.append([functions.is_keyword(i), i])
    elif i.isnumeric() == True:
        tokeniser.append(["num", i])
    elif functions.is_variable((counter-1)) == "true":
        tokeniser.append(["variable", i])
    else:
        errors.error_call(1, line_counter)
    if i == "NEWLINE":
        line_counter += 1
    counter += 1

#print(wordBroken)
print(tokeniser)
# 0 = starting point, 1 = variable declaration,
# 2 variable creation, 3 value assignment, 4 arithmetic mode,
# 5 display mode, 6 operand handling
mode = 0  # denotes state of parser
parser_counter = 0
line_counter = 1
variable_index = []  # holds the variable name
variable_list = []  # holds the token and value
arithmetic_buffer = []  # holds all the values and operand for a specific line
arithmetic_handler = None  # holds the value before placing in the buffer
answer = None

for i in tokeniser:
    token = i[0]
    value = i[1]
    if token == "var_keyword":
        mode = 1
    elif token == "variable":
        if value not in variable_list:
            if mode == 1 and tokeniser[(parser_counter - 1)][1] == "INT":
                variable_index.append(value)
                variable_list.append([tokeniser[(parser_counter - 1)][1], None])
                mode = 2
            elif mode == 1 and tokeniser[(parser_counter - 1)][1] == "STRING":
                variable_index.append(value)
                variable_list.append(tokeniser[(parser_counter - 1)][1], None)
            else:
                errors.error_call(2, line_counter)
        elif mode == 4:
            arithmetic_handler = value
            mode = 6
        else:
            errors.error_call(2, line_counter)
    elif token == "=":
        if mode == 2:
            mode = 3
        elif mode == 0:
            mode = 4
            # TODO arithmetic
        else:
            errors.error_call(2, line_counter)
    elif token == "num":
        if mode == 3:
            if variable_list[(len(variable_list) - 1)][0] == "INT":
                variable_list[(len(variable_list)-1)][1] = value
                mode = 0
            else:
                errors.error_call(3, line_counter)
        else:
            errors.error_call(2, line_counter)
    elif token == "-":
        pass
        # TODO minus
    elif token == "+":
        pass
        # TODO add
    elif token == "*":
        pass
        # TODO multiply
    elif token == "/":
        pass
        # TODO divide
    elif token == "gen_keyword":
        if value == "NEWLINE":
            line_counter += 1
        elif value == "DISPLAY":
            mode = 5
    parser_counter += 1
    print(variable_list, variable_index)
# TODO Parser





#for i in lexer:
#    if i.isnumeric() == True:
#        try:
