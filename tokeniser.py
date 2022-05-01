import functions
import errors
import classes

file = open("code.txt", "r")

code = file.read()

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

counter = 0
line_counter = 1

# [TOKEN, VALUE]
for i in wordBroken:
    if functions.is_keyword(i) != "false":
        tokeniser.append([functions.is_keyword(i), i])
    elif i.isnumeric():
        tokeniser.append(["num", int(i)])
    elif functions.is_variable(wordBroken[(counter-1)]) == "true":
        tokeniser.append(["variable", i])
        functions.variable_add(i)
    elif functions.variable_check(i) == "true":
        tokeniser.append(["variable", i])
    elif i == "TRUE" or i == "FALSE":
        tokeniser.append(["boolean", i])
    else:
        errors.error_call(1, line_counter)
    if i == "NEWLINE":
        line_counter += 1
    counter += 1

#print(wordBroken)
print(tokeniser)
# 0 = starting point, 1 = variable declaration,
# 2 variable creation, 3 value assignment, 4 arithmetic mode,
# 5 operand handling, 6 display handling, 7 left-side assignment
mode = 0  # denotes state of parser
parser_counter = 0
line_counter = 1
variable_index = []  # holds the variable name
variable_list = []  # holds the token and value

#  arithmetic engine
arithmetic_buffer = []  # holds all the values and operand for a specific line
arithmetic_position_buffer = []  # holds the position and priority of value
left_side_buffer = []
bracket_priority = 5
priority_max = 0  # holds the highest priority in the equation
bracket_buffer = []  # holds the values relating to within a given bracket
answer_buffer = []  # holds answers for future buffer rewrites
display_buffer = []
answer = None

for i in tokeniser:
    token = i[0]
    value = i[1]
    if token == "var_keyword":
        mode = 1
    elif token == "variable":
        if value not in variable_index:
            if mode == 1 and tokeniser[(parser_counter - 1)][1] == "INT":
                variable_index.append(value)
                variable_list.append([tokeniser[(parser_counter - 1)][1], None])
                mode = 2
            elif mode == 1 and tokeniser[(parser_counter - 1)][1] == "STRING":
                variable_index.append(value)
                variable_list.append(tokeniser[(parser_counter - 1)][1], None)
            elif mode == 1 and tokeniser[(parser_counter - 1)][1] == "BOOLEAN":
                variable_index.append(value)
                variable_list.append([tokeniser[(parser_counter - 1)][1], None])
                mode = 2
            else:
                errors.error_call(2, line_counter)
        elif mode == 0 and value in variable_index:
            left_side_buffer.append(value)
            mode = 7
        elif mode == 7 and value in variable_index:
            left_side_buffer.append(value)
        elif mode == 4:
            arithmetic_buffer.append(value)
            arithmetic_position_buffer.append(0)
            mode = 5
        elif mode == 6 and value in variable_index:
            display_buffer.append(value)
        else:
            errors.error_call(2, line_counter)
    elif token == "=":
        if mode == 2:
            mode = 3
        elif mode == 7:
            mode = 4
        else:
            errors.error_call(2, line_counter)
    elif token == "num":
        if mode == 3:
            if variable_list[(len(variable_list) - 1)][0] == "INT":
                variable_list[(len(variable_list)-1)][1] = value
                mode = 0
            else:
                errors.error_call(3, line_counter)
        elif mode == 4:
            arithmetic_buffer.append(value)
            arithmetic_position_buffer.append(0)
            mode = 5
        else:
            errors.error_call(2, line_counter)
    elif token == "boolean":
        if mode == 3:
            if variable_list[(len(variable_list) - 1)][0] == "BOOLEAN":
                variable_list[(len(variable_list) - 1)][1] = value
                mode = 0
            else:
                errors.error_call(3, line_counter)
    elif token == "-":
        if mode == 5:
            arithmetic_buffer.append(token)
            arithmetic_position_buffer.append(1)
            mode = 4
            if priority_max < 1:
                priority_max = 1
        else:
            errors.error_call(2, line_counter)
            # TODO minus string handling
    elif token == "+":
        if mode == 5:
            arithmetic_buffer.append(token)
            arithmetic_position_buffer.append(2)
            mode = 4
            if priority_max < 2:
                priority_max = 2
        else:
            errors.error_call(2, line_counter)
        # TODO add string handling
    elif token == "*":
        if mode == 5:
            arithmetic_buffer.append(token)
            arithmetic_position_buffer.append(3)
            mode = 4
            if priority_max < 3:
                priority_max = 3
        else:
            errors.error_call(2, line_counter)
        # TODO multiply
    elif token == "/":
        if mode == 5:
            arithmetic_buffer.append(token)
            arithmetic_position_buffer.append(4)
            mode = 4
            if priority_max < 4:
                priority_max = 4
        else:
            errors.error_call(2, line_counter)
        # TODO divide
    elif token == "^":
        if mode == 5:
            arithmetic_buffer.append(token)
            arithmetic_position_buffer.append(5)
            mode = 4
            if priority_max < 5:
                priority_max = 5
        else:
            errors.error_call(2, line_counter)
    elif token == "(":
        if mode == 5:
            bracket_priority += 1
            arithmetic_buffer.append(token)
            arithmetic_position_buffer.append(bracket_priority)
            mode = 4
            if priority_max < bracket_priority:
                priority_max = bracket_priority
        else:
            errors.error_call(2, line_counter)
    elif token == ")":
        if mode == 5:
            arithmetic_buffer.append(token)
            arithmetic_position_buffer.append(bracket_priority)
            mode = 4
            if priority_max < bracket_priority:
                priority_max = bracket_priority
            bracket_priority -= 1
        else:
            errors.error_call(2, line_counter)
    elif token == "gen_keyword":
        if value == "NEWLINE":
            if mode == 6:
                counter = 0
                for i in display_buffer:
                    if i in variable_index:
                        display_buffer[counter] = variable_list[(variable_index.index(i))][1]
                counter += 1
                print("".join(str(x) for x in display_buffer))
            elif mode == 5:
                for j in left_side_buffer:
                    answer = functions.arithmetic(arithmetic_buffer, arithmetic_position_buffer,
                                                  priority_max, variable_list, variable_index)
                    position = variable_index.index(j)
                    variable_list[position][1] = answer
            line_counter += 1
        elif value == "DISPLAY":
            mode = 6
    parser_counter += 1
    #print(variable_list, variable_index, mode, left_side_buffer, arithmetic_buffer, arithmetic_position_buffer)
# TODO handle boolean expression
# TODO string handling





#for i in lexer:
#    if i.isnumeric() == True:
#        try:
