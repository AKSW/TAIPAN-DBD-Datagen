"""TreeWalker contains functions for walking a tree. :)"""

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
    return sorted(permutations, key=lambda x: sum(x))


def get_distribution_permutations(distribution):
    return itertools.permutations(list(distribution))


def distribute_weight(weight, number_of_buckets):
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
    for i in range(0, len(permutation)):
        if permutation[i] > buckets[i]:
            return False
    return True


def _distribute_weight_recursive(n, m):
    if m == 0:
        yield [n]
    if n == 0:
        yield m * [0]
    for i in range(n):
        for l in _distribute_weight_recursive(i, m - 1):
            res = [n - i] + l
            try:
                if n - i >= l[0] and len(res) == m:
                    yield res
            except IndexError:
                continue


def distribute_weight_recursive(n, m):
    """
        Distribute weights recursively.

        Implementation provided by Micha Hoffmann.
    """
    for partition in _distribute_weight_recursive(n, m + 1):
        yield partition[:-1]


def distribute_weight_recursive_faster(n, b, minimum=0):
    if b == 1:
        if n == 0:
            return [[]]
        else:
            return [[n]]

    partitions = []
    for i in range(minimum, n):
        sub_partitions = distribute_weight_recursive_faster(n - i, b - 1, i)
        for sub_partition in sub_partitions:
            if i <= sub_partition[-1]:
                partitions.append(sub_partition + [i])
    return partitions


def get_integer_partitions(n):
    """
        Get integer partitions.

        http://jeromekelleher.net/category/combinatorics.html
    """
    a = [0 for i in range(n + 1)]
    k = 1
    y = n - 1
    while k != 0:
        x = a[k - 1] + 1
        k -= 1
        while 2 * x <= y:
            a[k] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            a[k] = x
            a[l] = y
            yield a[:k + 2]
            x += 1
            y -= 1
        a[k] = x + y
        y = x + y - 1
        yield a[:k + 1]
