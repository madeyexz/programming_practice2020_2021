import turtle

t = turtle.Turtle()
w = turtle.Screen()

def biotree(branchlen,t,deg):
    if branchlen > 5:
        t.forward(branchlen)
        t.right(deg)
        biotree(branchlen-5,t,deg)
        t.left(2*deg)
        biotree(branchlen-5,t,deg)
        t.right(deg)
        t.backward(branchlen)


def main():
    t.speed(1000)
    t.left(90)

    biotree(50,t,20)
    w.exitonclick()
    
main()

