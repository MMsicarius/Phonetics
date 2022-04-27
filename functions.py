import errors

numeric_keywords = [ "ADD", "SUB", "MULTIPLY", "DIVIDE", "EQUALS"]

numeric_keywords_translate = ["+", "-", "*", "/", "="]

# INPUT
generic_keywords = ["DISPLAY", "NEWLINE"]
# OUTPUT
variable_keywords = ["INT", "STRING"]

def is_keyword(x):

    if x in generic_keywords:
        index = generic_keywords.index(x)
        return "gen_keyword"
    elif x in variable_keywords:
        index = variable_keywords.index(x)
        return "var_keyword"
    elif x in numeric_keywords:
        index = numeric_keywords.index(x)
        return numeric_keywords_translate[index]
    else:
        return "false"

def is_variable(x):
    if x in generic_keywords:
        return "false"
    else:
        return "true"

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