import functions
import errors

file = open("full_example.txt", "r")  # This is input file for the language to read

code = file.read()


def tokenKey(dictionary, value):
    key = []
    for keys in dictionary:
        if dictionary[key] == value:
            key.append(key)
    return key


lineScanner = code.split('\n')
# print(scanner)

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
    elif len(tokeniser) > 0 and (tokeniser[(counter - 1)][0] == "SENTENCE" or tokeniser[(counter - 1)][0] == "WORD" or
                                 tokeniser[(counter - 1)][1] == "COMMENT"):
        tokeniser.append(["WORD", i])
    elif functions.is_numeric(i) or functions.is_float(i):
        if functions.is_numeric(i):
            tokeniser.append(["num", int(i)])
        else:
            tokeniser.append(["num", float(i)])
    elif functions.is_variable(wordBroken[(counter - 1)]) == "true":
        tokeniser.append(["variable", i])
        functions.variable_add(i)
    elif functions.variable_check(i) == "true":
        tokeniser.append(["variable", i])
    elif i == "TRUE" or i == "FALSE":
        tokeniser.append(["boolean", i])
    elif i == "NONE":
        tokeniser.append(["NONE", None])
    elif i == "":
        tokeniser.append(["LINE", i])
    elif i in functions.numeric_keywords_translate:
        errors.error_call(5, line_counter)
    else:
        errors.error_call(1, line_counter)
    if i == "NEWLINE":
        line_counter += 1
    counter += 1

# Parser
# print(wordBroken)
# 0 = starting point, 1 = variable declaration,
# 2 variable creation, 3 value assignment, 4 arithmetic mode,
# 5 operand handling, 6 display handling, 7 left-side assignment,
# 8 string assignment
mode = 0  # denotes state of parser
assignment_mode = 0
equivalence_mode = 0
not_equal = 0
parser_counter = 0
line_counter = 1
boolean_handling = 0
greater_than_count = 0
resolved = 0
while_state = 1
while_counter = 0
variable_index = []  # holds the variable name
variable_list = []  # holds the token and value
assignment_buffer = []
equivalence_buffer = []
sentence_holder = []
logic_mode = 0
condition_state = ""
if_skip_state = 0
while_values = []
while_startpoint = 0
while_loop = False
while_handling = False
if_handling = False
in_while = 0
while_loop_highest_loop = 0
comment = 0
else_loop = 0
if_solved = False

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
while while_state > 0:
    while_state -= 1
    for i in tokeniser:
        token = i[0]
        value = i[1]
        if while_loop is True and value != "WHILE" and parser_counter < \
                functions.find_while_counter(while_values, while_loop_highest_loop):
            pass
        elif condition_state == "FALSE" and functions.value_check(value) is True and if_skip_state == 1:
            pass
        elif token == "logic_keyword":
            if value == "IF" and mode == 0:
                logic_mode = 1
                mode = 3
                if_handling = True
            elif value == "ELSEIF" and mode == 0 and (else_loop == 1 or if_solved is False):
                logic_mode = 1
                mode = 3
                if_handling = True
            elif value == "ELSEIF" and mode == 0 and (else_loop == 0 or if_solved is True):
                if_skip_state = 1
            elif value == "ELSE" and mode == 0 and (else_loop == 0 or if_solved is True):
                if_skip_state = 1
            elif value == "ELSE" and mode == 0 and else_loop == 1 and if_solved is False:
                pass
            elif value == "ENDELSE" and mode == 0 and else_loop == 1:
                mode = 0
                condition_state = ""
                if_skip_state = 0
            elif value == "ENDELSE" and mode == 0 and if_skip_state == 1:
                mode = 0
                condition_state = ""
                if_skip_state = 0
            elif value == "ENDIF" and mode == 0 and if_solved is False:
                mode = 0
                condition_state = ""
                if_skip_state = 0
            elif value == "ENDIF" and mode == 0 and if_solved is True:
                if_skip_state = 1
                condition_state = "FALSE"
            elif value == "WHILE" and mode == 0:
                logic_mode = 1
                mode = 3
                while_handling = True
                while_values.append(parser_counter)
                in_while += 1
            elif value == "ENDWHILE" and mode == 0:
                if while_loop is True and while_loop_highest_loop == in_while:
                    while_state += 1
                    parser_counter = 0
                    line_counter = 1
                    break
                else:
                    in_while -= 1
                    condition_state = ""
            else:
                errors.error_call(2, line_counter)
        elif token == "var_keyword":
            mode = 1
        elif token == "variable":
            if value not in variable_index:
                if mode == 1 and tokeniser[(parser_counter - 1)][1] == "NUMBER":
                    variable_index.append(value)
                    variable_list.append([tokeniser[(parser_counter - 1)][1], None])
                    mode = 2
                elif mode == 1 and tokeniser[(parser_counter - 1)][1] == "STRING":
                    variable_index.append(value)
                    variable_list.append([tokeniser[(parser_counter - 1)][1], None])
                    mode = 2
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
            elif mode == 3 and value in variable_index:
                assignment_buffer.append((variable_list[(variable_index.index(value))][1]))
                arithmetic_position_buffer.append(0)
            else:
                errors.error_call(2, line_counter)
        elif token == "SENTENCE":
            if mode == 3:
                mode = 8
            elif mode == 8:
                mode = 3
            elif mode == 4:
                mode = 8
            else:
                errors.error_call(2, line_counter)
        elif token == "WORD":
            if mode == 8:
                sentence_holder = functions.word_add(str(sentence_holder), str(value))
            elif comment == 1:
                pass
            else:
                errors.error_call(2, line_counter)
        elif token == "=":
            if mode == 2:
                mode = 3
            elif mode == 7:
                mode = 4
            else:
                errors.error_call(2, line_counter)
        elif token == "==":
            if mode == 3 and assignment_mode == 1 and boolean_handling == 0:
                answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max
                                              , variable_list, variable_index)
                equivalence_buffer.append(answer)
                equivalence_mode = 1
                assignment_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
            elif mode == 3 and assignment_mode == 1 and greater_than_count == 1:
                answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max,
                                              variable_list, variable_index)
                equivalence_buffer.append((functions.greater_than(equivalence_buffer[0], answer)))
                equivalence_mode = 1
                assignment_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
                greater_than_count = 0
                resolved = -1
            elif mode == 3 and assignment_mode == 1 and greater_than_count == -1:
                answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max,
                                              variable_list, variable_index)
                equivalence_buffer.append((functions.less_than(equivalence_buffer[0], answer)))
                equivalence_mode = 1
                assignment_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
                greater_than_count = 0
                resolved = -1
            elif mode == 3 and boolean_handling == 1:
                equivalence_buffer.append(0)
                equivalence_buffer.append(assignment_buffer[0])
                equivalence_mode = 1
                assignment_buffer.clear()
            else:
                errors.error_call(2, line_counter)
        elif token == "!=":
            if mode == 3 and assignment_mode == 1 and boolean_handling == 0:
                answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max
                                              , variable_list, variable_index)
                equivalence_buffer.append(answer)
                equivalence_mode = 1
                not_equal = 1
                assignment_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
            elif mode == 3 and assignment_mode == 1 and greater_than_count == 1:
                answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max,
                                              variable_list, variable_index)
                equivalence_buffer.append((functions.greater_than(equivalence_buffer[0], answer)))
                equivalence_mode = 1
                assignment_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
                greater_than_count = 0
                not_equal = 1
                resolved = -1
            elif mode == 3 and assignment_mode == 1 and greater_than_count == -1:
                answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max,
                                              variable_list, variable_index)
                equivalence_buffer.append((functions.less_than(equivalence_buffer[0], answer)))
                equivalence_mode = 1
                assignment_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
                greater_than_count = 0
                not_equal = 1
                resolved = -1
            elif mode == 3 and boolean_handling == 1:
                equivalence_buffer.append(0)
                equivalence_buffer.append(assignment_buffer[0])
                equivalence_mode = 1
                not_equal = 1
                assignment_buffer.clear()
            else:
                errors.error_call(2, line_counter)
        elif token == "NONE":
            if mode == 3:
                assignment_buffer.append(value)
        elif token == "num":
            if mode == 3:
                assignment_buffer.append(value)
                arithmetic_position_buffer.append(0)
                assignment_mode = 1
            elif mode == 4:
                arithmetic_buffer.append(value)
                arithmetic_position_buffer.append(0)
                mode = 5
            elif mode == 6:
                display_buffer.append(value)
            else:
                errors.error_call(2, line_counter)
        elif token == "boolean":
            if mode == 3:
                assignment_buffer.append(value)
                boolean_handling += 1
            elif mode == 4:
                equivalence_buffer.append(value)
                boolean_handling += 1
                mode = 5
            else:
                errors.error_call(2, line_counter)
        elif token == "-":
            if mode == 5:
                arithmetic_buffer.append(token)
                arithmetic_position_buffer.append(1)
                mode = 4
                if priority_max < 1:
                    priority_max = 1
            elif mode == 3 and assignment_mode == 1:
                assignment_buffer.append(token)
                arithmetic_position_buffer.append(1)
                assignment_mode = 0
                if priority_max < 1:
                    priority_max = 1
            else:
                errors.error_call(2, line_counter)
        elif token == "+":
            if mode == 5:
                arithmetic_buffer.append(token)
                arithmetic_position_buffer.append(2)
                mode = 4
                if priority_max < 2:
                    priority_max = 2
            elif mode == 3 and assignment_mode == 1:
                assignment_buffer.append(token)
                arithmetic_position_buffer.append(2)
                assignment_mode = 0
                if priority_max < 2:
                    priority_max = 2
            else:
                errors.error_call(2, line_counter)
        elif token == "*":
            if mode == 5:
                arithmetic_buffer.append(token)
                arithmetic_position_buffer.append(3)
                mode = 4
                if priority_max < 3:
                    priority_max = 3
            elif mode == 3 and assignment_mode == 1:
                assignment_buffer.append(token)
                arithmetic_position_buffer.append(3)
                assignment_mode = 0
                if priority_max < 3:
                    priority_max = 3
            else:
                errors.error_call(2, line_counter)
        elif token == "/":
            if mode == 5:
                arithmetic_buffer.append(token)
                arithmetic_position_buffer.append(4)
                mode = 4
                if priority_max < 4:
                    priority_max = 4
            elif mode == 3 and assignment_mode == 1:
                assignment_buffer.append(token)
                arithmetic_position_buffer.append(4)
                assignment_mode = 0
                if priority_max < 4:
                    priority_max = 4
            else:
                errors.error_call(2, line_counter)
        elif token == "^":
            if mode == 5:
                arithmetic_buffer.append(token)
                arithmetic_position_buffer.append(5)
                mode = 4
                if priority_max < 5:
                    priority_max = 5
            elif mode == 3 and assignment_mode == 1:
                assignment_buffer.append(token)
                arithmetic_position_buffer.append(5)
                assignment_mode = 0
                if priority_max < 5:
                    priority_max = 5
            else:
                errors.error_call(2, line_counter)
        elif token == "(":
            if mode == 4:
                bracket_priority += 1
                arithmetic_buffer.append(token)
                arithmetic_position_buffer.append(bracket_priority)
                if priority_max < bracket_priority:
                    priority_max = bracket_priority
            elif mode == 3 and assignment_mode == 0:
                bracket_priority += 1
                assignment_buffer.append(token)
                arithmetic_position_buffer.append(bracket_priority)
                if priority_max < bracket_priority:
                    priority_max = bracket_priority
            else:
                errors.error_call(2, line_counter)
        elif token == ")":
            if mode == 4:
                arithmetic_buffer.append(token)
                arithmetic_position_buffer.append(bracket_priority)
                if priority_max < bracket_priority:
                    priority_max = bracket_priority
                bracket_priority -= 1
            elif mode == 3 and assignment_mode == 0:
                assignment_buffer.append(token)
                arithmetic_position_buffer.append(bracket_priority)
                if priority_max < bracket_priority:
                    priority_max = bracket_priority
                bracket_priority -= 1
            else:
                errors.error_call(2, line_counter)
        elif token == ">":
            if mode == 3:
                answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max,
                                              variable_list, variable_index)
                equivalence_buffer.append(answer)
                assignment_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
                greater_than_count += 1
                boolean_handling += 1
                equivalence_mode = 1
            elif mode == 5:
                answer = functions.arithmetic(arithmetic_buffer, arithmetic_position_buffer, priority_max,
                                              variable_list, variable_index)
                equivalence_buffer.append(answer)
                arithmetic_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
                greater_than_count += 1
            else:
                errors.error_call(2, line_counter)
        elif token == "<":
            if mode == 3:
                answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max,
                                              variable_list, variable_index)
                equivalence_buffer.append(answer)
                assignment_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
                greater_than_count -= 1
                equivalence_mode = 1
                boolean_handling += 1
            elif mode == 5:
                answer = functions.arithmetic(arithmetic_buffer, arithmetic_position_buffer, priority_max,
                                              variable_list, variable_index)
                equivalence_buffer.append(answer)
                arithmetic_buffer.clear()
                arithmetic_position_buffer.clear()
                priority_max = 0
                greater_than_count -= 1
            else:
                errors.error_call(2, line_counter)
        elif token == "gen_keyword":
            if value == "NEWLINE":
                if mode == 6:  # displaying what is in the display buffer
                    counter = 0
                    for i in display_buffer:
                        if i in variable_index:
                            display_buffer[counter] = variable_list[(variable_index.index(i))][1]
                            counter += 1
                    print(" ".join(str(x) for x in display_buffer))
                    display_buffer.clear()
                    mode = 0
                elif mode == 0:
                    pass
                elif mode == 5 and equivalence_mode == 0:  # assigning new values to existing variables
                    if len(assignment_buffer) > 0:
                        if assignment_buffer[0] is None:
                            position = variable_index.index(assignment_buffer[0])
                            variable_list[position][1] = None
                    else:
                        for j in left_side_buffer:
                            answer = functions.arithmetic(arithmetic_buffer, arithmetic_position_buffer,
                                                          priority_max, variable_list, variable_index)
                            position = variable_index.index(j)
                            variable_list[position][1] = answer
                        arithmetic_buffer.clear()
                        arithmetic_position_buffer.clear()
                        left_side_buffer.clear()
                        priority_max = 0
                        mode = 0
                elif mode == 5 and greater_than_count != 0:
                    if greater_than_count == 1:
                        answer = functions.arithmetic(arithmetic_buffer, arithmetic_position_buffer,
                                                      priority_max, variable_list, variable_index)
                        answer = functions.greater_than(equivalence_buffer[0], answer)
                        for k in left_side_buffer:
                            position = variable_index.index(k)
                            variable_list[position][1] = answer
                        equivalence_buffer.clear()
                        arithmetic_buffer.clear()
                        arithmetic_position_buffer.clear()
                        left_side_buffer.clear()
                        priority_max = 0
                        mode = 0
                    elif greater_than_count == -1:
                        answer = functions.arithmetic(arithmetic_buffer, arithmetic_position_buffer,
                                                      priority_max, variable_list, variable_index)
                        answer = functions.less_than(equivalence_buffer[0], answer)
                        for k in left_side_buffer:
                            position = variable_index.index(k)
                            variable_list[position][1] = answer
                        equivalence_buffer.clear()
                        arithmetic_buffer.clear()
                        arithmetic_position_buffer.clear()
                        left_side_buffer.clear()
                        priority_max = 0
                        mode = 0
                elif mode == 3 and equivalence_mode == 0 and len(assignment_buffer) > 1:  # assign variable value with
                    # equation involved
                    answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer,
                                                  priority_max, variable_list, variable_index)
                    if variable_list[(len(variable_list) - 1)][0] == "NUMBER":
                        variable_list[(len(variable_list) - 1)][1] = answer
                        mode = 0
                        assignment_buffer.clear()
                        arithmetic_position_buffer.clear()
                    elif variable_list[(len(variable_list) - 1)][0] == "BOOLEAN":
                        variable_list[(len(variable_list) - 1)][1] = answer
                        mode = 0
                        assignment_buffer.clear()
                        arithmetic_position_buffer.clear()
                    else:
                        errors.error_call(3, line_counter)
                elif mode == 3 and equivalence_mode == 0 and len(
                        assignment_buffer) == 1:  # assign variable with 1 value
                    if variable_list[(len(variable_list) - 1)][0] == "NUMBER":
                        variable_list[(len(variable_list) - 1)][1] = assignment_buffer[0]
                        mode = 0
                        assignment_buffer.clear()
                        arithmetic_position_buffer.clear()
                    elif variable_list[(len(variable_list) - 1)][0] == "BOOLEAN":
                        variable_list[(len(variable_list) - 1)][1] = assignment_buffer[0]
                        mode = 0
                        boolean_handling = 0
                        assignment_buffer.clear()
                        arithmetic_position_buffer.clear()
                    elif variable_list[(len(variable_list) - 1)][0] == "STRING":
                        variable_list[(len(variable_list) - 1)][1] = assignment_buffer[0]
                        mode = 0
                        assignment_buffer.clear()
                        arithmetic_position_buffer.clear()
                    else:
                        errors.error_call(3, line_counter)
                elif mode == 3 and equivalence_mode == 1:  # assign boolean output from 2 sides
                    if greater_than_count == 1:
                        answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max,
                                                      variable_list, variable_index)
                        equivalence_buffer.append((functions.greater_than(equivalence_buffer[0], answer)))
                        boolean_handling += 1
                        assignment_buffer.clear()
                        arithmetic_position_buffer.clear()
                        priority_max = 0
                        greater_than_count = 0
                    elif greater_than_count == -1:
                        answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max,
                                                      variable_list, variable_index)
                        equivalence_buffer.append((functions.less_than(equivalence_buffer[0], answer)))
                        boolean_handling += 1
                        assignment_buffer.clear()
                        arithmetic_position_buffer.clear()
                        priority_max = 0
                        greater_than_count = 0
                    else:
                        pass
                    if boolean_handling == 2:
                        if resolved == -1:
                            assignment_result = functions.boolean_handling(equivalence_buffer[1], assignment_buffer[0])
                        else:
                            assignment_result = equivalence_buffer[1]
                        if variable_list[(len(variable_list) - 1)][0] == "BOOLEAN" and logic_mode == 0:
                            variable_list[(len(variable_list) - 1)][1] = assignment_result
                        elif logic_mode == 1:
                            logic_mode = 0
                            if assignment_result == "TRUE" and if_handling is True:
                                condition_state = "TRUE"
                                if_handling = False
                                if_solved = True
                            elif assignment_result == "TRUE" and while_handling is True:
                                while_loop = True
                                While_handling = False
                                if while_loop_highest_loop < in_while:
                                    while_loop_highest_loop += 1
                            elif assignment_result == "FALSE" and while_handling is True:
                                while_values.pop()
                                condition_state = "FALSE"
                                while_handling = False
                            else:
                                condition_state = "FALSE"
                                if_skip_state = 1
                                if_handling = False
                                else_loop = 1
                                if_solved = False
                        equivalence_mode = 0
                        boolean_handling = 0
                        assignment_buffer.clear()
                        arithmetic_position_buffer.clear()
                        equivalence_buffer.clear()
                    elif boolean_handling == 1:
                        errors.error_call(4, line_counter)
                    elif boolean_handling == 0:
                        answer = functions.arithmetic(assignment_buffer, arithmetic_position_buffer, priority_max,
                                                      variable_list, variable_index)
                        if not_equal == 1:
                            assignment_result = functions.boolean_not_equal(equivalence_buffer[0], answer)
                            not_equal = 0
                        else:
                            assignment_result = functions.boolean(equivalence_buffer[0], answer)
                        if variable_list[(len(variable_list) - 1)][0] == "BOOLEAN":
                            variable_list[(len(variable_list) - 1)][1] = assignment_result
                        elif logic_mode == 1:
                            logic_mode == 0
                            if assignment_result == "TRUE" and if_handling is True:  # if true
                                condition_state == "TRUE"
                                if_handling = False
                                if_solved = True
                            elif assignment_result == "TRUE" and while_handling is True:  # while true
                                while_loop = True
                                While_handling = False
                                if while_loop_highest_loop < in_while:
                                    while_loop_highest_loop += 1
                            elif assignment_result == "FALSE" and while_handling is True:  # while false
                                while_values.pop()
                                condition_state = "FALSE"
                                while_handling = False
                            else:  # if FALSE
                                condition_state = "FALSE"
                                if_skip_state = 1
                                if_handling = False
                                else_loop = 1
                                if_solved = False
                        mode = 0
                        equivalence_mode = 0
                        assignment_buffer.clear()
                        arithmetic_position_buffer.clear()
                        equivalence_buffer.clear()
                        priority_max = 0
                    else:
                        errors.error_call(3, line_counter)
                    mode = 0
                elif mode == 3 and len(sentence_holder) > 0:  # assigning string variable
                    variable_list[(len(variable_list) - 1)][1] = sentence_holder
                    sentence_holder = ""
                    mode = 0
                else:
                    errors.error_call(2, line_counter)
            elif value == "DISPLAY":
                if mode == 0:
                    mode = 6
                else:
                    errors.error_call(2, line_counter)
            elif value == "COMMENT":
                comment = 1
            elif value == "ENDCOMMENT":
                comment = 0
        elif token == "LINE":
            pass
        else:
            errors.error_call(2, line_counter)
        if value == "NEWLINE":
            line_counter += 1
        parser_counter += 1
