# coding:utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

def random_int32():
  return np.random.randint(low=0, high=np.iinfo(np.int32).max, dtype=np.int32)

def sample_with_exclusion(num_items, positive_set, n, replacement=True):
  # type: (int, typing.Iterable, int, bool) -> list
  """Vectorized negative sampling.

  This function samples from the positive set's conjugate, both with and
  without replacement.

  Performance:
    This algorithm generates a vector of candidate values based on the expected
    number needed such that at least k are not in the positive set, where k
    is the number of false negatives still needed. An additional factor of
    safety of 1.2 is used during the generation to minimize the chance of having
    to perform another generation cycle.

    While this approach generates more values than needed and then discards some
    of them, vectorized generation is inexpensive and turns out to be much
    faster than generating points one at a time. (And it defers quite a bit
    of work to NumPy which has much better multi-core utilization than native
    Python.)

  Args:
    num_items: The cardinality of the entire set of items.
    positive_set: The set of positive items which should not be included as
      negatives.
    n: The number of negatives to generate.
    replacement: Whether to sample with (True) or without (False) replacement.

  Returns:
    A list of generated negatives.
  """

  if not isinstance(positive_set, set):
    positive_set = set(positive_set)

  p = 1 - len(positive_set) /  num_items
  n_attempt = int(n * (1 / p) * 1.2)  # factor of 1.2 for safety

  # If sampling is performed with replacement, candidates are appended.
  # Otherwise, they should be added with a set union to remove duplicates.
  if replacement:
    negatives = []
  else:
    negatives = set()

  while len(negatives) < n:
    negative_candidates = np.random.randint(
        low=0, high=num_items, size=(n_attempt,))
    if replacement:
      negatives.extend(
          [i for i in negative_candidates if i not in positive_set]
      )
    else:
      negatives |= (set(negative_candidates) - positive_set)

  if not replacement:
    negatives = list(negatives)
    np.random.shuffle(negatives)  # list(set(...)) is not order guaranteed, but
    # in practice tends to be quite ordered.

  return negatives[:n]
