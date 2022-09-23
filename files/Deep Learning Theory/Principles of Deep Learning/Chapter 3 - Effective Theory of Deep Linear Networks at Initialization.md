# Deep Linear Networks
By considering networks with many layers and no activation function we can introduce the machinery that will be used to analyse more general networks later. In particular this chapter shows how layer-to-layer recursions determine the statistics (M-point (connected) correlators) of neural networks at initialisation, and solves the recursion exactly for selected correlators. These correlators are measurements of NN behaviour and ways of controlling these behaviors are discussed.

In this chapter we consider NNs with linear transformations at each layer with no biases:

![[Pasted image 20220616155602.png]]

These layers are initialised independently according to a normal distribution with mean 0:
![[Pasted image 20220616163521.png]]

Deep linear networks represent a smaller set of functions than generic linear transformations: consider a 2 layer neural network with inputs $n_0$, outputs $n_2$ and a hidden layer with one neuron. This bottleneck means the network can represent only a subset of the transformations given by all $n_2 \times n_0$ matrices.

Similarly, the statistics of a deep network differ from the statistics of a one-layer network: each layer has gaussian $W_{ij}^{(l)}$, but the product $\mathcal{W}_{ij}^{(l)}$ is in general non-gaussian.

In this chapter we want to determine: 

![[Pasted image 20220616160524.png]]

Which (like any distribution) is determined by its M-point correlators.

It is trivial to show that $\mathbb{E}[z^{(l)}] = 0$ by taking the expectation of (3.2). Similarly its possible to show that the odd M-point correlators is also $0$.

## Criticality

Recursion for the two point correlator:

![[Pasted image 20220616161149.png]]

Writing the inner product of $\mathbf{x}_{\alpha_1}$ and $\mathbf{x}_{\alpha_2}$ as:

![[Pasted image 20220616161433.png]]

We get:

![[Pasted image 20220616161453.png]]

Next to evaluate the recursion for an arbitrary layer:

![[Pasted image 20220616161745.png]]

Notice that for any layer the two-point correlator vanishes unless the neural indices $i_1, i_2$ are the same and is this proportional to the kronecker delta $\delta_{{i_1}{i_2}}$. 

By considering the last sentence and looking at this for a while you should be able to see that:

![[Pasted image 20220616162809.png]]
and that:

![[Pasted image 20220616162845.png]]

So the quantity $G^{(l)}_{{\alpha_1}{\alpha_2}}$ can be thought of as the average inner product of activations at a given layer, averaged over neurons. This depends on the sample indices $\alpha_1, \alpha_2$ only so $G^{(l)}_{{\alpha_1}{\alpha_2}} = G^{(l)}({x_{\alpha_1},x_{\alpha_2}})$ can be interpreted as the covariance of the two inputs after passing through layer $l$. 

Now it is easy to see that $G^{(l+1)}_{{\alpha_1}{\alpha_2}} = C_WG^{(l)}_{{\alpha_1}{\alpha_2}}$ and that $G^{(l+1)}_{{\alpha_1}{\alpha_2}} = C_W^lG^{(0)}_{{\alpha_1}{\alpha_2}}$ 

Note: $n_l$, the width of the network at each layer, in the initialisation of the layers has dropped out: indicating that this is the proper way of scaling the variance.

### Criticality: Physics
Now we can see that if $C_W < 1$ the covariance will vanish to $0$ and if $C_W > 1$ the covariance will blow up to $\infty$. The authors refer to any fixed point approached exponentially quickly as a **trivial fixed point**. Such behavior would make it difficult for the NN to approximate the desired function.

If instead $C_W = 1$ we have that the variance is preserved and the covariance (since it is not tending exponentially quickly towards anything) tends towards a **non-trivial fixed point**. A setting of the initialisation hyperparameters that avoids blow up or vanishing is called a **critical initialisation hyperparameters**. 

### Fluctuations
For zero mean gaussians the covariance completely determines the distribution, so if the distribution $p(z^{(l)}|\mathcal{D})$ were gaussian the critical tuning of $C_W=1$ ensures all observables are well behaved. If this distribution isn't Gaussian then the behavior of observables that depend on higher-point connected correlators may not be well behaved with the tuning that makes the covariance well behaved.

Now we consider the recursion for the four-point correlator and for simplicity only consider correlators that depend on one input:

![[Pasted image 20220617093145.png]]

Recursion for the first layer:

![[Pasted image 20220617093402.png]]

Going from the second line to the first we take the wick contraction which yields 3 pairings of the $W_{ij}$'s (double factorial $(2*2 - 1)!! = 3$) and used (3.4) to evaluate the weight variance. Then evaluate the sums over the $j$'s and substitute the the definition of the inner product from above:

![[Pasted image 20220617094319.png]]

This is precisely what we'd expect for the fourpoint correlator if the preactivation distribution were Gaussian. For deeper layers this won't be the case:

![[Pasted image 20220617094702.png]]

Where we use the fact that the $(l+1)$th layer weights are independent from the $(l)$th layer activations.

Similarly in the covariance case we notice that *any* layer is proportional to the factor $(\delta_{{i_1}{i_2}}\delta_{{i_3}{i_4}} + \delta_{{i_1}{i_3}}\delta_{{i_2}{i_4}} + \delta_{{i_1}{i_4}}\delta_{{i_2}{i_4}})$ we can write:

![[Pasted image 20220617100018.png]]

and put all the layer dependence into $G_4^{(l)}$ so for the first layer we get:

![[Pasted image 20220617100142.png]]

and the final term in the above summation becomes:

![[Pasted image 20220617102257.png]]

(First kronecker delta sum is $n_l^2$ second is $n_l$ and third is $n_l$) so we can rewrite the recursion:

![[Pasted image 20220617103150.png]]

and then the recursion can be solved using the initial condition from above:

![[Pasted image 20220617103259.png]]

#### Resulting physics
The point of doing this is to analyse the behavior of the four point correlator. For instance, taking the limit as $n_l \rightarrow \infty$ notice that the full four point correlator becomes:

![[Pasted image 20220617104427.png]]

I.e in the infinite width limit the preactivation distributions are gaussian and the four point correlator is determined by the two point correlator.

If we instead have equal hidden layer widths for all layers we get for the deviation of the four point correlator from that in the infinite width limit:

![[Pasted image 20220617105252.png]]

Where we expand in $1/n$ and keep the leading correction to the infinite width limit. At criticality where $G^{(l)}_2$ is constant we have that the correction scales proportionally with depth and inversely with width, and is thus proportional to the depth-to-width ratio of the network, something the authors refer to as **emergent scale**.

They give some examples of interpreting this correction, see the text book for more details.

The take away point is that networks show these finite-width effects where behavior depends on the depth-to-width ratio.


Summary:

