# Adapted from the code in Chapter 2 of the book "Probabilistic Programming
# and Bayesian Methods for Hackers", this code uses PyMC to analyze
# the results of a landing page test. I added support for using real
# clicks and orders from landing page testing data.
# To use your own data, just update the clicks_A, clicks_B,
# orders_A, and orders_B variables.


import numpy as np
import pymc as pm
import matplotlib.pyplot as plt

clicks_A = 1135
orders_A = 5
clicks_B = 1149
orders_B = 17

data_A = np.r_[ [0] * (clicks_A - orders_A), [1] * orders_A ]
data_B = np.r_[ [0] * (clicks_B - orders_B), [1] * orders_B ]

# The rest of this code comes from Chapter 2 the book
# "Probabilistic Programming and Bayesian Methods for Hackers"
# which can be found here:
# https://github.com/CamDavidsonPilon/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers

p_A = pm.Uniform('p_A', lower=0, upper=1)
p_B = pm.Uniform('p_B', lower=0, upper=1)

@pm.deterministic
def delta(p_A=p_A, p_B=p_B):
    return p_B - p_A

obs_A = pm.Bernoulli("obs_A", p_A, value = data_A, observed = True)
obs_B = pm.Bernoulli("obs_B", p_B, value = data_B, observed = True)

mcmc = pm.MCMC([p_A, p_B, delta, obs_A, obs_B])
mcmc.sample(20000, 1000)

p_A_samples = mcmc.trace("p_A")[:]
p_B_samples = mcmc.trace("p_B")[:]
delta_samples = mcmc.trace("delta")[:]

print "Observed conversion rate of page A: ", '{percent:.2%}'.format(percent=data_A.mean())
print "Observed conversion rate of page B: ", '{percent:.2%}'.format(percent=data_B.mean())

print "Probability site A is BETTER than site B: %.3f" % \
    (delta_samples < 0).mean()

print "Probability site A is WORSE than site B: %.3f" % \
    (delta_samples > 0).mean()

ax = plt.subplot(311)

plt.xlim(0, .035)
plt.hist(p_A_samples, histtype='stepfilled', bins=25, alpha=0.85,
         label="posterior of $p_A$", color="#A60628", normed=True, edgecolor = "none")
plt.legend(loc="upper right")
plt.title("Posterior distributions of $p_A$, $p_B$, and delta unknowns")

ax = plt.subplot(312)

plt.xlim(0, .035)
plt.hist(p_B_samples, histtype='stepfilled', bins=25, alpha=0.85,
         label="posterior of $p_B$", color="#467821", normed=True, edgecolor = "none")
plt.legend(loc="upper right")

ax = plt.subplot(313)
plt.ylim(0,120)
plt.hist(delta_samples, histtype='stepfilled', bins=50, alpha=0.85,
         label="posterior of $p_B$ - $p_A$", color="#7A68A6", normed=True, edgecolor = "none")
plt.legend(loc="upper right")
plt.vlines(0, 0, 120, color="black", alpha = .5)

plt.show()