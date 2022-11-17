n = int(input(""))

lucky_number = [4, 7, 47, 74, 447, 474, 744, 477, 747, 774]
status = False
if n in lucky_number:
    status = True
else:
    for i in lucky_number:
        if n % i ==0:
            status = True
            break        
if status == True:
    print("YES")
elif status == False:
    print("NO")