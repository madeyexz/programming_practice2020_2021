sentence = input("")
vowels = ["a","e","i","o","u","y"]
for i in sentence:
    if i.isupper() == True:
        i = i.lower()
    if i in vowels:
        i = ""
    if (i !=("a" or "e" or "i" or "o" or "u" or "y")) and (i != " ") and (i != ""):
        i = "."+ str(i) 
    print(i, end = "")
        
