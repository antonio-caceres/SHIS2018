import FeedforwardNeuralNet
import numpy as np

ann = FeedforwardNeuralNet.NeuralNet([4, 5, 3], .15)  # initializes with random weights
print(ann.weight_matrices, "\n\n", ann.bias_matrices, "\n\n")

inputs = np.array([4, 6, 1, 3]).transpose()

output = ann.process_input(inputs)
print(inputs, "\n\n", output)  # tested it and it works!!
