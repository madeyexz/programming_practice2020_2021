from decimal import Decimal, Context

def prime_greater_thatn_1000(power):
    print(power)

    ctx = Context(prec=10000)
    number = ctx.power(Decimal(2), Decimal(power))
    number = ctx.add(number, Decimal(1))
    end = number.sqrt()

    is_prime = True
    i = Decimal(1)
    while (Decimal(i) <= Decimal(end) + Decimal(1)): # 除數的循環
        i = ctx.add(i, Decimal(1))
        if ctx.remainder(number, i) == Decimal(0):
            is_prime = False
            break

    print("")

    return is_prime

power = 1000
while True:
    power += 1
    if prime_greater_thatn_1000(power) == True:
        print("\nThe power you are finding is: ", power)
        break