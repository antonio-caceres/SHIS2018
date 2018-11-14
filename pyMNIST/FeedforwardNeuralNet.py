import numpy as np


class NeuralNet:
    weight_matrices = []
    bias_matrices = []
    learning_rate = 1

    def __init__(self, neuron_layers, learning_rate = 1):
        """
        Generate a neural network with a specified number of layers and neurons.
        :param neuron_layers: list of integers representing the number of neurons in each layer.
        :param learning_rate: learning rate of the neural network
        """
        self.weight_matrices = []
        self.bias_matrices = []
        for i in range(len(neuron_layers) - 1):
            weight_matrix = []
            for r in range(neuron_layers[i + 1]):
                weight_matrix.append(np.random.uniform(-1, 1, neuron_layers[i]))
            weight_matrix = np.array(weight_matrix)
            self.weight_matrices.append(weight_matrix)
            self.bias_matrices.append(np.array(np.random.uniform(-1, 1, neuron_layers[i+1])))
        self.learning_rate = learning_rate

    def process_input(self, input_list):
        """
        Process one input using the current weights of the neural network.
        :param input_list: numpy column np array of inputs to be fed to the input layer
        :return: np array of the output layer with given input
        """
        output = input_list
        for i in range(len(self.weight_matrices)):
            output = NeuralNet.sigmoid(np.matmul(self.weight_matrices[i], output) + self.bias_matrices[i].transpose())
        return output

    def stochastic_training_input(self, input_outputs, num_epochs, mini_batch_size):
        """
        Run several iterations of the training process, backpropagating at the end
        :param input_outputs: a list of tuples of input arrays and their expected output arrays
        :param num_epochs: the number of times to train batches
        :param mini_batch_size: the size of batches to use.
        :return: None
        """
        if mini_batch_size > len(input_outputs):
            mini_batch_size = len(input_outputs)
        for n in range(num_epochs):
            np.random.shuffle(input_outputs)
            io_batch = [input_outputs[i] for i in range(mini_batch_size)]
            cost = 0
            for i, o in io_batch:
                actual = self.process_input(i)
                cost += self.quad_cost_func(actual, o)
            cost /= len(io_batch)  # mean of all of the costs for the outputs
        # calculate cost using process_input
        # average cost over mini_batch_size number of inputs
        # Use gradient descent w/ der_sigmoid to find the instantaneous slope w/ respect to outputs
        # backprop

    @staticmethod
    def quad_cost_func(actual, expected):
        """
        Computation of the quadratic cost function for one input/output of the neural net.
        :param actual: np array of actual output values
        :param expected: np array of expected output values
        :return: a scalar value for the difference between the actual and expected values.
        """
        delta_matrix = np.abs(expected - actual)
        vec_length = np.dot(delta_matrix, delta_matrix)
        return 0.5 * vec_length  # I don't know why it's divided by 2; I'm copying the cost function from the book.

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def der_sigmoid(sig_x):
        """
        Compute the derivative of sigmoid(x) at x with the value of sigmoid(x).
        :param sig_x: takes the result of NeuralNet.sigmoid(x) to compute the derivative of sigmoid(x) at x.
        :return: the derivative of the sigmoid function at the x-value of x given the value of sigmoid(x).
        """
        return sig_x * (1 - sig_x)
