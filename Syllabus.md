# SHIS Syllabus
### Major Assigments
**Python MNIST Digit Recognition**
* Process the digit data set to randomize the location of the actual handwriting within the 28x28 input, ensuring the net can recognize handwriting that isn't in the center of the input.
  * Add input read/write to files to the FileProcessor.
  * Process the MNIST dataset into a different format to read it from there.
  * Change the MNIST dataset, adding different translations of the images.
* Train a multilayer feedforward network with the school computers, storing the sets of weights after training.
* Add realtime neural net processing and 'brain confidence' to the Pygame drawing app for the demonstration.
* Test an 'imagination function' of the *trained* neural net using the generalized inverse by:
  * Applying a function to the 'backwards outputs' of each layer to restrict the values to the intended range.
  * Restricting the values by just setting all negative values to 0 and all values greater than 1 to 1.

**Small Presentation**
* Create a small, five-minute presentation to explain neural nets to beginners.
* Create a feedback form for people that I give the small presentation to.
* Give the small presentation to colleagues and revise it.

**Learning Path**
* Design a 'learning path' to introduce computer science students to neural nets.
* Find new sources for beginners (less math-focused) or for niche cases (like Monte Carlo).

**Final Presentation**
* Begin to put together the final presentation.
* Begin practicing the presentation.

**Bambino Game Reinforcement**
* Research Monte Carlo reinforcement learning algorithms.
* Implement a Monte Carlo algorithm for the network to learn Bambino.
* Adjust the Bambino code to include neural net training processes.

**Bandit Feedback Project**
* Reach out to Dr. Thorsten Joachims about his project comparing bandit feedback from the proposal of the project.

### Research
Neural Networks
* Introduction to Neural Networks with Java – The Future of Neural Networks
* [Deep Learning with Logged Bandit Feedback](http://www.cs.cornell.edu/people/tj/publications/joachims_etal_18a.pdf)
* [Understanding the Difficulty of Training Deep Feedforward Neural Networks](http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf?hc_location=ufi)
* Neural Networks and Deep Learning – Improving the Way Neural Networks Learn
* Intelligence Emerging – Evolutionary Algorithms
* Intelligence Emerging – Artificial Neural Networks
* Intelligence Emerging – Knowledge Representation in Neural Networks
* Intelligence Emerging – Evolving Artificial Neural Networks

Reinforcement Learning
* Reinforcement Learning: An Introduction – Introduction
* Reinforcement Learning: An Introduction – Multi-armed Bandits
  * Supporting Resource: [Bandit Problems](https://oneraynyday.github.io/ml/2018/05/03/Reinforcement-Learning-Bandit/)
* Reinforcement Learning: An Introduction – Finite Markov Decision Processes
  * Supporting Resource: [Markov Decision Processes](https://oneraynyday.github.io/ml/2018/05/06/Reinforcement-Learning-MDPs/)
* Reinforcement Learning: An Introduction – Monte Carlo Methods
  * Supporting Resource: [Monte Carlo](https://oneraynyday.github.io/ml/2018/05/24/Reinforcement-Learning-Monte-Carlo/)
