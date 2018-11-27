import turtle
import numpy as np
import FeedforwardNeuralNet as NetClass

test_names = ["Sigmoid Function Test",
              "Derivative Sigmoid Function Test",
              "Sigmoid Inverse Function Test",
              "Linear Sigmoid Inverse Function Test"]
test_linear_spaces = [(-5, 5), (-5, 5), (0.01, 0.99), (-5, 5)]
test_scaling = [(50, 100), (50, 100), (100, 50), (50, 50)]


def reset_turtle(turtle_object, i):
    turtle_object.speed(1)
    turtle_object.penup()
    turtle_object.goto(0, 120)
    turtle_object.write(test_names[i], move=False, align="center", font=("Arial", 20, "bold"))
    turtle_object.goto(0, 0)


if __name__ == "__main__":
    t = turtle.Turtle()

    for i in range(4):
        reset_turtle(t, i)
        a, b = test_linear_spaces[i]
        for j in np.linspace(a, b, num=100):
            x = j
            if i == 0:
                y = NetClass.NeuralNet.sigmoid(j)
            elif i == 1:
                y = NetClass.NeuralNet.der_sigmoid(NetClass.NeuralNet.sigmoid(j))
            elif i == 2:
                y = NetClass.NeuralNet.anti_sigmoid(j)
            else:
                y = NetClass.NeuralNet.anti_sigmoid(NetClass.NeuralNet.sigmoid(j))
            x_scaling, y_scaling = test_scaling[i]
            t.goto(x * x_scaling, y * y_scaling)
            t.pendown()
        t.screen.reset()
