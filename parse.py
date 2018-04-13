"""
Programming Assignment 3
Authors: Meelad Dawood and Chris Jung
Date: 11/30/17
"""
import sys

arg_list = sys.argv
input_filename = open(arg_list[1])
output_filename = arg_list[2]

map = {}
new_map = {}
input_string = ""
desired_string = ""
alphabet = []

# Read lines from input file
with input_filename as f:
    lines = [line.rstrip('\n') for line in f]
    count = len(lines[0])
    for letter in lines[0]:
        new_map[letter] = {letter:letter}
        alphabet.append(letter)
    current = 1
    for x in lines[0]:
        line = lines[current]
        index = 1
        for y in lines[0]:
            map[x + y] = line[index - 1:index]
            index += 1
        index = 1
        current += 1
    input_string = lines[current]
    desired_string = lines[current + 1]
input_filename.close()

sys.stdout = open(output_filename, 'wt')
for initial_entry in map:
    new_map[initial_entry] = {initial_entry:map[initial_entry]}

def createNew(first, second):
    """Parenthesizes left/right strings based on guidelines.
    :param first: The first string to be parenthesized
    :param second: The second string to be parenthesized
    :return: Parenthesized string
    """
    new_str = None
    if len(first) < len(second) and len(first) == 1:
        new_str = first + "(" + second + ")"
    elif len(first) > len(second) and len(second) == 1:
        new_str = "(" + first + ")" + second
    else:
        new_str = "(" + first + ")" + "(" + second + ")"
    return new_str

def check(s):
    """Fills the table "new_map" with parenthesized versions of substrings
    Table values will be returned later to output file
    :param s: The source string to parenthesize
    """

    # Start a new table entry for string
    if s not in new_map:
        new_map[s] = {}

    # Split string into possible substrings, populate table for each substring
    for i in range(1, len(s)):
        key = s[:i]
        left_over = s[i:]
        key_value = None
        left_over_value = None

        # Strings of length 1 and 2 already in "map"
        if len(key) == 1:
            key_value = key
        if len(left_over) == 1:
            left_over_value = left_over
        if len(key) == 2:
            key_value = map[key]
        if len(left_over) == 2:
            left_over_value = map[left_over]

        """
        If left or right substring has no table values, populate its entry by
        recursively calling "check" on the left or right. This will fill 
        the table for the substring(s) at the following step.
        """
        if key_value is None or left_over_value is None:
            if key_value is None:
                check(key)
            if left_over_value is None:
                check(left_over)

        # At this level, store all possible parenthesized combinations of the string
        for key_entry in new_map[key]:
            for left_entry in new_map[left_over]:
                to_check = new_map[key][key_entry] + new_map[left_over][left_entry]
                map_value = map[to_check]
                to_add = createNew(key_entry, left_entry)
                if to_add not in new_map[s]:
                    new_map[s][to_add] = map_value

check(input_string)

# Print the table values for the input string to the output file
if bool(new_map[input_string]):
    printed = False
    for result in reversed(sorted(new_map[input_string], key=str.upper)):
        if new_map[input_string][result] == desired_string:
            print(result)
            if not printed:
                printed = True
if not printed:
    print("Not possible")