def parse_database(string,cursor):
    if cursor >= len(string):
        return None, cursor

    for i in range(cursor,len(string)):
        if string[i] == '{' or string[i]==',':
            break
    
    j = i + 1

    for j in range(i+1,len(string)):
        if string[j] == '}' or string[j]==',':
            break
    
    if i>= len(string) or j >= len(string):
        return None, len(string)
    else:
        tab = string[i+1:j].split(':')
        return tab,j



def parse_number(raw):
    try:
        return int(raw)
    except:
        return raw.strip(" ")

