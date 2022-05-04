import errors

numeric_keywords = ["ADD", "SUB", "MULTIPLY", "DIVIDE", "EQUALS", "POWER", "OPENBRACKET", "CLOSEBRACKET", "EQUIV", "NOTEVQUIV", "GREATERTHAN, LESSTHAN"]

numeric_keywords_translate = ["+", "-", "*", "/", "=", "^", "(", ")", "==", "!=", ">", "<"]

logic_keywords = ["IF", "ELSE", "AND", "OR", "NOT"]

generic_keywords = ["DISPLAY", "NEWLINE"]

variable_keywords = ["INT", "STRING", "BOOLEAN"]

variable_list_tokeniser = []

def is_keyword(x):
    if x in generic_keywords:
        return "gen_keyword"
    elif x in variable_keywords:
        return "var_keyword"
    elif x in numeric_keywords:
        index = numeric_keywords.index(x)
        return numeric_keywords_translate[index]
    elif x in logic_keywords:
        return "logic_keyword"
    elif x == "SENTENCE":
        return "SENTENCE"
    else:
        return "false"

def variable_add(x):
    variable_list_tokeniser.append(x)

def variable_check(x):
    if x in variable_list_tokeniser:
        return "true"
    else:
        return "false"

def is_variable(x):
    if x in variable_keywords:
        return "true"
    else:
        return "false"

def addition(x, y):
    answer = x + y
    return answer

def subtraction(x, y):
    answer = x - y
    return answer

def multiply(x, y):
    answer = x * y
    return answer

def divide(x, y):
    answer = x / y
    return answer

def power(x, y):
    answer = pow(x, y)
    return answer

def boolean(x, y):
    if x == y:
        return "TRUE"
    else:
        return "FALSE"

def boolean_not_equal(x, y):
    if x != y:
        return "TRUE"
    else:
        return "FALSE"

def boolean_handling(x, y):
    if x and y == "TRUE":
        return "TRUE"
    else:
        return "FALSE"

def word_add(x, y):
    if x == "[]":
        return y
    else:
        answer = x + " " + y
        return answer

def greater_than (x, y):
    if x > y:
        return "TRUE"
    else:
        return

def less_than (x, y):
    if x < y:
        return "TRUE"
    else:
        return "FALSE"

def simple_arithmetic(x, y, var_list, var_index):
    equation = []
    priority = []
    variable_list = []
    variable_index = []
    answer_buffer = []
    midway_buffer = []
    midway_position_buffer = []
    priority_counter = 5
    counter = 0

    for i in x:
        equation.append(i)
    for i in y:
        priority.append(i)
    for i in var_list:
        variable_list.append(i)
    for i in var_index:
        variable_index.append(i)

    for i in equation:
        if i in variable_index:
            equation[counter] = variable_list[(variable_index.index(i))][1]
        counter += 1
    counter = 0

    while priority_counter > 0:
        exists = 1
        while exists >= 1:
            answer_buffer.clear()
            for i in priority:
                if i == 5 and priority_counter == 5:
                    input_1 = equation[(counter-1)]
                    input_2 = equation[(counter+1)]
                    answer = power(input_1, input_2)
                    answer_buffer.append(answer)
                    answer_buffer.append((counter-1))
                    exists += 1
                elif i == 4 and priority_counter == 4:
                    input_1 = equation[(counter - 1)]
                    input_2 = equation[(counter + 1)]
                    answer = divide(input_1, input_2)
                    answer_buffer.append(answer)
                    answer_buffer.append((counter - 1))
                    exists += 1
                elif i == 3 and priority_counter == 3:
                    input_1 = equation[(counter - 1)]
                    input_2 = equation[(counter + 1)]
                    answer = multiply(input_1, input_2)
                    answer_buffer.append(answer)
                    answer_buffer.append((counter - 1))
                    exists += 1
                elif i == 2 and priority_counter == 2:
                    input_1 = equation[(counter - 1)]
                    input_2 = equation[(counter + 1)]
                    answer = addition(input_1, input_2)
                    answer_buffer.append(answer)
                    answer_buffer.append((counter - 1))
                    exists += 1
                elif i == 1 and priority_counter == 1:
                    input_1 = equation[(counter - 1)]
                    input_2 = equation[(counter + 1)]
                    answer = subtraction(input_1, input_2)
                    answer_buffer.append(answer)
                    answer_buffer.append((counter - 1))
                    exists += 1
                else:
                    counter += 1
            exists = exists - 1
            counter = 0
            if len(answer_buffer) > 0:
                midway_buffer.clear()
                midway_position_buffer.clear()
                line_answer = answer_buffer[0]
                answer_position = answer_buffer[1]
                for i in equation:
                    if answer_position == counter:
                        line_answer = midway_buffer.append(line_answer)
                        midway_position_buffer.append(0)
                    elif (answer_position + 2) >= counter > answer_position:
                        pass
                    else:
                        midway_buffer.append((equation[counter]))
                        midway_position_buffer.append((priority[counter]))
                    counter += 1
                equation.clear()
                priority.clear()
                counter = 0
                for i in midway_buffer:
                    equation.append(i)
                for i in midway_position_buffer:
                    priority.append(i)
        priority_counter -= 1
        #  TODO equation update bug needs fixing
    return equation[0]


def arithmetic(a_buffer, p_buffer, p_max, var_list, var_index):
    arithmetic_buffer_ = a_buffer
    position_buffer = p_buffer
    position_max = p_max
    variable_list = var_list
    variable_index = var_index
    bracket_buffer = []
    bracket_position_buffer = []
    midway_buffer = []
    midway_position_buffer = []
    answer_buffer = []
    answer = None

    while position_max >= 6:
        in_bracket = 0
        counter = 0
        exists = 1
        for i in position_buffer:
            if i == position_max and in_bracket == 0:
                in_bracket = 1
                exists += 1
            elif in_bracket == 1:
                bracket_buffer.append(answer_buffer[counter])
                bracket_position_buffer.append(i)
            elif i == position_max and in_bracket == 1:
                in_bracket == 0
            counter += 1
        answer = simple_arithmetic(bracket_buffer, bracket_position_buffer, variable_list, variable_index)
        loop_counter = 0
        finished = None
        for i in bracket_buffer:
            if i == "(" and in_bracket == 0 and finished is None:
                midway_buffer.append(answer)
                midway_position_buffer.append(0)
                start_position = loop_counter
                in_bracket = 1
            elif in_bracket == 1 and i != ")":
                pass
            elif i == ")" and finished is None:
                finished = 1
            else:
                midway_buffer.append(i)
                midway_position_buffer.append((position_buffer[loop_counter]))
        arithmetic_buffer_.clear()
        position_buffer.clear()
        arithmetic_buffer_ = midway_buffer
        position_buffer = midway_position_buffer
        exists -= 1
        if exists == 0:
            position_max -= 1

    answer = simple_arithmetic(arithmetic_buffer_, position_buffer, variable_list, variable_index)

    return answer
