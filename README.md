# Independent-Study
## Antonio Caceres's Senior Honors Independent Study
  This repository is dedicated to my Senior Honors Independent Study, taking place in the fall semester of the 2018-2019 school year. The Independent Study course gives seniors the opportunity to do an independent research project for course credit.
  In my Independent Study this semester, I will be studying Artificial Neural Networks (ANNs), a type of artificial intelligence and machine learning process. I chose to study ANNs because they are an increasingly popular topic in the field of computer science, and they combine my enthusiasm for math and computer science.

**What is an artificial neural network?**
  In computer science, artificial neural networks are layered systems of nodes designed to imitate the processes of biological brains. There are three types of layers in a neural net: the input layer, the hidden layers, and the output layer. The nodes in the input layer receive inputs given to the network and send those inputs to the first hidden layer. Each node in that hidden layer applies a mathematical function to the value, and sends it to nodes in the next hidden layers, and so on, until reaching the output layer, which simply represents the outputs of the network.

  The most important concept of neural nets is that every connection between nodes has some weight attached to it. The weight determines the impact that the node sending the signal has on the node receiving the signal. The connection either increases, does little to, or decreases the output of the receiving node, depending on whether the weight is positive, close to zero, or negative, respectively.
   The neural network learns by changing these weights. With a certain set of weights, the network is capable of abstraction, explained by Ray Kurzweil in [his Ted Talk](https://youtu.be/PVXQUItNEDQ?t=234). While this abstraction is not *actually* how the neural net makes its decisions, it's a good way to conceptualize what the net is doing.
   
   Initially, a neural net is given a random set of weights. In order to find a set of weights that gives the outputs we are looking for, there are three types of training.
   During supervised training, the neural network is given the correct output, and compares its output with the correct one. If they don’t match, the network adjusts its weights by a small amount to move closer to the correct output and repeats the process.
   During unsupervised training, there's no 'correct output', and the network learns without any specific goal in mind. One way to implement this is by making the connections between nodes more extreme. Essentially, if the connection is positive, it should be made more positive, and if it is negative, it should be made more negative. This reinforces what the network 'already knows', which helps sort data when programmers don't know what characteristic to sort by.
   During reinforcement training, the network has some quantifiable goal to measure its performance, like score in a video game. There is not necessarily a correct output, but the network has something to work towards. In this training, the network compares the output it chose to the reward or punishment it received to learn what outputs are good or bad in certain situations.
   
### Goals for this Independent Study
Learning Goals for the Independent Study:
* Understand the processes and math that make an artificial neural network function.
* Understand the different types of neural networks and their applications.
* Investigate when a human is more effective than an artificial neural network, and vice versa.
* Build my own simple neural network to learn a task like recognizing patterns or playing a game.
* Teach other computer science students about neural nets and make the field accessible to newcomers.

Guiding Questions:
* How do neural networks work, and what determines the functions applied in the nodes?
* What are the different types of neural networks and where do they work best?
  * What is the difference between feedforward and feedback/recurrent neural networks?
* What are some potential applications of neural networks?
* What kinds of mental labor are humans better at than artificial neural networks?

Major Assignments:
* Create a small presentation to explain neural nets in layman's terms.
* Train a neural net to tell the difference between two or three types of objects.
* Outline a ‘learning path’ for other computer scientists to more easily learn about neural nets.
* Create an neural net that can ‘imagine’ and ‘write’ numbers or letters.
