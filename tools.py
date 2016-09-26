import re
import string

# extracts a single character above the ^
def char_extract(lines):
    if len(lines) < 2 or not re.search(r"\^", lines[1]):
        return
    index = lines[1].index("^")
    if len(lines[0]) < index + 1:
        return
    return lines[0][lines[1].index("^")]

# extracts all characters above the first sequence of ~
def tilde_extract(lines):
    if len(lines) < 2 or not re.search(r"~", lines[1]):
        return
    start = lines[1].index("~")
    length = 1
    while len(lines[1]) > start + length and lines[1][start + length] == "~":
        length += 1
    if len(lines[0]) < start + length:
        return
    return lines[0][start:start+length]

# extracts all characters starting with the one before the first ~ and ending two after the last ~
def tilde_extract_function(lines):
    if len(lines) < 2 or "~" not in lines[1]:
        return

    start = lines[1].index("~") - 1
    end = lines[1].rfind("~") + 3
    return lines[0][start:end]

# extract the name of a variable above the ^
# by default, assumes that ^ is under the first character of the variable
# if left_aligned is set to False, ^ is under the next character after the variable
def var_extract(lines, left_aligned=True):
    if len(lines) < 2 or not re.search(r"\^", lines[1]):
        return
    permissibles = string.ascii_letters + string.digits + '_'
    index = lines[1].index("^")
    var = ""
    
    if left_aligned:
        while len(lines[0]) > index + 1 and lines[0][index] in permissibles:
            var += lines[0][index]
            index += 1
    elif len(lines[0]) > index + 1:
        index -= 1
        while index >= 0 and lines[0][index] in permissibles:
            var = lines[0][index] + var
            index -= 1
            
    if len(var) > 0:
        return var
        
    