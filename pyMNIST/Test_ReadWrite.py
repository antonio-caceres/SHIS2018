import os
import WeightFileReaderWriter as Writer
import FeedforwardNeuralNet as NetClass


def write_test_files():
    for i in range(3):
        title = Writer.get_complete_title("Test")
        with open(title, 'w') as file:
            file.write("test\ntest")


def write_test_weight_file():
    size = [4, 5, 3]
    net = NetClass.NeuralNet(size, learning_rate=.15)
    Writer.write_weights(net, "Weight Test", 5, 5, 5, [1, 8, 4, 20, 5])


if __name__ == "__main__":
    print(os.getcwd())
    write_test_files()
    write_test_weight_file()
