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
t.screen.reset()
t.speed(1)
t.penup()
t.goto(0, 120)
t.write("Derivative Sigmoid Function Test", move=False, align="center", font=("Arial", 20, "bold"))
t.goto(0, 0)


def der_sigmoid(sig_x):
    return sig_x * (1 - sig_x)


for i in np.linspace(-5, 5, num=100):
    y = der_sigmoid(sigmoid(i))
    t.goto(i*50, y*100)
    t.pendown()
print(-1, der_sigmoid(sigmoid(-1)))
print(0, der_sigmoid(sigmoid(0)))
print(1, der_sigmoid(sigmoid(1)))
t.screen.reset()
t.speed(1)
t.penup()
t.goto(0, 120)
t.write("Sigmoid Inverse Function Test", move=False, align="center", font=("Arial", 20, "bold"))
t.goto(0, 0)


def anti_sigmoid(x):
    return -1 * np.log((1 / x) - 1)


for i in np.linspace(0.01, 0.99, 100):
    y = anti_sigmoid(i)
    t.goto(i*100, y*50)
    t.pendown()
t.screen.reset()
t.speed(1)
t.penup()
t.goto(0, 120)
t.write("Linear Sigmoid Inverse Function Test", move=False, align="center", font=("Arial", 20, "bold"))
t.goto(0, 0)

for i in np.linspace(-5, 5, num=100):
    y = anti_sigmoid(sigmoid(i))
    t.goto(i*50, y*50)
    t.pendown()
