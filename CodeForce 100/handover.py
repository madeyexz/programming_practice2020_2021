
n = float(input("How many cards do you want to overhand?"))

def hangover(n):
    cards = 0
    for i in range(1, n+1):
        cards += 1/i
    return cards

print(hangover(n))


