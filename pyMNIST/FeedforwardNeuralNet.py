import numpy as np


class NeuralNet:
    weight_matrices = []
    bias_matrices = []
    learning_rate = 1

    def __init__(self, neuron_layers, learning_rate):
        """
        Generate a neural network with a specified number of layers and neurons.
        :param neuron_layers: list of integers representing the number of neurons in each layer.
        """
        self.weight_matrices = []
        self.bias_matrices = []
        for i in range(len(neuron_layers) - 1):
            weight_matrix = []
            for r in range(neuron_layers[i + 1]):
                weight_matrix.append(np.random.ranf(neuron_layers[i]))
            weight_matrix = np.matrix(weight_matrix)
            self.weight_matrices.append(weight_matrix)
            self.bias_matrices.append(np.matrix(np.random.ranf(neuron_layers[i+1])))
        self.learning_rate = learning_rate

    def process_input(self, input_list):
        """
        Process one input using the current weights of the neural network.
        :param input_list: numpy column matrix of inputs to be fed to the input layer
        :return: matrix of the output layer with given input
        """
        output = input_list
        for i in range(len(self.weight_matrices)-1):
            output = NeuralNet.sigmoid(self.weight_matrices[i] * output + self.bias_matrices[i].transpose())
        return output

    def stochastic_training_input(self, inputs, expected_outputs):
        """
        Run several iterations of the training process, backpropagating at the end
        :param inputs: a list of inputs to be processed using stochastic gradient descent.
        :param expected_outputs: a list of expected outputs associated with the inputs.
        :return: None
        """
        delta = 0
        for i in inputs:
            delta += (np.linalg.norm(expected_outputs[i] - self.process_input(i)))**2
        delta /= 2*len(inputs)
        # finish stochastic training


    @staticmethod
    def sigmoid_matrix(matrix):
        new_matrix = []
        for r in range(len(matrix)):
            new_matrix.append([])
            for c in range(len(matrix)):
                new_matrix[r].append(NeuralNet.sigmoid(matrix[r][c]))
        return new_matrix

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))


if __name__ == "__main__":
    a = NeuralNet([4, 3, 5])
    input_matrix = (np.matrix([1, 1, 1, 1])).transpose()
    print(a.process_input(input_matrix))
