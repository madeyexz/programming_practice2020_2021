import turtle
import math

# configuring pen
pen = turtle.Turtle()
pen.hideturtle
pen.speed(0)

# condfiguring node
node = turtle.Turtle()
node.speed(0)
node.hideturtle()

# configuring point A
A = turtle.Turtle()
A.speed(0)
A.hideturtle()

# configuring point B
B = turtle.Turtle()
B.speed(0)
B.hideturtle()

# setting the title bar
screen = turtle.Screen()
screen.title("REFRACTION SIMULATOR - FERMAT'S PRINCIPLE")

def draw_dotted_line(obj, startx=0, starty=0, endx=0, endy=0, color="red"):
    # pen.speed(0)
    obj.up()
    obj.color(color)
    obj.goto(startx,starty)
    nugget_x = (endx - startx)/ 20
    nugget_y = (endy - starty)/ 20
    num = 1
    while obj.distance(endx, endy) > 10:
        obj.down()
        obj.goto(startx + nugget_x * num, starty + nugget_y * num)
        obj.up()
        num += 1
        obj.goto(startx + nugget_x * num, starty + nugget_y * num)
        num += 1
    obj.up()
        
def draw_line(startx, starty, endx, endy):
    pen.up()
    pen.goto(startx,starty)
    pen.down()
    pen.goto(endx, endy)

def draw_the_frame():
    draw_line(-300,200,300,200)
    draw_line(300,200, 300,-200)
    draw_line(300,-200,-300,-200)
    draw_line(-300,200,-300,-200)
    draw_line(200,200,200,-200)
    draw_line(200,0,-300,0)

def write_at_(posx, posy, content, size):
    pen.up()
    pen.goto(posx,posy)
    pen.down()
    pen.write(content, align= "center", font=("Times New Roman",size,"normal"))

def info():
    # log m1 v1
    write_at_(250,100,"m1\nv1=10",25)
    
    # log m2 v2
    write_at_(250,-100,"m2\nv2=8",25)
    
    # log I
    write_at_(-285,170,"I",25)
    
    # log II
    write_at_(-285,-30,"II",25)
    
    # log surface
    write_at_(250,0,"contact surface",15)

    # description
    pen.up()
    pen.goto(0,225)
    pen.write(\
        "This Python program intends to simulate the process of light beam refraction(from A to B),\naccording to Fermat's principle, light travels along the fastest path possible.\nWe calculate the path through comparing the total time light travels in both medium 1 and 2.\n\nActually, sinA/sinB ≠ v1/v2, I dunno why yet hahaha",\
         align="center", font=("Times New Roman",20, "normal"))
    
    
    # log point A
    write_at_(-230,130,"A",25)
    A.up()
    A.goto(-230,130)
    A.down()

    # draw line a
    draw_dotted_line(pen, -230, 0, -230, 130, "black")

    # log point B
    write_at_(130,-160,"B",25)
    B.up()
    B.goto(130,-135)
    B.down()
    
    # draw line b
    draw_dotted_line(pen, 130, 0, 130, -130, "black")

def distance_between_A_and_B(x1, y1, x2, y2):
    ans = math.sqrt((x2-x1) ** 2 + (y2 - y1) ** 2) # float
    return ans

def time_total(nodex=node.pos()[0], nodey=node.pos()[1]):
    nodex = int(node.xcor())
    nodey = int(node.ycor())
    Ax = int(A.xcor())
    Ay = int(A.ycor())
    Bx = int(B.xcor())
    By = int(B.ycor())
    dA_N = distance_between_A_and_B(nodex, nodey, Ax, Ay)
    dB_N = distance_between_A_and_B(nodex, nodey, Bx, By)
    v1 = 10
    v2 = 8
    timeAN = dA_N / v1
    timeBN = dB_N / v2
    ans = timeAN + timeBN
    return ans
    
def move_node_and_compare_time():
    dict_posx_time= {}
    for i in range(-300, 200, 10):
        node.up()
        node.goto(i,0)
        dict_posx_time[i] = time_total()
        draw_dotted_line(node, A.xcor() ,A.ycor(), node.xcor(), node.ycor(),  "blue")
        node.goto(i,0)
        draw_dotted_line(node, node.xcor(), node.ycor(), B.xcor(), B.ycor(), "green")
    temp = min(dict_posx_time.values())
    min_time_x = [key for key in dict_posx_time if dict_posx_time[key] == temp][0]
    node.goto(min_time_x, 0)
    node.pensize(2)
    draw_dotted_line(node, A.xcor(), A.ycor(), node.xcor(), node.ycor(), "red")
    node.goto(min_time_x, 0)
    draw_dotted_line(node, node.xcor(), node.ycor(), B.xcor(), B.ycor(), "red")
    node.goto(min_time_x, 0)
    node.write("Here", align="center", font=("Times New Roman",20, "normal"))

def info2():
    sinA = distance_between_A_and_B(A.xcor(),A.ycor(),A.xcor(),0)/distance_between_A_and_B(A.xcor(),A.ycor(),node.xcor(),node.ycor())
    sinB = distance_between_A_and_B(B.xcor(),B.ycor(),B.xcor(),0)/distance_between_A_and_B(B.xcor(),B.ycor(),node.xcor(),node.ycor())
    print("sinA = %.2f,\nsinB = %.2f,\nsinA/sinB = %.2f,\nv1/v2 = %.2f" % (sinA,sinB,sinA/sinB,10/8))

def main():
    draw_the_frame()
    info()
    move_node_and_compare_time()
    # info2()

if __name__ == "__main__":
    main()

turtle.mainloop()