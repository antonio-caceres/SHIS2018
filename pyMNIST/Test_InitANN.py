import FeedforwardNeuralNet as NetClass

net = NetClass.NeuralNet([4, 5, 3])

if __name__ == "__main__":
    for i in range(len(net.weight_matrices)):
        print(net.weight_matrices[i], "\n\n")
        print(net.bias_matrices[i], "\n\n")
        print(net.weight_matrices[i][0], "\n\n", net.weight_matrices[i][0][0])
