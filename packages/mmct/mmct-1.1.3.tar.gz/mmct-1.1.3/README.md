# mmct

Provides functionality for performing multinomial tests using monte carlo simulation

![Tests](https://github.com/cwand/mmct/actions/workflows/tests.yml/badge.svg)

## Background

This library contain python code that can be used to test whether a given set of observations are
likely to be drawn from a multinomial distribution with a given set of parameters (probabilities
for each case). The test is done using Monte Carlo methods. A bunch of random samples from the
hypothesised distribution is drawn and the probability of each sample is calculated.  These are all
compared to the probability of the sample under test. The p-value of the null-hypothesis (that the 
sample comes from the distribution) is simply the fraction of random samples with probability
smaller than the sample under test.

The library is inspired by [met](https://pypi.org/project/met/), which achieve the same objective
as mmct, but does so by painstakingly enumerating every possible case for the given multinomial
distribution and calculating the p-value exactly. While this is certainly preferable, it becomes
very slow very quickly, so for performing many tests or tests with a large parameter space, a
monte carlo approximation may be good enough. mmct has also drawn inspiration
from the [XNomial](https://cran.r-project.org/web/packages/XNomial/vignettes/XNomial.html) package,
which performs an identical task in the R programming language.

## Usage

The package is most easlily installed via pip:

```text
pip install mmct
```

The source code is also available on GitHub and is free for use and modification:
[mmct on GitHub](https://github.com/cwand/mmct/)

When the package has been installed, a test can be performed following the example below, in which
we test whether a set of dice rolls could have been generated from rolling two fair dice 20 times
and adding the eyes:

```text
import mmct
import numpy as np
#     Eyes    2  3  4  5  6  7  8  9 10 11 12
x = np.array([0, 0, 2, 4, 5, 2, 3, 1, 0, 1, 2])
# Hypothsised probabilities:
p = np.array([1/36, 2/36, 3/36, 4/36, 5/36, 6/36, 5/36, 4/36, 3/36, 2/36, 1/36])
# Initialise tester:
t = mmct.mt_tester() # Use the multithreaded tester class
# Set number of Monte Carlo samples to generate
t.n_samples = 100000
pval = t.do_test(x,p)
```

The result of the test will of course vary (unless the random simulator is seeded), but should in
general result in a p-value around 0.34, i.e. we cannot reject the hypothesis that the numbers
above are taken from a fair dice rolling (which they actually are).
