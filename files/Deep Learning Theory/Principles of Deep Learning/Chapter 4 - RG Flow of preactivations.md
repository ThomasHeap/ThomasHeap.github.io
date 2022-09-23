## Last Chapter

* Computed statistics of preactivations for a deep neural network without activation functions
* Using Wick contractions and the recursive structure of the network we were able to understand the effect of the initialization scheme, depth, width on preactivation correlators
* This highlighted the importance of critical initialization hyperparamters and a sufficiently small depth-to-width ratio in order for the networks outputs to be "well behaved"

## In This Chapter
* Overall goal is to discover how a particular neural network learns from a dataset. To that end they start by investigating how *ensembles* of neural networks behave at initialisation, as a function of the data.
* By doing this they hope to isolate the *typical* behavior of a neural network, and how any particular neural network might fluctuate from this typicality.
* In the infinite width limit NNs become GPs (with a fixed kernel) and show reduced capacity for representation learning. To investigate what happens in the large but not infinite width regime, they propose to use a $1/n$ expansion.
* They proceed recursively, going layer by layer.

## First Layer
![[Pasted image 20220718170151.png]]

Next step: Two derivations of the distributions of the first-layer preactivations at initialisation.

### Via Wick Contractions
Starting with one-point correlator:

![[Pasted image 20220718170610.png]]

Since bias and weights have 0 mean. In fact all odd-point correlators of $p(z^{(1)}|\mathcal{D})$ vanish because there are always an odd number of biases or weights left unpaired under Wick contractions.

For two-point correlator:

![[Pasted image 20220718170839.png]]

This is a function of the two samples. $G^{(1)}_{{\alpha_1}{\alpha_2}} = G^{(1)}(x_{\alpha_{1}}, x_{\alpha_{2}})$ and represents the two-point correlations of preactivations in the first layer between different samples.

Higher-point correlators can be found similarly, here for the four-point correlator:

![[Pasted image 20220718171348.png]]

The end result is the same as Wick-contracting $z^{(1)}$'s with the variance given by (4.7). recalling chapter 1, we remember that can be summed up by saying the connected four-point correlator vanishes (since the $z^{(1)}$'s are gaussian). Similarly all higher-point correlators also vanish. So all correlators can be generated from a Gaussian with zero mean and the variance (4.7).

So to write down the first-layer action we need the inverse of this variance:

![[Pasted image 20220718172355.png]]

![[Pasted image 20220718172851.png]]

## Via Hubbard-Stratonovich 
Instead of computing correlators and backing out the distribution that generates them, instead we can work directly with the distribution. Using the formal expression for the preactivation distribution worked out in the last chapter:

![[Pasted image 20220718173156.png]]

We could try to eliminate some of the integrals over the model parameters with respect to the constraints from the delta-functions, but it can become confusing due to the different numbers of model-parameter integrals and delta-function constraints.

So to simplify things we can use the **Hubbard-Stratonovich transformation**, using the following integral representation of the Dirac delta function:

![[Pasted image 20220718174639.png]]

Completing the square for the biases $b$ and weights $W$ gives a quadratic action in model parameters:

![[Pasted image 20220722180449.png]]

Then the weights and biases can be integrated out:

![[Pasted image 20220722180707.png]]

In effect what we have done is swap the delta-function constraints and model parameters for the Hubbard-Statonovich variables $\Lambda_i^\alpha$ which have a quadratic action (the first term above) and a linear interaction with the preactivations (second term).

Note the inverse variance here is the first layer metric (4.8) in the wick contraction derivation (restoring layer superscripts):

![[Pasted image 20220722181120.png]]

Then we can complete the square again, and integrate out the H-S variables to recover the previous result:

![[Pasted image 20220722181359.png]]

#### Quadratic action in action
Now given this action representation for the distribution of the first layer preactivations we can compute some expectations, in particular we can compute the expectation of two actiavtions on the same neuron, and the expectation of four activations either with all on the same neuron or pairs on two different neurons:

![[Pasted image 20220722181810.png]]

The second equality is because the probability distribution factorises for each neuron ($e^{(x+y)} = e^xe^y$). The third equality comes about because the first set of integrals are all trivial, and from renaming the dummy variables $z_{{i_1}:\alpha_1} \rightarrow z_{\alpha_1}$. The final equality uses the notation:

![[Pasted image 20220722182130.png]]

This is a gaussian expectation with variance $g$ and an arbitrary function $F(z_{\alpha_1}, ..., z_{\alpha_m}$) over variables with sample indices only. For this chapter we consider computations complete when they can be reduces to gaussian expectations like these.

Using the shorthand $\sigma_\alpha \equiv \sigma(z_\alpha)$, the computation above can be expressed simply as:
$$
\mathbb{E}\left[\sigma(z_{{z_{i_1};\alpha_1}}^{(1)})\sigma(z_{{z_{i_1};\alpha_2}}^{(1)})\right] = \langle \sigma_{\alpha_1}, \sigma_{\alpha_2} \rangle_{G^{(1)}}
$$
This can quite easily be generalised to correlators of more than two activations:

![[Pasted image 20220722182943.png]]

It's clear that each neuron factorises and gives seperate integrals. In deeper layers the preactivation distributions are nearly-Gaussian and things get a bit more complicated.


## Second Layer: Genesis of Non-Gaussianity
The joint distribution of the first and second layer preactivations is given:

![[Pasted image 20220722184716.png]]

We evaluated the last term in the previous section, for the conditional distribution we have:

![[Pasted image 20220722184839.png]]

We then marginalise over the first layer preactivations:

![[Pasted image 20220722184908.png]]

First we need to figure out how to treat the conditional distribution, then we need to figure out how to integrate out the $z^{(1)}$.

#### Second layer conditional distribution
If we replace the layer indices $l$ $1 \rightarrow 2$ and exchange the network inputs for the first layer preactivations $x_{j;\alpha} \rightarrow \sigma_{j;\alpha}^{(1)}$ we can evaluate this in exactly the same way as we evaluated the first-layer distribution:

![[Pasted image 20220722185406.png]]

Where the second-layer metric $\hat{G}$ is a random variable that depends on $z^{(1)}$:
![[Pasted image 20220722185934.png]]

So the second layer conditional distribution is a Gaussian with a variance which is a random variable. This random variable has a mean, and they measure the fluctuation of the second-layer metric by subtracting this mean from the R.V:

![[Pasted image 20220722190448.png]]

![[Pasted image 20220722190501.png]]

Which by construction has mean zero when averaged over first layer preactivations.

The variance of the fluctuation is given by its two-point correlator, remembering the expression for the gaussian integrals of the two and four activations on the same neurons from above:

![[Pasted image 20220722190700.png]]

At the end we introduce the four-point vertex $V^{(2)}_{(\alpha_1\alpha_2)(\alpha_3\alpha_4)} = V(x_{\alpha_1}, x_{\alpha_2}, x_{\alpha_3}, x_{\alpha_4})$ which is depends on four points of input data and is symmetric under exchanges of sample indices: $\alpha_1 \leftrightarrow \alpha_2, \alpha_3 \leftrightarrow \alpha_4, (\alpha_1,\alpha_2) \leftrightarrow (\alpha_3,\alpha_4)$.

Here we also see that as for $n_1 \gg 1$, since $V$ is of order one, the metric fluctuation will become more and more suppressed. We see that the metric fluctuation will become more and more Gaussian due to the central limit theorem. In the limit as $n_1$ tends to infinity the fluctuation will dissapear.

There are now two ways of integrating out $z^{(1)}$ and obtaining $p(z^{(2)}|\mathcal{D})$, one brute-force involving lots of wick contractions, and one clever:

#### Wick Derivation Results:
- Expectation of a function under a nearly Gaussian distribution
![[Pasted image 20220725125708.png]]


#### Clever derivation:
Plug the conditional distribution (4.35) into the marginalization equation (4.34):

![[Pasted image 20220722201106.png]]

Use the previously discussed decomposition of the stochastic metric into its mean and fluctuating parts:

![[Pasted image 20220722202157.png]]

To write a Neumann series for the inverse of this:

![[Pasted image 20220722202325.png]]

Then put this into the exponential of the marginal distribution in (4.53):

![[Pasted image 20220722202444.png]]

Then the denominator becomes:
![[Pasted image 20220722202757.png]]
The first line is expressing the determinant as a Gaussian integral and the second is substituting in (4.56).

Now we plug these two expressions back into (4.53) to get:

![[Pasted image 20220722204631.png]]

(Not sure about this) Where they have used that $\mathbb{E}\left[ \hat{\Delta G}^{(2)}_{\beta_1\beta_2}\right] = 0$ and $\mathbb{E}\left[ \hat{\Delta G}^{(2)}_{\beta_1\beta_2}\hat{\Delta G}^{(2)}_{\beta_3\beta_4}\right] = \frac{1}{n_1}V^{(2)}_{(\beta_1\beta_2)(\beta_3\beta_4)}$. Then taking log:

![[Pasted image 20220722210250.png]]

They mention that one might wonder why they drop the $1/{n_1}$ correction to the quadratic coupling, but keep the quartic coupling despite it being of the same order. They mention that such a correction is a subleading contribution to the two-point correlator, while the quartic coupling gives the leading contribution to the connected four-point correlator. In short, the first is a minor quantitative effect, while for the latter there will be observables whose leading contributions come soley from the quartic coupling.

#### Nearly-Gaussian action in action

- Using a previously derived equation for the expectation of a function under a nearly-gaussian distribution they show how to obtain the expectations of two activations on the same neuron, and four activations: two pairs on seperate neurons and all four on one neuron.
	- There is a non-trivial effect from the quartic coupling $v$, and pairs of neurons can only correlate by adding a quartic action, highlighting the importance of finite width for feature learning.
- They give a formula for the covariance between two functions that depend on subsamples of the data:
![[Pasted image 20220725130229.png]]

### Deeper Layers: Accumulation of Non-Gaussianity
By following the same procedure as the one for the second-layer distribution we can proceed to find the marginal distribution of an arbitrary layer. Care must be taken however as the previous layers will no longer be gaussian.

- Recursive strategy: Reconstruct the $(l+1)$-th layer marginal distribution out of the $(l+1)$-th layer preactivation correlators, then use the $l$-th layer action to evaluate the expectations of the $l$-th layer activations that occur in the expressions for the $(l+1)$-th layer preactivation correlators.

#### Recursion
- Using previous work they are able to derive expressions for the two-point correlator and the connected four-point correlator of the $(l+1)$-th layer in terms of the correlators for the $l$-th layer. These correlators can be used to obtain the $(l+1)$-th layer marginal.
- This can be done efficiently by finding the action of the preactivation distribution.

#### Action
- The preactivation function can be written in terms of an action $S(z^{(l)})$
- The ansatz for the action:
![[Pasted image 20220725132140.png]]

- The coefficients are data-dependent couplings, and the results in (4.2) can be generalised to the $l$-th layer
![[Pasted image 20220725133002.png]]
- The higher order terms $\mathcal{O}(...)$ can only be ignored iff the quartic coupling $v$ and higher order couplings are perturbatively small, which they show next.

#### Large-width expansion
- The calculations needed for the recursive strategy simplify in the wide regime, with a larger number of neurons per layer. (i.e the regime in which the networks are "practically usable and theoretically tractable").
- To be brief, when in this regime the order of the mean metric $G$ and four-point vertex $V$ is order one at layer $l$ and remains order one at layer $l+1$ 
- They derive recursion relations for this mean metric and four-point vertex:

![[Pasted image 20220725133920.png]]

![[Pasted image 20220725134140.png]]

- "The additional finite-width corrections given by the higher-order terms in the action can change quantitative results but should not really exhibit qualitative differences." - Is this true?


## Marginalisation rules
- In this section they show how to perform marginalisations over a subset of the data or a subset of neurons.
	- Over Data:
		- Allows us to simplify the recursion for the two-point correlator by considering integrals only over the two samples of interest rather than using $\mathcal{N}_\mathcal{D}$ integrals.
	- Over neurons:
		- Can be used to overcome some perturbation scaling issues by integrating over a reduced set of neurons. (See the book)
- The couplings depend on the number of neurons in the action, and they show how how to account for this. The key takeaway is that observables of the $l$-th layer depend on the number of neurons in that layer.

## Subleading Corrections