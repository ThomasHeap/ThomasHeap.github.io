---
title: "Massively Parallel Reweighted Wake-Sleep"
collection: publications
permalink: /publication/MPRWS
date: 2009-10-01
venue: 'UAI'
paperurl: 'https://arxiv.org/abs/2305.11022f'

---
Reweighted wake-sleep (RWS) is a machine learning method for performing Bayesian inference in a very general class of models.
RWS draws $K$ samples from an underlying approximate posterior, then uses importance weighting to provide a better estimate of the true posterior.
RWS then updates its approximate posterior towards the importance-weighted estimate of the true posterior.
However, recent work [Chattergee and Diaconis, 2018] indicates that the number of samples required for effective importance weighting is exponential in the number of latent variables.
Attaining such a large number of importance samples is intractable in all but the smallest models.
Here, we develop massively parallel RWS, which circumvents this issue by drawing $K$ samples of all $n$ latent variables, and individually reasoning about all $K^n$ possible combinations of samples.
While reasoning about $K^n$ combinations might seem intractable, the required computations can be performed in polynomial time by exploiting conditional independencies in the generative model.
We show considerable improvements over standard "global" RWS, which draws $K$ samples from the full joint.

https://arxiv.org/abs/2305.11022
