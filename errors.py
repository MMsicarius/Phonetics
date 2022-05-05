error = {
    1: "Error! Unknown keyword",
    2: "Error! unknown syntax",
    3: "Error! Improper type assignment",
    4: "Error! Improper type assignment through logic value (2 needed, 1 given)",
    5: "Error! Please write the appropriate WORD"
}

def error_call(x, y):
    return exit(f"{error[x]} on line {y}")

