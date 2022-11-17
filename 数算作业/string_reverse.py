# 編寫將字符串反串的遞歸



def dp_reverse(string):

    if len(string) > 1:
        string = string[-1] + dp_reverse(string[:-1])

    return string


# print(dp_reverse('shit'))

def helper(s1,s2):
    if s1 == s2:
        return True
    else:
        return False

def dp_palcheck(string):
    if len(string) < 2:
        return True
    
    return helper(string[0],string[-1]) and dp_palcheck(string[1:-1])

print(dp_palcheck('aba'))

        