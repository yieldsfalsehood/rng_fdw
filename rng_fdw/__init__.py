#!/usr/bin/env python

from multicorn import ForeignDataWrapper

import numpy as np
import scipy.stats

class RNGWrapper(ForeignDataWrapper):

    def __init__(self, options, columns):

        super(RNGWrapper, self).__init__(options, columns)
        self.columns = columns

        # default to the normal distribution if none was specified
        distribution = options.get("distribution", "norm")

        # this should be made to fail indicating that the distribution
        # given doesn't exist
        try:
            self.func = getattr(scipy.stats, distribution)
        except:
            pass

    def execute(self, quals, columns):

        has_size = False
        size = 20
        params = dict()

        for qual in quals:

            # right now we only handle simple equality
            # constraints. any other predicates will cause no results
            # to be generated (because they won't be satisfied).
            if qual.is_list_operator or qual.operator != "=":
                pass

            # if a constraint on "size" is given, use that to override
            # the default value (20). otherwise, keep a record of the
            # parameters provided and their values
            if qual.field_name == "size":
                has_size = True
                size = qual.value
            else:
                params[qual.field_name] = np.float(qual.value)

        # instantiate a distribution object from the parameters and
        # generate some variates!
        F = self.func(**params)
        for x in F.rvs(size=size):
            # this is a messy way of saying:
            # 1. set the column "val" to the value of this variate
            # 2. include all the equality predicates that were passed
            #    in as extracted above
            # 3. set the column "size" to the provided value if one
            #    was given (otherwise leave it null)
            d = dict([("val", x)] + params.items() + ([("size", size)] if has_size else []))
            yield d
