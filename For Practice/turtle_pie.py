import turtle 

ninja = turtle.Turtle()

ninja.speed(10000)
style = ('Courier', 60, 'italic')

for i in range(180):
    ninja.forward(100)
    ninja.right(30)
    ninja.forward(20)
    ninja.left(60)
    ninja.forward(50)
    ninja.right(30)
    ninja.write('Hello!',font=style,align= "center")
    
    ninja.penup()
    ninja.setposition(0, 0)
    ninja.pendown()
    
    ninja.right(2)
    
turtle.done()