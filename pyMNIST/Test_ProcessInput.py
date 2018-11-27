import FeedforwardNeuralNet as NetClass
import numpy as np

net = NetClass.NeuralNet([4, 5, 3])
inputs = np.array([[4], [6], [1], [3]])
output = net.process_input(inputs)

if __name__ == "__main__":
    print(net.weight_matrices, "\n\n", net.bias_matrices, "\n\n")
    print("Inputs: \n", inputs, "\n\nOutputs: \n", output)
