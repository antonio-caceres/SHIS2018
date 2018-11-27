import os
import sys
import imageio
import numpy as np
from utils import mnist_reader
import FeedforwardNeuralNet as NetClass
import NetTrainerTester as Processor
import WeightFileReaderWriter as Writer

x_test, y_test = mnist_reader.load_mnist('data/mnist', kind='t10k')


def process_bitmap_input_data(data_list):
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
                new_input.append([(255 - element)/256])
        processed_inputs.append(np.array(new_input))
    return processed_inputs


def get_inputs_and_files():
    orig_inputs = []
    file_names = []
    for file_name in os.listdir(os.getcwd() + "/data/user"):
        if file_name != '.DS_Store':
            orig_inputs.append(imageio.imread("data/user/" + file_name, as_gray=True))
            file_names.append(file_name)
    return orig_inputs, file_names


def get_outputs(net, input_list):
    outputs = []
    for image_input in input_list:
        output_array = net.process_input(image_input)
        outputs.append(output_array[-1])
    return outputs


def draw_input_in_ascii(output):
    i = 0
    for r in range(28):
        for c in range(28):
            char = '.'
            if output[i] != 0:
                char = '#'
            sys.stdout.write(char)
            i += 1
        sys.stdout.write("\n")
    sys.stdout.write("\n")


if __name__ == "__main__":
    size = [784, 15, 10]
    net = NetClass.NeuralNet(size, learning_rate=0.30)

    # import weights and biases from the file
    new_weights, new_biases = Writer.read_weight_file("Weights.txt", net)
    net.weight_matrices = new_weights
    net.bias_matrices = new_biases

    orig_inputs, file_names = get_inputs_and_files()

    new_inputs = process_bitmap_input_data(orig_inputs)
    new_outputs = get_outputs(net, new_inputs)

    # test_inputs = Processor.process_input_data(x_test)  # for the mnist dataset

    for i in range(len(new_inputs)):
        print("\n\n", file_names[i], "\n")
        draw_input_in_ascii(new_inputs[i])
