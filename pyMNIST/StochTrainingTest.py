import numpy as np
import FeedforwardNeuralNet as Net

ann = Net.NeuralNet([3, 4, 2], 0.15)

inputs = [np.array([0.1, 0.2, 0.3]),
          np.array([0.4, 0.0, 0.7]),
          np.array([0.99, 0.4, 0.2]),
          np.array([0.5, 0.7, 0.4]),
          np.array([0.3, 0.6, 0.2])]
outputs = [np.array([0.2, 0.7]),
           np.array([0.5, 0.8]),
           np.array([0.9, 0.1]),
           np.array([0.5, 0.2]),
           np.array([0.6, 0.4])]
input_outputs = list(zip(inputs, outputs))
# print(input_outputs)

ann.stochastic_training_input(input_outputs, 1, 3)
