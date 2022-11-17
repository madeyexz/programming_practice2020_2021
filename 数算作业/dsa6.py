import turtle
import random

t = turtle.Turtle()
w = turtle.Screen()

def biotree(branchlen,t,ideg):
    deg = random.randint(10,40)

    t.pensize(branchlen // 10)
    if branchlen < 10:
        t.color("green")
    else:
        t.color("brown")

    if branchlen > 5:
        t.forward(branchlen)
        t.right(deg)
        biotree(branchlen-5,t,deg)
        t.left(2*deg)
        biotree(branchlen-5,t,deg)
        t.right(deg)
        t.backward(branchlen)


size = 10

def hilbert(level, angle):
    if level == 0:
        return

    turtle.color("Blue")
    turtle.speed(1000)

    turtle.right(angle)
    hilbert(level - 1, -angle)
    turtle.forward(size)
    turtle.left(angle)
    hilbert(level - 1, angle)
    turtle.forward(size)
    hilbert(level - 1, angle)
    turtle.left(angle)
    turtle.forward(size)
    hilbert(level - 1, -angle)
    turtle.right(angle)

def pascalTriangle(numofrow):
    for i in range(numofrow):
        print(printPascal(i))

def printPascal(testVariable) :
    if testVariable == 0 :
        return [1]
    else :
        line = [1]
        previousLine = printPascal(testVariable - 1)
        for i in range(len(previousLine) - 1):
            line.append(previousLine[i] + previousLine[i + 1])
        line += [1]
    return line

def main():
    t.speed(1000)
    t.left(90)
    biotree(50,t,30)
    hilbert(4,90)

    w.exitonclick()
    pascalTriangle(10)
    
main()
