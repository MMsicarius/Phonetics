import functions
import errors

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

token = {
    "digit": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    "character": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k",
                  "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
                  "w", "x", "y", "z"],
    "operator": ["+", "-", "*", "/"],
    "identifier": ["int"],
    "whiteSpace": " "
}

digit = {1,2,3,4,5,6,7,8,9,0}
character = {"a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"}
operator = {"ADD", "SUBTRACT", "MULTIPLY", "DIVIDE"}
identifier = {"int"}

digitToken = {
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '0': 0
}

#for i, char in enumerate(input):
#    print(str(i+1).rjust(3, ' '), ':', char)

#tokenExist = token.get(["3"])
#print(tokenExist)

#tokenKey(token, "4")

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
    elif wordBroken[(counter - 1)] == "int" or wordBroken[(counter - 1)] == "str":
        tokeniser.append(["variable", i])
    else:
        errors.error[1]
    counter += 1

print(tokeniser)

variable_list = []

for i in tokeniser:
    token = i[0]
    value = i[1]
    if token in variable_list:
# TODO Parser





#for i in lexer:
#    if i.isnumeric() == True:
#        try:
