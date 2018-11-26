import FeedforwardNeuralNet as NetClass
import numpy as np

size = [4, 5, 3]
net = NetClass.NeuralNet(size)

input_temp = [[0.4], [0.1], [0.6], [0.8]]
input_array = np.array(input_temp)
print(input_array)

output = net.process_input(input_array)
print(output, "\n\n", output[-1])

new_input = net.input_from_output(output[-1])
print(new_input)

new_output = net.process_input(new_input)
print("\n\n", new_output)
