error = {
    1: "Error! Unknown keyword",
    2: "Error! unknown syntax",
    3: "Error! Improper type assignment"
}

def error_call(x, y):
    return exit(f"{error[x]} on line {y}")
