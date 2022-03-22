import errors

numeric_keywords = {
    "ADD": "+",
    "SUB": "-",
    "MULTIPLY": "*",
    "DIVIDE": "/"
}

generic_keywords = {
    "int": "INT",
    "string": "STR"
}

def is_keyword(x):
    word = x
    if word in numeric_keywords:
        return numeric_keywords[word]
    elif word in generic_keywords:
        return generic_keywords[word]
    else:
        return "false"

def addition():
    return 0
    #TODO addition function

def subtraction():
    return 0
    #TODO subtraction function

def multiply():
    return 0
    #TODO multiply function

def division():
    return 0
    #TODO division function