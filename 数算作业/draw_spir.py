import turtle

t = turtle.Turtle()
w = turtle.Screen()

def draw_spir(turtle,n):
    if n > 0:
        t.forward(n)
        t.right(90)
        draw_spir(turtle,n-3)

draw_spir(t,100)
w.exitonclick()