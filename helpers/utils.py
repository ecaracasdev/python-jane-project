import re

def replacer(initial_string, ch,
         replacing_character, occurrence):
     
    # breaking a string into
    # it's every single character
    lst1 = list(initial_string)
    lst2 = list(ch)
     
    # Loop to find the occurrence
    # of the character in the string
    # and replace it with the given
    # replacing_character   
    for j in lst2:
        sub_string = j
        checklist = [i for i in range(0, len(initial_string))
              if initial_string[i:].startswith(sub_string)]
        if len(checklist)>= occurrence:
            lst1[checklist[occurrence-1]] = replacing_character
 
    return ''.join(lst1)

def is_valid_data(str):
    valid = False
    if re.match(r"[0-9]{3}", str):
        valid = True
    return valid

def is_txt(file_name):
    flag = False
    
    if re.search(r'\b.txt\b',file_name):
        flag = True
    return flag

def is_csv(file_name):
    flag = False
    if re.search(r'\b.csv\b',file_name):
        flag = True
    return flag