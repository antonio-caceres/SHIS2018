import os
import numpy as np


def write_weights(net, name, num_trials, num_epochs, batch_size, num_correct_list):
    with open(get_complete_title(name), 'w') as file:
        file.write("Dataset: " + name + "\n\n")
        file.write("Number of Epochs: " + str(num_epochs) + "\n")
        file.write("Batch Size: " + str(batch_size) + "\n")
        file.write("Learning Rate: " + str(net.learning_rate) + "\n\n")
        for i in range(num_trials):
            file.write("Trial " + str(i) + ": " + str(num_correct_list[i]) + " Correct\n")
        file.write("\n")
        file.write("Weight Matrices\n")
        for i in range(len(net.weight_matrices)):
            file.write("-Weight Matrix " + str(i) + "\n")
            for row in net.weight_matrices[i]:
                for element in row:
                    file.write(str(element) + " ")
                file.write("\n")
            file.write("\n")
        file.write("\n\n")
        file.write("Bias Matrices\n")
        for i in range(len(net.bias_matrices)):
            file.write("-Bias Matrix " + str(i) + "\n")
            for col in net.bias_matrices[i]:
                file.write(str(col[0]) + " ")
            file.write("\n\n")


def get_complete_title(name):
    base_title = name + " Trial "
    counter = 0
    unique = False
    while not unique:
        title = base_title + str(counter)
        unique = True
        for item in os.listdir(os.getcwd() + "/weight_database"):
            if item == title + ".txt":
                unique = False
        counter += 1
    complete_title = "weight_database/" + title + ".txt"
    return complete_title


def read_weight_file(name, net):
    file_name = "weight_database/" + name
    new_weights = []
    new_biases = []
    with open(file_name, 'r') as file:
        for i in range(12):
            file.readline()
        for i in range(len(net.weight_matrices)):
            weight_matrix = []
            for j in range(len(net.weight_matrices[i])):
                line_data = file.readline().split()
                weight_row = []
                for string in line_data:
                    weight_row.append(float(string))
                weight_matrix.append(weight_row)
            new_weights.append(np.array(weight_matrix))
            file.readline()
            file.readline()
        for i in range(3):
            file.readline()
        for i in range(len(net.bias_matrices)):
            bias_matrix = []
            line_data = file.readline().split()
            for string in line_data:
                bias_matrix.append([float(string)])
            new_biases.append(np.array(bias_matrix))
            file.readline()
            file.readline()
    return new_weights, new_biases
