import os
import WeightFileWriter as Writer
import FeedforwardNeuralNet

# Current Working Directory Test
print(os.getcwd())

# Get Complete Title Test
for i in range(3):
    title = Writer.get_complete_title("Test")
    with open(title, 'w') as file:
        file.write("test\ntest")

# Weight Writer Test
size = [4, 5, 3]
net = FeedforwardNeuralNet.NeuralNet(size, learning_rate=.15)
Writer.write_weights(net, "Test", 5, 5, 5, [1, 8, 4, 20, 5])
