import turtle
import numpy as np

t = turtle.Turtle()
t.speed(1)
t.penup()
t.goto(0, 120)
t.write("Sigmoid Function Test", move=False, align="center", font=("Arial", 20, "bold"))
t.goto(0, 0)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


for i in np.linspace(-5, 5, num=100):
    t.goto(i*50, sigmoid(i)*100)
    t.pendown()
