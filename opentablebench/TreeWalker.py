"""TreeWalker contains functions for walking a tree."""

import itertools


def build_permutation_tree(tree):
    """
    Build permutation tree.

    Given list [1,2,1] it will produce output such as:
    [0,0,0]
    [0,0,1]
    [0,1,0]
    [0,1,1]
    ...
    [1,2,1]

    Suboptimal. Memory explodes at one point.
    """
    permutations = []
    initial_value = [0] * len(tree)
    r_edges_length_list = list(reversed(tree))
    index = 0
    while True:
        if initial_value[index] < r_edges_length_list[index]:
            if index == 0:
                initial_value[index] += 1
            else:
                initial_value[index] += 1
                for reset in range(0, index):
                    initial_value[reset] = 0
                index = 0
            permutations.append(list(reversed(initial_value)))

        if initial_value[index] >= r_edges_length_list[index]:
            index += 1

        if initial_value == r_edges_length_list:
            break

    return permutations


def sort_permutation_tree(permutations):
    """
    Sort permutation tree.

    Sorting by sum of all elements.
    This is required function for build_permutation_tree
    """
    # pylint: disable=W0108
    return sorted(permutations, key=lambda x: sum(x))


def get_distribution_permutations(distribution):
    """Return permutations of a list."""
    return itertools.permutations(list(distribution))


def distribute_weight(weight, number_of_buckets):
    """Distribute weigth in N buckets."""
    if weight == 0 and number_of_buckets == 0:
        raise Exception("Can not distribute 0 weight in 0 buckets")

    if number_of_buckets == 1:
        return set([(weight)])

    if weight == 0:
        return set([tuple([0] * number_of_buckets)])

    sums = set()

    state = [0] * number_of_buckets
    state[0] = weight
    new_states = [tuple(state)]
    sums.add(tuple(state))
    while True:
        states = list(set(new_states))
        sums_before_evaluation = len(sums)
        while states:
            state = list(states.pop())
            state[0] -= 1
            for i in range(1, number_of_buckets):
                intermediate_state = state[:]
                intermediate_state[i] += 1
                intermediate_state = sorted(intermediate_state, reverse=True)
                sums.add(tuple(intermediate_state))
                new_states.append(tuple(intermediate_state))
        sums_after_evaluation = len(sums)
        if sums_before_evaluation == sums_after_evaluation:
            break
    return sums


def is_permutation_fit_buckets(permutation, buckets):
    """Check if permutation can be fit into buckets."""
    for i in range(0, len(permutation)):
        if permutation[i] > buckets[i]:
            return False
    return True


def _distribute_weight_recursive(iter1, iter2):
    if iter2 == 0:
        yield [iter1]
    if iter1 == 0:
        yield iter2 * [0]
    for iter3 in range(iter1):
        for iter4 in _distribute_weight_recursive(iter3, iter2 - 1):
            result = [iter1 - iter3] + iter4
            try:
                if iter1 - iter3 >= iter4[0] and len(result) == iter2:
                    yield result
            except IndexError:
                continue


def distribute_weight_recursive(iter1, iter2):
    """
    Distribute weights recursively.

    Implementation provided by Micha Hoffmann.
    """
    for partition in _distribute_weight_recursive(iter1, iter2 + 1):
        yield partition[:-1]


def distribute_weight_faster(iter1, buckets, minimum=0):
    """Faster implementation of distribute_weight_recursive."""
    if buckets == 1:
        if iter1 == 0:
            return [[]]
        else:
            return [[iter1]]

    partitions = []
    for iter2 in range(minimum, iter1):
        sub_partitions = distribute_weight_faster(
            iter1 - iter2,
            buckets - 1,
            iter2
        )
        for sub_partition in sub_partitions:
            if iter2 <= sub_partition[-1]:
                partitions.append(sub_partition + [iter2])
    return partitions


def get_integer_partitions(iter1):
    """
    Get integer partitions.

    http://jeromekelleher.net/category/combinatorics.html
    """
    partition = [0 for i in range(iter1 + 1)]
    iter2 = 1
    iter3 = iter1 - 1
    while iter2 != 0:
        iter4 = partition[iter2 - 1] + 1
        iter2 -= 1
        while 2 * iter4 <= iter3:
            partition[iter2] = iter4
            iter3 -= iter4
            iter2 += 1
        iter5 = iter2 + 1
        while iter4 <= iter3:
            partition[iter2] = iter4
            partition[iter5] = iter3
            yield partition[:iter2 + 2]
            iter4 += 1
            iter3 -= 1
        partition[iter2] = iter4 + iter3
        iter3 = iter4 + iter3 - 1
        yield partition[:iter2 + 1]
