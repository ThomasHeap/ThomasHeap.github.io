## Neural Networks

### Function approximation and activation functions
The authors introduce the basics of function approximation (what NNs do) and then cover some of the more common activation functions (perceptron, linear, RELU etc...). The big thing to take away from these sections is that neural networks aim to approximate general functions through learning weights in paramterised models, can be induced to learn particular functions by particular structures on the parameters, and that some activations functions (like RELU) are scale free (i.e $\sigma(kx) = k\sigma(x)$).

![[Pasted image 20220608162619.png]]


### Ensembles
By defining the initialisation regime of a neural network in terms of probability distributions we constrain the resulting ensemble of networks to have particular properties depending on the probability distributions chosen. In particular Gaussian initialistion of the weights and biases are easy to work with in practice and in theory.

![[Pasted image 20220608163251.png]]

By theoretically analysing the resulting outputs from NN's initialised with weights and biases sampled from these distributions, they can give recommendations for the setting of the hyperparameter variances $C_b^{(l)}$ and $C_W^{(l)}$.

These randomly sampled W&Bs induce a probability distribution over the outputs $z^{(L)}$ of the NN. 

![[Pasted image 20220608164122.png]]

The function $p(z^{(L)}|\theta, \mathcal{D})$ is actually deterministic, since it is defined by the NN which we know how to evaluate if we know the weights. This results in putting down a dirac delta function on the outputs of each layer:

![[Pasted image 20220608164417.png]]

![[Pasted image 20220608164433.png]]

![[Pasted image 20220608164450.png]]

