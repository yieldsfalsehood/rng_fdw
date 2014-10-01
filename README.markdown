# Overview

This is rng_fdw, a random number generator foreign data wrapper for
postgres.

# Setup

You'll need to install [multicorn](http://multicorn.org/) (which
implies you'll also need python and postgres). Then install this
package somewhere python can find it - either do `sudo python setup.py
install` or play around with getting multicorn working in a
virtualenv.

```
-- Create the multicorn extension
create extension multicorn;

-- Add a foreign server for the RNG wrapper
create server rng_srv foreign data wrapper multicorn
options (
  wrapper 'rng_fdw.RNGWrapper'
)
;
```

# Usage

Once those are in place we can start using the wrapper. For each
distribution family for which we want to generate random variates
we'll need a corresponding foreign table, like this:

```
-- Create a schema to hold the distribution tables.
create schema rng;

-- Tie a distribution to a table
create foreign table rng.norm_variates
(
  loc float,
  scale float,
  size int,
  val float
) server rng_srv options (
  distribution 'norm'
)
;
```

Now, to actually generate variates using this distribution, we select
from it, passing the distribution parameters as predicates in the
where clause.

```
-- Generate 3 variates from N(3.1, 2.2)
select *
from rng.norm_variates
where mu = 3.1
  and sigma = 2.2
  and size = 3
;
```
