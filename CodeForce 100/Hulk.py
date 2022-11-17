n = int(input(""))

lv = "that I love "
ht = "that I hate "

if n == 1:
    print("I hate it")

elif n == 2:
    print("I hate that I love it")
else:
    if n % 2 == 1:
        t = n // 2
        mid = (lv + ht) * t      
    else:
        t = n // 2
        mid = (lv + ht) * (t-1) + lv
    print("I hate " + mid + "it")