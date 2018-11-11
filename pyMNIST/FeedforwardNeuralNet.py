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
                weight_matrix.append(np.random.ranf(neuron_layers[i])) # TODO: add negative chance
            weight_matrix = np.matrix(weight_matrix)
            self.weight_matrices.append(weight_matrix)
            self.bias_matrices.append(np.matrix(np.random.ranf(neuron_layers[i+1])))  # TODO: add negative chance
        self.learning_rate = learning_rate

    def process_input(self, input_list):
        """
        Process one input using the current weights of the neural network.
        :param input_list: numpy column matrix of inputs to be fed to the input layer
        :return: matrix of the output layer with given input
        """
        output = input_list
        for i in range(len(self.weight_matrices)):
            output = NeuralNet.sigmoid(self.weight_matrices[i] * output + self.bias_matrices[i].transpose())
        return output

    def stochastic_training_input(self, input_outputs, num_epochs, mini_batch_size):
        """
        Run several iterations of the training process, backpropagating at the end
        :param input_outputs: a list of tuples of inputs and their expected outputs
        :param num_epochs: the number of times to train batches
        :param mini_batch_size: the size of batches to use.
        :return: None
        """
        pass  # to finish one training path

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))
