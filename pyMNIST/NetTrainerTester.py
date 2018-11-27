from utils import mnist_reader
import FeedforwardNeuralNet as NetClass
import numpy as np
import WeightFileReaderWriter


def process_input_data(data_list):
    """
    Process a list of inputs, where one input is a list of integers corresponding to the pixels of the images, by
    dividing each input by 256 to limit the inputs to values between 0 and 1.
    :param data_list: a list of lists of integers, where each list is one input.
    :return: a list of numpy column arrays with length 784, with floats between 0 and 1.
    """
    processed_inputs = []
    for old_input in data_list:
        new_input = []
        for integer in old_input:
            new_input.append([integer/256.0])
        processed_inputs.append(np.array(new_input))
    return processed_inputs


def process_output_data(data_list):
    """
    Process a list of outputs, where one output is an integer
    corresponding to the group that the input should be classified under.
    :param data_list: a list of integers, where each integer is one output.
    :return: a list of numpy arrays with length 10, with 0 at all indices except the integer from data_list
    """
    processed_outputs = []
    for old_output in data_list:
        new_output = []
        for i in range(10):
            if i == old_output:
                new_output.append([1])
            else:
                new_output.append([0])
        processed_outputs.append(np.array(new_output))
    return processed_outputs


def test_neural_net(neural_net, input_outputs):
    """
    Validate a neural network with a zipped set of inputs and outputs
    :param input_outputs: A zipped s
    :param neural_net: the neural network with which to process the data
    :return: the number of correct outputs that the network was able to achieve.
    """
    correct_counter = 0
    for i, o in input_outputs:
        actual = (neural_net.process_input(i))[-1]
        index = -1
        largest = -1
        for n in range(len(actual)):
            if actual[n][0] > largest:
                index = n
                largest = actual[n][0]
        if index == o:
            correct_counter += 1
    return correct_counter


def ann_training(net, dataset_name, train_data, test_data, num_trials, num_epochs, batch_size):
    num_correct_list = []
    for i in range(num_trials):
        net.stochastic_training_input(train_data, num_epochs, batch_size)
        num_correct = test_neural_net(net, test_data)
        num_correct_list.append(num_correct)
        print("Correct, ", i, ": ", num_correct)
    WeightFileReaderWriter.write_weights(net, dataset_name, num_trials, num_epochs, batch_size, num_correct_list)


if __name__ == "__main__":
    size = [784, 15, 10]
    net = NetClass.NeuralNet(size, learning_rate=0.30)

    # This is data from the MNIST dataset. It contains 784 length arrays with integers between 0 and 255.
    data_set = "Digits"  # "Fashion"
    if data_set == "Fashion":
        x_train, y_train = mnist_reader.load_mnist('data/fashion', kind='train')
        x_test, y_test = mnist_reader.load_mnist('data/fashion', kind='t10k')
    else:
        x_train, y_train = mnist_reader.load_mnist('data/mnist', kind='train')
        x_test, y_test = mnist_reader.load_mnist('data/mnist', kind='t10k')

    train_inputs = process_input_data(x_train)
    train_outputs = process_output_data(y_train)
    test_inputs = process_input_data(x_test)
    # No need to process test_outputs because of how the test_neural_net function works.

    train_io = list(zip(train_inputs, train_outputs))
    test_io = list(zip(test_inputs, y_test))

    ann_training(net, data_set, train_io, test_io, num_trials=3, num_epochs=24000, batch_size=5)
