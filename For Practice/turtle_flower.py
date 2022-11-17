import turtle

def flower(obj="bob", rad=120, arc=60, side=7):
    obj = turtle.Turtle()
    obj.speed(0)

    for i in range(1, side+1):
        obj.circle(rad, arc) # drawing half of the petal
        obj.circle(rad, -arc)# returning home
        obj.right(180-arc)   # reposition itself and prepare for the next petal, since we need the circle drawn in the oppositie direction obj.circle(rad, -arc), we have to turn (180-arc)degrees
        obj.circle(rad, -arc)# drawing the other half of the petal
        obj.circle(rad, arc) # returning home
        obj.setheading(360/side * i) # setting the direction for the petal to go

    turtle.mainloop()

flower("bob", 1000, 10, 180)
