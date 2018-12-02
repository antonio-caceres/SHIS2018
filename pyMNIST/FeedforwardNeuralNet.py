import numpy as np
import FileProcessor as Processor
# import ProgressBar
# TODO: Implement progress bar code into the neural network trainer.


class NeuralNet:
    def __init__(self, neuron_layers, learning_rate=.1):
        """
        Generate a neural network with a specified number of layers and neurons.
        :param neuron_layers: list of integers representing the number of neurons in each layer
        :param learning_rate: learning rate of the neural network
        """
        self.size = neuron_layers
        self.weight_matrices = []
        self.bias_matrices = []
        learning_rate = -np.abs(learning_rate)
        for i in range(len(neuron_layers) - 1):
            weight_matrix = []
            for r in range(neuron_layers[i + 1]):
                weight_matrix.append(np.random.uniform(-1, 1, neuron_layers[i]))
            self.weight_matrices.append(np.array(weight_matrix))
            bias_matrix = []
            for r in range(neuron_layers[i + 1]):
                bias_matrix.append(np.random.uniform(-1, 1, 1))
            self.bias_matrices.append(np.array(bias_matrix))
        self.learning_rate = learning_rate

    def process_input(self, input_list):
        """
        Process one input using the current weights of the neural network.
        :param input_list: numpy column np array of inputs to be fed to the input layer
        :return: np array of the output layer with given input
        """
        output = input_list
        output_values = [input_list]
        for i in range(len(self.weight_matrices)):
            output = NeuralNet.sigmoid(np.matmul(self.weight_matrices[i], output) + self.bias_matrices[i])
            output_values.append(output)
        return output_values

    def stochastic_training_input(self, input_outputs, num_epochs, mini_batch_size, epoch_callback=None):
        """
        Run several iterations of the training process, backpropagating at the end
        :param input_outputs: a list of tuples of input arrays and their expected output arrays
        :param num_epochs: the number of times to train batches
        :param mini_batch_size: the size of batches to use
        :param epoch_callback: a callback function to take the epoch number that just finished
        :return: None
        """
        if mini_batch_size > len(input_outputs):
            mini_batch_size = len(input_outputs)
        for num in range(num_epochs):
            np.random.shuffle(input_outputs)
            io_batch = [input_outputs[i] for i in range(mini_batch_size)]
            weight_deltas = []
            for x in self.weight_matrices:
                weight_deltas.append(np.zeros(x.shape))
            bias_deltas = []
            for x in self.bias_matrices:
                bias_deltas.append(np.zeros(x.shape))
            for i, o in io_batch:
                layer_outputs = self.process_input(i)  # an array of matrices, same size as weight_matrices
                layer_error = np.multiply((layer_outputs[-1] - o), self.der_sigmoid(layer_outputs[-1]))
                weight_deltas[-1] += np.matmul(layer_error, np.transpose(layer_outputs[-2]))  # from column -> row
                bias_deltas[-1] += layer_error
                for n in range(len(self.weight_matrices)-1):
                    # Each layer_output corresponds to a layer from the input to the output.
                    # Each weight_matrix corresponds to a layer from (input + 1) to the output.
                    # Each weight_ and bias_delta should corresponds to a layer from (input+1) to the output.
                    # We've already taken care of the output layer above.
                    a = np.dot(np.transpose(self.weight_matrices[-n-1]), layer_error)  # temporary value
                    b = self.der_sigmoid(layer_outputs[-n-2])  # temporary value
                    layer_error = np.multiply(a, b)
                    weight_deltas[-n - 2] += np.matmul(layer_error, np.transpose(layer_outputs[-n - 3]))
                    bias_deltas[-n - 2] += layer_error
            for i in range(len(self.weight_matrices)):
                weight_deltas[i] *= self.learning_rate / mini_batch_size
                self.weight_matrices[i] += weight_deltas[i]
                bias_deltas[i] *= self.learning_rate / mini_batch_size
                self.bias_matrices[i] += bias_deltas[i]
            if epoch_callback is not None:
                epoch_callback(num+1)

    def input_from_output(self, output_values):
        """
        Generate a matrix of inputs from a matrix of outputs.
        :param output_values: matrix of outputs to "imagine" an input from.
        :return: matrix of inputs from the outputs
        """
        reverse_output = output_values
        for i in range(len(self.weight_matrices)):
            a = np.linalg.pinv(self.weight_matrices[-i-1])
            b = NeuralNet.anti_sigmoid(reverse_output) - self.bias_matrices[-i-1]
            reverse_output = np.matmul(a, b)
        return reverse_output

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
    def der_sigmoid(sig_x):  # derivative of output with respect to sum of weights/inputs/biases
        """
        Compute the derivative of sigmoid(x) at x with the value of sigmoid(x).
        :param sig_x: takes the result of NeuralNet.sigmoid(x) to compute the derivative of sigmoid(x) at x.
        :return: the derivative of the sigmoid function at the x-value of x given the value of sigmoid(x).
        """
        return sig_x * (1 - sig_x)

    @staticmethod
    def anti_sigmoid(x):
        return -1 * np.log((1 / x) - 1)


class NetworkTrainer:
    def __init__(self, net_size, learning_rate=.1, num_trials=1, num_epochs=60000, batch_size=1,
                 dataset_name="MNIST Digits"):
        """
        Generate an object to train a neural network.
        :param net_size: the size of the layers in the neural network to be initialized
        :param learning_rate: the learning rate of the neural network to be initialized
        :param num_trials: the number of trials over which to train one neural network
        :param num_epochs: the number of epochs to run during one trial
        :param batch_size: the number of inputs to process during one epoch
        :param dataset_name: the name of the dataset with which to train and test the neural network
            Currently, the supported options are "MNIST Digits" and "MNIST Fashion".
        """
        self.net_size = net_size
        self.learning_rate = learning_rate
        self.num_trials = num_trials
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.name = dataset_name
        self.train_inputs_outputs, self.test_inputs_outputs = Processor.process_mnist_data(dataset_name)

    def training(self, num_networks):
        """
        Train a certain number of randomly initialized networks, writing weight files for each network after
        training and testing is completed.
        :param num_networks: the number of new, randomly initialized networks to train with the dataset
        :return: a list of file names and the index of the file name storing the information for the best network
        :rtype: list, int
        """
        file_list = []
        largest = 0
        index = -1
        for i in range(num_networks):
            net = NeuralNet(self.net_size, self.learning_rate)
            num_correct_list = []
            for j in range(self.num_trials):
                net.stochastic_training_input(self.train_inputs_outputs, self.num_epochs, self.batch_size)
                num_correct_list.append(self.testing(net))
                print(num_correct_list[j])
            file_name = Processor.write_net_file(net, self.name,
                                                 self.num_trials, self.num_epochs, self.batch_size,
                                                 num_correct_list)
            file_list.append(file_name)
            if num_correct_list[-1] > largest:
                index = i
                largest = num_correct_list[-1]
        return file_list, index


        # PROGRESS_BAR_DISPLAY_SIZE = 30  # set this to None to turn off progress bar output
        # if PROGRESS_BAR_DISPLAY_SIZE is not None:
        #     import ProgressBar, time, sys
        # t_start = 0
        # if PROGRESS_BAR_DISPLAY_SIZE != None:
        #     t_start = time.time()
        #     print("ann training...")
        #     ProgressBar.draw_bar(0, PROGRESS_BAR_DISPLAY_SIZE, 0)
        # for i in range(self.num_trials):
        #     if PROGRESS_BAR_DISPLAY_SIZE != None:
        #         def update_progress_bar_on_epoch(epoch_index):
        #             ProgressBar.draw_bar((float(i) / num_trials) + (float(epoch_index) / (num_epochs * num_trials)),
        #                                  PROGRESS_BAR_DISPLAY_SIZE, time.time() - t_start)
        #
        #         net.stochastic_training_input(train_data, num_epochs, batch_size, update_progress_bar_on_epoch)
        #     else:
        #     net.stochastic_training_input(train_data, num_epochs, batch_size)
        #     num_correct = test_neural_net(net, test_data)
        #     num_correct_list.append(num_correct)
        #     if PROGRESS_BAR_DISPLAY_SIZE != None:
        #         ProgressBar.draw_bar_text(float(i + 1) / num_trials, PROGRESS_BAR_DISPLAY_SIZE, time.time() - t_start)
        #         sys.stdout.write("Correct " + str(num_correct_list) + "\r")
        #     else:
        #         print("Correct: ", i, ": ", num_correct)
        # if PROGRESS_BAR_DISPLAY_SIZE != None:
        #     sys.stdout.write("ann training took " + ProgressBar.timing(time.time() - t_start, 12) + "\n")
        # WeightFileReaderWriter.write_weights(net, dataset_name, num_trials, num_epochs, batch_size, num_correct_list)
    # if PROGRESS_BAR_DISPLAY_SIZE != None: print("")

    def testing(self, net):
        """
        Test a neural network.
        :param net: trained neural network
        :return: number of testing inputs that the neural network classified correctly
        """
        def get_largest_output(output_list):
            index, largest = -1  # placeholders for champions
            for n in range(len(output_list)):
                if output_list[n][0] > largest:
                    index = n
                    largest = output_list[n][0]
            return index
        correct_counter = 0
        for i, o in self.test_inputs_outputs:
            actual_list = net.process_input(i)[-1]
            actual_index = get_largest_output(actual_list)
            expected_index = get_largest_output(o)
            if actual_index == expected_index:
                correct_counter += 1
        return correct_counter


if __name__ == "__main__":
    size = [28*28, 26*26, 7*7, 10]
    rate = .3
    name = "MNIST Digits"
    trainer = NetworkTrainer(size, learning_rate=rate, num_trials=3, num_epochs=24000, batch_size=5, dataset_name=name)
    file_list, i = trainer.training(num_networks=5)
    print(file_list[i])
    net = Processor.read_net_file(file_list[i])
