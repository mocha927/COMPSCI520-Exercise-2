def is_happy(s):
    if len(s) < 3:
        return False
    else:
        distinct_count = 0
        for i in range(len(s)-2):
            if s[i:i+3] == s[i+1:] or s[i:i+3] == s[i+2]: # introduce erroneous slicing fault
                distinct_count += 1
        return distinct_count == 3