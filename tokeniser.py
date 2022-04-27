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

# [TOKEN, VALUE]
for i in wordBroken:
    if functions.is_keyword(i) != "false":
        tokeniser.append([functions.is_keyword(i), i])
    elif i.isnumeric() == True:
        tokeniser.append(["num", i])
    elif functions.is_variable((counter-1)) == "true":
        tokeniser.append(["variable", i])
    else:
        errors.error_call(1)
    counter += 1

#print(wordBroken)
print(tokeniser)
# mode 0 = starting point, 1 = variable declaration, 2 variable creation
mode = 0
parser_counter = 0
variable_list = []

for i in tokeniser:
    token = i[0]
    value = i[1]
    if token == "var_keyword":
        mode = 1
    elif token == "variable":
        if value not in variable_list:
            if mode == 1 and tokeniser[1][(parser_counter - 1)] == "INT":
                variable_list.append(value)
                value = classes.num_variable(value, None)
                mode = 2
            elif mode == 1 and tokeniser[1][(parser_counter - 1)] == "STRING":
                variable_list.append(value)
                value = classes.str_variable(value, None)
            else:
                errors.error_call(2)
    elif token == "=":
        if mode == 2:
            tokeniser[1][parser_counter - 1].value = tokeniser[1][i]
        else:
            errors.error_call(2)
    parser_counter += 1

print(a.__dict__)
# TODO Parser





#for i in lexer:
#    if i.isnumeric() == True:
#        try:
