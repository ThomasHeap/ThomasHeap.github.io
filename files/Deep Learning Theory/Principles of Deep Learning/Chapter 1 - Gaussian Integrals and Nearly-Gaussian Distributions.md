## Integrating Multivariate Gaussians
$$
\begin{aligned}
I_K = &\int d^Nz \ \mathrm{exp}\left[-\frac{1}{2}\sum_{\mu,\nu = 1}^N z_\mu(K^{-1})_{\mu\nu} \ z_\nu \right] \\
=& \int d_{z_1} \int d_{z_2} ... \int d_{z_N} \mathrm{exp} \left[-\frac{1}{2}\sum_{\mu,\nu = 1}^N z_\mu(K^{-1})_{\mu\nu} \ z_\nu \right]
\end{aligned}
$$
Note, since K is symmetric, we can diagonalize K with orthogonal matrix $O_{\mu\nu}$ which gives $(OK^{-1}O^T)_{\mu\nu} = (1/\lambda_\mu)\delta_{\mu\nu}$ with eigenvalues $\lambda_{\mu = 1,...,N}$. Knowing this:

$$
\sum_{\mu,\nu = 1}^N z_\mu(K^{-1})_{\mu\nu} \ z_\nu = \sum_{\mu=1}^N \frac{1}{\lambda_\mu}(Oz)^2_\mu
$$
This transforms the nested integrals above into a product of single variable gaussian integrals:

$$
I_K = \prod_{\mu=1}^{N} \left[ \int du_\mu \mathrm{exp}\left(-\frac{u^2_\mu}{2\lambda_\mu}\right) \right] = \sqrt{\prod_{\mu=1}^{N} (2\pi\lambda_\mu)} = \sqrt{|{2\pi K}|}
$$
Where the final equality is from noting that the product of the eigenvalues of a matrix equals its determinant.
### Using source terms to evaluate moments
By including a source term $J$ we can express the generating function of a multivariate gaussian as:

$$
Z_{K,J} = \sqrt{|2\pi K|} \mathrm{exp}\left( \frac{1}{2} \sum_{\mu,\nu = 1}^N J^\mu K_{\mu\nu}J^\nu \right)
$$
Differentiating this function with respect to the source term "brings down a power of $z_\mu$" so can be used to evaluate gaussian integrals with insertions:

$$
\begin{aligned}
I_{K,(\mu_1,\mu_2,...,\mu_M)} &= \int d^Nz \ \mathrm{exp}\left(-\frac{1}{2}\sum_{\mu,\nu = 1}^N z_\mu(K^{-1})_{\mu\nu} \ z_\nu \right)z_{\mu_1}z_{\mu_2}...z_{\mu_M} \\
&=\left[\frac{d}{dJ^{\mu_1}}\frac{d}{dJ^{\mu_2}}...\frac{d}{dJ^{\mu_M}} Z_{K,J}\right]_{J=0}
\end{aligned}
$$
Using this we get the following expression for gaussian integrals with an even number of insertions $M=2m$:

$$
\begin{aligned}
\mathbb{E}[z_{\mu_1}z_{\mu_2}...z_{\mu_M}] &= \frac{I_{K,(\mu_1,\mu_2,...,\mu_M)}}{I_K} \\
&=\frac{1}{I_K}\left[\frac{d}{dJ^{\mu_1}}\frac{d} {dJ^{\mu_2}}...\frac{d}{dJ^{\mu_M}} Z_{K,J}\right]_{J=0} \\
&=\frac{1}{2^m m!}\frac{d}{dJ^{\mu_1}}\frac{d}{dJ^{\mu_2}}...\frac{d}{dJ^{\mu_M}} \left( \sum_{\mu,\nu = 1}^N J^\mu K_{\mu\nu}J^\nu \right)^m
\end{aligned}
$$

Using this, it is possible to derive Wick's Theorem for gaussians:

$$
\mathbb{E}[z_{\mu_1}z_{\mu_2}...z_{\mu_M}] = \sum_{\mathrm{all \ \ pairings}} K_{\mu_{k_1}\mu_{k_2}}...K_{\mu_{k_{2m-1}}\mu_{k_{2m}}}
$$

Note there are $(2m-1)!!$ terms in this sum. Double factorial: https://en.wikipedia.org/wiki/Double_factorial

### Connected Correlators
If we knew all the moments (or M-point correlators) of our distribution we would be able to calculate the expectation of any analytic function (observable) via Taylor expansion. But actually estimating these moments is challenging, for the M'th moment (M-point correlator) we would need to measure M components of a random variable for each sample and repeat this multiple times.

Luckily we can often specify distributions using a smaller number of quanities, for example gaussians are constrained by their mean and covariance. These are the first and second cumulants or connected correlators:

$$
\begin{aligned}
\mathbb{E}[z_\mu]|_{\mathrm{connected}} &= \mathbb{E}[z_\mu] \\

\mathbb{E}[z_\mu z_\nu]|_{\mathrm{connected}} &= \mathbb{E}[z_\mu z_\nu] - \mathbb{E}[z_\mu]\mathbb{E}[z_\nu]
\end{aligned}
$$

For gaussian distributions it can be shown that all connected correlators higher than this ($M>2$) are zero. We define nearly-Gaussian distributions as those distributions for which the connected correlators are small.

### Nearly-Gaussian Distributions
How can we link small but non-zero connected correlators (observables) to the functional form of the distribution?

We can use actions $S(z)$, which define unnormalised probability distributions as so:

$$
p(z) \propto e^{-S(z)}
$$
The action function for a standard multivariate gaussian is called the quadratic action. 

If we deform the Gaussian distribution by the addition of a small quartic term added to the quadratic action we can recover a small non-zero four-point correlator:


$$
S(z) = \frac{1}{2} \sum_{\mu,\nu =1}^N K^{\mu\nu}z_\mu z_\nu + \frac{\epsilon}{4!} \sum_{\mu,\nu,\rho,\lambda = 1}^N V^{\mu\nu\rho\lambda}z_\mu z_\nu z_\rho z_\lambda
$$
Where V is a $(N \times N \times N \times N)$-dimensional tensor that is completely symmetric in all four indices (hence the $4!$ term to compensate for overcounting)
$$
\mathbb{E}[z_{\mu_1}z_{\mu_2}z_{\mu_3}z_{\mu_4}]|_{\mathrm{connected}} = O(\epsilon)
$$

Using this in conjuction with pertubative methods we can show an explicit relationship between the 4-point correlator and the quartic coupling.

This is possible because of the small dimensionless parameter $\epsilon$, which in future chapters will be provided by the inverse of the width of a neural network, which will allow similar analysis of the nearly-gaussian distributions which arise from neural networks.