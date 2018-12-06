import os
import time
import random
import pickle
import imageio
import numpy as np
from utils import mnist_reader
import FeedforwardNeuralNet
import ProgressBar


# Data Processing
def write_mnist_data(dataset_name):
    """
    Writes pickle files that contain the mnist dataset to the data folder
    :param dataset_name: name of the folder within the 'unprocessed' folder to get the files from
    """
    def process_mnist_input(input_list):
        """
        Process a list of inputs, where one input is a list of integers corresponding to the pixels of the images, by
        dividing each input by 256 to limit the inputs to values between 0 and 1.
        :param input_list: a list of lists of integers, where each list is one input.
        :return: a list of numpy column arrays with length 784, with floats between 0 and 1.
        """
        # Progress Bar
        start_time = time.time()
        print("Processing Input")
        ProgressBar.draw_bar(0, 30, 0)
        inputs_completed = 0

        processed_inputs = []
        for old_input in input_list:
            new_input = []
            for integer in old_input:
                new_input.append([integer / 256.0])
            processed_inputs.append(np.array(new_input))

            inputs_completed += 1.0
            ProgressBar.draw_bar(inputs_completed / len(input_list), 30, time.time() - start_time)
        print("Input processing took " + ProgressBar.time_to_string(time.time() - start_time) + ".")
        return processed_inputs

    def process_mnist_output(output_list):
        """
        Process a list of outputs, where one output is an integer
        corresponding to the group that the input should be classified under.
        :param output_list: a list of integers, where each integer is one output.
        :return: a list of numpy arrays with length 10, with 0 at all indices except the integer from data_list
        """
        start_time = time.time()
        print("Processing Output")
        ProgressBar.draw_bar(0, 30, 0)
        outputs_completed = 0

        processed_outputs = []
        for old_output in output_list:
            new_output = []
            for i in range(10):
                if i == old_output:
                    new_output.append([1])
                else:
                    new_output.append([0])
            processed_outputs.append(np.array(new_output))

            outputs_completed += 1.0
            ProgressBar.draw_bar(outputs_completed / len(output_list), 30, time.time() - start_time)
        print("Output processing took " + ProgressBar.time_to_string(time.time() - start_time) + ".")
        return processed_outputs

    data = 'unprocessed/' + dataset_name
    x_train, y_train = mnist_reader.load_mnist(data, kind='train')
    x_test, y_test = mnist_reader.load_mnist(data, kind='t10k')

    train_io = list(zip(process_mnist_input(x_train), process_mnist_output(y_train)))
    test_io = list(zip(process_mnist_input(x_test), process_mnist_output(y_test)))

    training_title = 'data/' + dataset_name + '_training' + '.pickle'
    testing_title = 'data/' + dataset_name + '_testing' + '.pickle'

    pickle.dump(train_io, open(training_title, 'wb'))
    pickle.dump(test_io, open(testing_title, 'wb'))


def read_mnist_data(dataset_name):
    training_title = 'data/' + dataset_name + '_training' + '.pickle'
    testing_title = 'data/' + dataset_name + '_testing' + '.pickle'

    train_io = pickle.load(open(training_title, 'rb'))
    test_io = pickle.load(open(testing_title, 'rb'))

    return train_io, test_io


def augment_mnist_digits_data(num_augments, width, height):
    """
    Takes the mnist digits dataset and augments it, multiplying its size by num_augments.
    Writes the new dataset to a pickle file. Requires the mnist digits data to already be written.
    :param num_augments: the number of new inputs to create from one base input in the mnist dataset.
    :param width: the width of the image in the input
    :param height: the height of the image in the input
    """
    start_time = time.time()
    print("Augmenting Digit Training Data")
    ProgressBar.draw_bar(0, 30, 0)

    def augment_inputs(io_list):
        """
        Takes a zipped list of inputs and their corresponding outputs
        :param io_list: list of tuples, each with one input and its corresponding output
        :return: a zipped list of augmented inputs and their corresponding outputs
        """
        inputs_completed = 0
        new_inputs = []
        new_outputs = []
        for i, o in io_list:
            # doing the original input and output
            new_inputs.append(i)
            new_outputs.append(o)
            inputs_completed += 1.0
            ProgressBar.draw_bar(inputs_completed / len(io_list * num_augments), 30, time.time() - start_time)
            for n in range(num_augments-1):  # TODO bugfix data augmentation
                x_range, y_range = calculate_shift_ranges(i, width, height)
                rnd_x = random.randint(x_range[0], x_range[1])
                rnd_y = random.randint(y_range[0], y_range[1])
                shift_delta = (rnd_x, rnd_y)
                new_input = shift_all_values(i, width, height, shift_delta)
                new_inputs.append(new_input)
                new_outputs.append(o)
                inputs_completed += 1.0
                ProgressBar.draw_bar(inputs_completed / len(io_list*num_augments), 30, time.time() - start_time)
        return list(zip(new_inputs, new_outputs))
    old_training, old_testing = read_mnist_data('mnist_digits')

    augmented_train_io = augment_inputs(old_training)
    augmented_test_io = augment_inputs(old_testing)
    print("Data augmenting took " + ProgressBar.time_to_string(time.time() - start_time) + ".")

    training_title = 'data/' + 'augmented_digits' + '_training' + '.pickle'
    testing_title = 'data/' + 'augmented_digits' + '_testing' + '.pickle'

    pickle.dump(augmented_train_io, open(training_title, 'wb'))
    pickle.dump(augmented_test_io, open(testing_title, 'wb'))


# This method is probably never going to be used but I'm going to leave it here.
def user_drawings_to_inputs(path, base_title):
    """
    From a folder of user drawings, convert them into a format that can be processed by a neural network.
    :param path: the folder to get the user drawings from
    :param base_title: file name without the added number or the file extension (ignores files without this name)
    :return: list of tuples with an input and its corresponding file name
    """
    input_list = []
    file_names = []
    for file_name in os.listdir(os.getcwd() + "/" + path):
        if file_name[:len(base_title)] == base_title:
            input_list.append(imageio.imread(path + "/" + file_name, as_gray=True))
            file_names.append(file_name)
    processed_input_list = []
    for old_input in input_list:
        new_input = []
        for row in old_input:
            for element in row:
                new_input.append([(255 - element) / 256])
        processed_input_list.append(np.array(new_input))
    return list(zip(processed_input_list, file_names))


def draw_input_to_ascii(input_list, width, height):
    """
    Prints an input to the network in ASCII characters.
    :param input_list: a list of floats between 0 and 1, representing an input to the neural network.
    :param width: the width of the image to be drawn
    :param height: the height of the image to be drawn
    """
    i = 0
    for r in range(height):
        for c in range(width):
            char = '.'
            if input_list[r * width + c][0] != 0:
                char = '#'
            print(char, end='')
            i += 1
        print("")
    print("")


# Handling Neural Network Information Files
def write_meta_net_file(net_size, learning_rate, dataset_name, num_trials, num_epochs, batch_size, num_correct_lists):
    """
    for a single training run of neural networks, records the metadata for each net.
    :param net_size: the size of neural network objects during the run
    :param learning_rate: the learning rate of nets during the run
    :param dataset_name: the name of the dataset the networks were trained on
    :param num_trials: number of training trials
    :param num_epochs: number of training epochs
    :param batch_size: size of training batches
    :param num_correct_lists: list of lists; the number of correct testing images in each trial for each network
    :return: the index of the neural network that got the most images correct on the final trial
    """
    file_name = get_complete_title(dataset_name + " Training", "weight_database", ".txt")
    largest, index = -1, -1  # placeholders for championship algorithm
    with open(file_name, 'w') as file:
        file.write("Dataset: " + dataset_name + "\n\n")
        file.write("Network Size: ")
        for num in net_size:
            file.write(str(num) + " ")
        file.write("\nLearning Rate: " + str(learning_rate) + "\n" +
                   "Number of Epochs: " + str(num_epochs) + "\n" +
                   "Batch Size: " + str(batch_size) + "\n\n")
        for i in range(len(num_correct_lists)):
            file.write("Network " + str(i) + " Trials\n")
            for j in range(num_trials):
                file.write("Trial " + str(i) + ": " + str(num_correct_lists[i][j]) + " Correct\n")
            file.write("\n")

            if num_correct_lists[i][-1] > largest:
                largest = num_correct_lists[i][-1]
                index = i
    return index


def write_net_file(net, dataset_name, folder_name):
    """
    Create a file containing all the information about a neural net after training.
    :param net: the trained neural network
    :param dataset_name: the name of the dataset the neural net was trained on
    :param folder_name: the path of the folder to put the net file under.
    :return: the file name that the net file was written under.
    """
    file_name = get_complete_title(dataset_name + ' Net', folder_name, '.pickle')
    information = (net.weight_matrices, net.bias_matrices)
    pickle.dump(information, file_name)
    return file_name


def read_net_file(net_size, net_rate, file_name):
    """
    Creates a NeuralNet object with preloaded weights and biases from a file.
    :param net_size: the size of the neural network to be created
    :param net_rate: the rate of the neural network to be created
    :param file_name: the path and file name to be used to preload the weights and biases
    :return: a neural net with weights and biases from the file.
    """
    net = FeedforwardNeuralNet.NeuralNet(net_size, net_rate)
    new_weights, new_biases = pickle.load(file_name)
    net.weight_matrices = new_weights
    net.bias_matrices = new_biases
    return net


# Miscellaneous
def get_complete_title(base, path, file_type):
    """
    Given a folder and a file name, add numbers to ensure the new file will not overwrite any existing files.
    :param base: file name without the file extension
    :param path: path to the folder to store the file in question, excluding the first and last '/'
    :param file_type: file extension given to the file you are trying to name
    :return: string with a path and file name that doesn't match any existing files in that path
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
    complete_title = path + "/" + title + file_type
    return complete_title


# Data Augmentation
def bound_box_of_values(input_list, width, height):
    """
    Calculates the box of values surrounding the image in question.
    :param input_list: a one-dimensional numpy column array containing values for a handwritten digit.
    :param width: the width of the image
    :param height: the height of the image
    :return: ((min_x, min_y), (max_x, max_y))
    """
    minimum, maximum = [width, height], [-1, -1]
    for r in range(height):
        for c in range(width):
            v = input_list[r * width + c][0]
            if v != 0:
                if c < minimum[0]:
                    minimum[0] = c
                if r < minimum[1]:
                    minimum[1] = r
                if c > maximum[0]:
                    maximum[0] = c
                if r > maximum[1]:
                    maximum[1] = r
    return (minimum[0], minimum[1]), (maximum[0], maximum[1])


def calculate_shift_ranges(input_list, width, height):
    """
    Calculates the maximum range by which to shift the image to reach the boundary
    :param input_list: a one-dimensional numpy column array containing values for a handwritten digit.
    :param width: the width of the image
    :param height: the height of the image
    :return: ((max_left, max_right),(max_up, max_down))
    """
    bounds = bound_box_of_values(input_list, width, height)
    x_range = (-bounds[0][0], width - bounds[1][0] - 1)
    y_range = (-bounds[0][1], height - bounds[1][1] - 1)
    return x_range, y_range


def range_of_shiftable_positions(input_list, width, height):
    """
    :param input_list: a one-dimensional numpy column array containing values for a handwritten digit.
    :param width: the width of the image
    :param height: the height of the image
    :return: a sequence of shift deltas to get every possible position of the input list within the bounds of the image.
        Note that the sequence assumes that the image is moving.
    """
    bounds = bound_box_of_values(input_list, width, height)
    result = []
    dx, dy = bounds[1][0] - bounds[0][0], bounds[1][1] - bounds[0][1]
    result.append((-bounds[0][0], -bounds[0][1]))
    for r in range(height - dy):
        if dx > 0:
            for c in range(width - dx - 1):
                result.append((+1, 0))
        if r < height - dy - 1:
            result.append((-(width - dx - 1), +1))
    return result


def shift_all_values(input_values, width, height, xy_delta):
    """
    return a new list of inputs that is the original inputs shifted by the delta.
    :param input_values: a one-dimensional numpy column array containing values for a handwritten digit.
    :param xy_delta: a shift delta that produces a new position for the image in the input_values
    :param width: the width of the image
    :param height: the height of the image
    :return: a list of new inputs that contain a shifted image.
    """
    # create a 2D array version of the 1D array
    two_dim_copy = []
    new_input_list = np.array([[0]] * width * height)
    for r in range(height):
        two_dim_copy.append([])
        for c in range(width):
            two_dim_copy[r].append(input_values[r * width + c][0])

    for r in range(len(two_dim_copy)):
        shift_list(two_dim_copy[r], xy_delta[0], 0)
    shift_list(two_dim_copy, xy_delta[1], [0] * width)

    # copy it back now
    for r in range(height):
        for c in range(width):
            new_input_list[r * width + c][0] = two_dim_copy[r][c]
    return new_input_list


def shift_list(values, delta, fill_extra_with=None):
    """
    Shift a list of inputs in-place a certain change delta.
    :param values: the inputs to shift.
    :param delta: the change with which to shift the inputs.
    :param fill_extra_with: the value to fill the empty spaces with
    :return: None
    """
    import copy
    if delta < 0:  # go backwards, losing values at the front
        for i in range(0, len(values) + delta):
            values[i] = values[i - delta]
        if fill_extra_with is not None:
            for i in range(len(values) + delta, len(values)):
                values[i] = copy.copy(fill_extra_with)
    if delta > 0:
        for i in range(len(values) - 1, -1, -1):
            values[i] = values[i - delta]
        if fill_extra_with is not None:
            for i in range(delta - 1, -1, -1):
                values[i] = copy.copy(fill_extra_with)


if __name__ == "__main__":
    # write_mnist_data('mnist_digits')
    # write_mnist_data('mnist_fashion')
    augment_mnist_digits_data(num_augments=5, width=28, height=28)
    augmented_train, augmented_test = read_mnist_data('mnist_digits')
    for i, o in augmented_train[:5]:
        draw_input_to_ascii(i, width=28, height=28)
        print(o)
