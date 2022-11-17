for i in range(int(input(""))):
    angle = []
    for i in range(3,1000):
        angle.append((i-2)*180/i)
    print("YES" if int(input("")) in angle else "NO")