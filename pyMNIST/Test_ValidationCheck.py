import NetTrainerTester as Processor
import FeedforwardNeuralNet as ANN
import numpy as np

net = ANN.NeuralNet([4, 2])
weight_matrix = [[-1, 1, 1, -1],
                 [-1, 0, -1, 1]]
net.weight_matrices = [np.array(weight_matrix)]
bias_matrix = [[0],
               [1]]
net.bias_matrices = [np.array(bias_matrix)]
inputs = [np.array([[-1], [1], [1], [0]]),
          np.array([[0], [1], [1], [-1]]),
          np.array([[1], [-1], [0], [1]]),
          np.array([[1], [-1], [0], [1]]),
          np.array([[0], [0], [0], [0]]),
          np.array([[0], [1], [1], [-1]])]
outputs = [0, 1, 1, 1, 0, 1]
num_correct = Processor.test_neural_net(list(zip(inputs, outputs)), net)
print("\n\nCorrect: ", num_correct)
