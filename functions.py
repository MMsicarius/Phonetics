import errors

numeric_keywords = [ "ADD", "SUB", "MULTIPLY", "DIVIDE"]

numeric_keywords_translate = ["+", "-", "*", "/"]

# INPUT
generic_keywords = ["INT", "STRING", "DISPLAY", "NEWLINE"]
# OUTPUT
generic_keywords_translate = ["int", "str", "print", "newline"]

print(generic_keywords)

def is_keyword(x):

    if x in generic_keywords:
        index = generic_keywords.index(x)
        return generic_keywords_translate[index]
    elif x in numeric_keywords:
        index = numeric_keywords.index(x)
        return numeric_keywords_translate[index]
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