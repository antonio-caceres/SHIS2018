import os, imageio
import numpy as np
import FeedforwardNeuralNet as NetClass
import WeightFileReaderWriter as Writer

size = [784, 15, 10]
net = NetClass.NeuralNet(size, learning_rate=0.30)

new_weights, new_biases = Writer.read_weight_file("Weights.txt", net)
net.weight_matrices = new_weights
net.bias_matrices = new_biases

file_names = []
orig_inputs = []
for file_name in os.listdir(os.getcwd() + "/data/user"):
    if file_name != '.DS_Store':
        file_names.append(file_name)
        orig_inputs.append(imageio.imread("data/user/" + file_name, as_gray=True))


def process_input_data(data_list):
    """
    Process a list of inputs, where one input is a 2D array of integers corresponding to the pixels of the images, by
    dividing each input by 256 to limit the inputs to values between 0 and 1.
    :param data_list: a list of 2D numpy arrays of integers, where each array is one input.
    :return: a list of numpy column arrays with length 784, with floats between 0 and 1.
    """
    processed_inputs = []
    for old_input in data_list:
        new_input = []
        for row in old_input:
            for element in row:
                new_input.append([element/256])
        processed_inputs.append(np.array(new_input))
    return processed_inputs


new_inputs = process_input_data(orig_inputs)
outputs = []
for image_input in new_inputs:
    output_array = net.process_input(image_input)
    outputs.append(output_array[-1])
