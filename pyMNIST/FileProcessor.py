import os
import numpy as np
from utils import mnist_reader
# TODO: Documentation


def process_mnist_data(dataset_name):
    """
    documentation to come
    :param dataset_name: string
    :return: a tuple with two zipped lists, the training input/outputs and the testing input/outputs
    """
    def process_mnist_input(input_list):
        """
        Process a list of inputs, where one input is a list of integers corresponding to the pixels of the images, by
        dividing each input by 256 to limit the inputs to values between 0 and 1.
        :param data_list: a list of lists of integers, where each list is one input.
        :return: a list of numpy column arrays with length 784, with floats between 0 and 1.
        """
        processed_inputs = []
        for old_input in input_list:
            new_input = []
            for integer in old_input:
                new_input.append([integer / 256.0])
            processed_inputs.append(np.array(new_input))
        return processed_inputs

    def process_mnist_output(output_list):
        """
        Process a list of outputs, where one output is an integer
        corresponding to the group that the input should be classified under.
        :param data_list: a list of integers, where each integer is one output.
        :return: a list of numpy arrays with length 10, with 0 at all indices except the integer from data_list
        """
        processed_outputs = []
        for old_output in output_list:
            new_output = []
            for i in range(10):
                if i == old_output:
                    new_output.append([1])
                else:
                    new_output.append([0])
            processed_outputs.append(np.array(new_output))
        return processed_outputs

    data = "data/" + dataset_name.lower()
    x_train, y_train = mnist_reader.load_mnist(data, kind='train')
    x_test, y_test = mnist_reader.load_mnist(data, kind='t10k')

    train_io = zip(process_mnist_input(x_train), process_mnist_output(y_train))
    test_io = zip(process_mnist_input(x_test), process_mnist_output(y_test))
    return train_io, test_io
    # TODO: Implement progress bar
    # t_start = 0
    # if PROGRESS_BAR_DISPLAY_SIZE is not None:
    #     t_start = time.time()
    #     print("processing input...")
    #     ProgressBar.draw_bar(0, PROGRESS_BAR_DISPLAY_SIZE, 0)
    #     progress = 0
    # processed_inputs = []
    # for old_input in data_list:
    #     new_input = []
    #     for integer in old_input:
    #         new_input.append([integer / 256.0])
    #     processed_inputs.append(np.array(new_input))
    #     if PROGRESS_BAR_DISPLAY_SIZE is not None:
    #         progress += 1.0
    #         ProgressBar.draw_bar(progress / len(data_list), PROGRESS_BAR_DISPLAY_SIZE, time.time() - t_start)
    # if PROGRESS_BAR_DISPLAY_SIZE is not None:
    #     sys.stdout.write("processing input took " + ProgressBar.timing(time.time() - t_start, 8) + "\n")
    # return processed_inputs

    # t_start = 0
    # if PROGRESS_BAR_DISPLAY_SIZE is not None:
    #     t_start = time.time()
    #     print("processing output...")
    #     ProgressBar.draw_bar(0, PROGRESS_BAR_DISPLAY_SIZE, 0)
    #     progress = 0
    # processed_outputs = []
    # for old_output in data_list:
    #     new_output = []
    #     for i in range(10):
    #         if i == old_output:
    #             new_output.append([1])
    #         else:
    #             new_output.append([0])
    #     processed_outputs.append(np.array(new_output))
    #     if PROGRESS_BAR_DISPLAY_SIZE is not None:
    #         progress += 1.0
    #         ProgressBar.draw_bar(progress / len(data_list), PROGRESS_BAR_DISPLAY_SIZE, time.time() - t_start)
    # if PROGRESS_BAR_DISPLAY_SIZE is not None:
    #     sys.stdout.write("processing output took " + ProgressBar.timing(time.time() - t_start, 8) + "\n")
    # return processed_outputs


def write_weight_file(net, dataset_name, num_trials, num_epochs, batch_size, num_correct_list):
    with open(get_complete_title(dataset_name + " Trial", "weight_database", ".txt"), 'w') as file:
        file.write("Dataset: " + dataset_name + "\n\n" +
                   "Number of Epochs: " + str(num_epochs) + "\n" +
                   "Batch Size: " + str(batch_size) + "\n" +
                   "Learning Rate: " + str(net.learning_rate) + "\n\n")
        for i in range(num_trials):
            file.write("Trial " + str(i) + ": " + str(num_correct_list[i]) + " Correct\n")

        file.write("\nWeight Matrices\n")
        for i in range(len(net.weight_matrices)):
            file.write("-Weight Matrix " + str(i) + "\n")
            for row in net.weight_matrices[i]:
                for element in row:
                    file.write(str(element) + " ")
                file.write("\n")
            file.write("\n")

        file.write("\n\nBias Matrices\n")
        for i in range(len(net.bias_matrices)):
            file.write("-Bias Matrix " + str(i) + "\n")
            for col in net.bias_matrices[i]:
                file.write(str(col[0]) + " ")
            file.write("\n\n")


def read_weight_file(name, net):
    file_name = "weight_database/" + name
    new_weights = []
    new_biases = []
    with open(file_name, 'r') as file:
        file.readlines(12)
        for i in range(len(net.weight_matrices)):
            weight_matrix = []
            for j in range(len(net.weight_matrices[i])):
                line_data = file.readline().split()
                weight_row = []
                for string in line_data:
                    weight_row.append(float(string))
                weight_matrix.append(weight_row)
            new_weights.append(np.array(weight_matrix))
            file.readlines(2)
        file.readlines(3)
        for i in range(len(net.bias_matrices)):
            bias_matrix = []
            line_data = file.readline().split()
            for string in line_data:
                bias_matrix.append([float(string)])
            new_biases.append(np.array(bias_matrix))
            file.readlines(2)
    return new_weights, new_biases


def get_files(path):
    pass


def get_complete_title(base, path, file_type):
    """
    Given a folder and a file name, add numbers to ensure the new file will not overwrite any existing files.
    :param base: The file name without the file extension.
    :param path: The path to the folder to store the file in question, excluding the first and last '/'.
    :param file_type: The file extension given to the file you are trying to name.
    :return: A string with a path and file name that doesn't match any existing files in that path.
    """
    title = base + " "
    counter = 0
    unique = False
    while not unique:
        title = base + " " + str(counter)
        unique = True
        for item in os.listdir(os.getcwd() + "/" + path):
            if item == title + file_type:
                unique = False
        counter += 1
    complete_title = path + "/" + title + ".txt"
    return complete_title
