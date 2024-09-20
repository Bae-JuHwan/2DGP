import turtle

t = turtle.Turtle()

move_distance = 50

def move_up():
    t.setheading(90)
    t.forward(move_distance)

def move_down():
    t.setheading(270)
    t.forward(move_distance)

def move_left():
    t.setheading(180)
    t.forward(move_distance)

def move_right():
    t.setheading(0)
    t.forward(move_distance)

turtle.onkey(move_up, 'w')
turtle.onkey(move_down, 's')
turtle.onkey(move_left, 'a')
turtle.onkey(move_right, 'd')

turtle.listen()

turtle.mainloop()
