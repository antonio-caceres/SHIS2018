import FeedforwardNeuralNet as NetClass
import numpy as np

net = NetClass.NeuralNet([4, 5, 3], .15)  # initializes with random weights
print(net.weight_matrices, "\n\n", net.bias_matrices, "\n\n")

inputs = np.transpose(np.array([[4, 6, 1, 3]]))
print("Inputs: ", [inputs])

output = net.process_input(inputs)
print(inputs, "\n\n", output)  # tested it and it works!!
