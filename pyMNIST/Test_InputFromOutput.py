import FeedforwardNeuralNet as NetClass
import numpy as np

net = NetClass.NeuralNet([4, 5, 3])

input_array = np.array([[0.4], [0.1], [0.6], [0.8]])
output = net.process_input(input_array)
new_input = net.input_from_output(output[-1])
new_output = net.process_input(new_input)

if __name__ == "__main__":
    print(input_array, "\n", output, "\n\n", output[-1], "\n", new_input, "\n\n", new_output)
