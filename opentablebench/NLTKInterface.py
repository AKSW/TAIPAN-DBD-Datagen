"""NLTKInterface for NLP related tasks."""

import operator
import random
import re

from nltk.corpus import wordnet as wn  # pylint: disable=import-error
from palmettopy.palmetto import Palmetto  # pylint: disable=import-error

from . import TreeWalker as tw
from .config import TABLE_HEADERS_FILE
from .FileReader import FileReader
from .Logger import get_logger

LOGGER = get_logger(__name__)


def get_header_synsets(header):
    """
    Return synsets for each header item.

    The format is [("header item1", [synset1, synset2]), ...]
    """
    synsets_header_pack = []
    for item in header:
        # if item is several words -- get synsets for all of those
        synsets = []
        subitems = []
        # split by space first
        subitems = _split_header_item_spaces(item)
        # if empty split by camelcase
        if len(subitems) == 1:
            subitems = _split_header_item_camelcase(item)
        for subitem in subitems:
            synsets.extend(wn.synsets(subitem, pos='n'))
        synsets_header_pack.append((item, synsets))
    return _prune_header_synsets(synsets_header_pack)


def _prune_header_synsets(synsets_header_pack):
    pruned_synsets_header_pack = []
    for (label, synsets) in synsets_header_pack:
        distinct_synsets = set()
        for synset in synsets:
            synset_name = synset.name().split(".")[0]
            # filtering complex synset (two and more words)
            # palmetto can not handle them at the moment
            if synset_name.find("_") == -1:
                distinct_synsets.add(synset_name)
        pruned_synsets = []
        while distinct_synsets:
            for synset in synsets:
                synset_name = synset.name().split(".")[0]
                if synset_name in distinct_synsets:
                    distinct_synsets.remove(synset_name)
                    pruned_synsets.append(synset)
        pruned_synsets_header_pack.append((label, pruned_synsets))

    return pruned_synsets_header_pack


def _split_header_item_camelcase(string):
    _camel_case_regex = re.compile(r"([A-Z])")
    _token_list = _camel_case_regex.split(string)

    _word_list = [_token_list[0]]
    for i, _ in enumerate(_token_list):
        if i % 2 == 1:
            word = "".join([_token_list[i], _token_list[i + 1]])
            _word_list.append(word)

    return _word_list


def _split_header_item_spaces(string):
    """Clean and split header into an array of strings."""
    split_by_space = re.compile(r"[\s]+")
    header_items = split_by_space.split(string)
    return list(
        map(
            _filter_non_print_chars,
            header_items
        )
    )


def _filter_non_print_chars(string):
    pattern = re.compile(r"[\W_]+")
    return pattern.sub('', string)


def build_weighted_graph(synset_packs):
    """
    Build a weighted graph out of synset packs.

    Return a list of tuples with weights such as:
    [
        [((item_a, item_b), 1.534), (item_a, item_c), 1.1234],
        [((item_c, item_d), 1.34), (item_c, item_f), 1.24],
        ...
    ]
    """
    # get all document frequencies
    # collect all terms
    words = []
    for i in range(0, len(synset_packs)):
        for j in range(0, len(synset_packs[i][1])):
            synset_packs[i][1][j] = synset_packs[i][1][j].name().split(".")[0]
            words.append(synset_packs[i][1][j])
        if len(synset_packs[i][1]) == 0:
            synset_packs[i][1].append(synset_packs[i][0])
            words.append(synset_packs[i][0])

    palmetto = Palmetto()
    doc_id_tuples = palmetto.get_df_for_words(words)
    doc_id_tuples_dict = dict(doc_id_tuples)

    edges = []
    for i in range(0, len(synset_packs)):
        for j in range(i + 1, len(synset_packs)):
            edge = []
            for that_word in synset_packs[j][1]:
                for this_word in synset_packs[i][1]:
                    edge_item = (
                        (
                            this_word,
                            that_word
                        ),
                        calculate_coherence(
                            this_word,
                            that_word,
                            doc_id_tuples_dict
                        )
                    )
                    edge.append(edge_item)
            edges.append(sorted(edge, key=lambda x: x[1], reverse=True))
    return edges


def calculate_coherence(word_a, word_b, doc_id_tuples_dict):
    """Calculate coherence between word_a and word_b."""
    corpus_size = 4264684
    doc_id_set_a = doc_id_tuples_dict[word_a]
    doc_id_set_b = doc_id_tuples_dict[word_b]
    doc_id_set_ab = len(doc_id_set_a.intersection(doc_id_set_b))
    if len(doc_id_set_a) == 0 or len(doc_id_set_b) == 0:
        coherence = 0
    else:
        coherence = \
            (doc_id_set_ab * corpus_size) / \
            (len(doc_id_set_a) * len(doc_id_set_b))
    return coherence


def pick_next_subgraph(synset_graph, permutation):
    """Pick next subgraph from permutation list."""
    pick = []
    for index in range(0, len(permutation)):
        pick.append(
            synset_graph[index][permutation[index]][0]
        )
    return pick


def is_graph_converge(subgraph, number_of_nodes):
    """
    Check if graph converge.

    Basically check if graph is a complete graph,
    as it is a required condition to have a valid header
    on output.
    """
    incoming_edges = set(map(lambda x: x[1], subgraph))
    outcoming_edges = set(map(lambda x: x[0], subgraph))
    all_nodes = incoming_edges.union(outcoming_edges)
    if len(all_nodes) == number_of_nodes:
        return True
    else:
        return False


def cluster_header_palmetto(header):
    """
    Find clusters for synsets_header_pack.

    Cluster synsets of a header based on the similarity
    between synsets of different columns.
    Number of clusters is equal to the minimum number of synsets
    for a column. That is if column "city" got 2 synsets and all other
    columns have > 2 synsets, there will be exactly 2 clusters.
    In case when column has no synsets, it is not considered in clustering
    and just attached to the resulting cluster at the end of calculation.
    This calculation is using graph algorithm.
    """
    synset_packs = get_header_synsets(header)
    number_of_nodes = len(header)
    synset_graph = build_weighted_graph(synset_packs)
    edges_length_list = list(map(lambda x: len(x) - 1, synset_graph))
    permutation_tree = tw.build_permutation_tree(edges_length_list)

    sorted_permutation_tree = tw.sort_permutation_tree(permutation_tree)

    for permutation in sorted_permutation_tree:
        subgraph = pick_next_subgraph(
            synset_graph,
            permutation
        )
        if is_graph_converge(subgraph, number_of_nodes):
            break

    assert is_graph_converge(subgraph, number_of_nodes),\
        "subgraph does not converge!"

    _header = set(sum(list(map(lambda x: [x[0], x[1]], subgraph)), []))
    new_header = []
    for synset_pack in synset_packs:
        (_, synsets) = synset_pack
        for synset in synsets:
            if synset.split(".")[0] in _header:
                new_header.append(synset)
    return new_header


def get_max_subgraph(max_weight, number_of_nodes,\
    edges_length_list, synset_graph):
    print(max_weight)
    print(len(edges_length_list))
    for weight in range(0, max_weight):
        for _dist in tw.distribute_weight_recursive(weight, len(edges_length_list)):
            for permutation in tw.get_distribution_permutations(_dist):
                if tw.is_permutation_fit_buckets(
                    permutation,
                    edges_length_list):
                    subgraph = pick_next_subgraph(
                        synset_graph,
                        permutation
                    )
                    if is_graph_converge(subgraph, number_of_nodes):
                        return subgraph
    raise Exception("subgraph does not converge!")


def cluster_header_palmetto_walker(header):
    """
    Find clusters for synsets_header_pack.

    Use optimized distribute_weight and get_distribution_permutations
    functions to walk the tree.
    NP complete problem.
    http://www.optimization-online.org/DB_FILE/2014/12/4678.pdf
    http://www.caam.rice.edu/~yad1/miscellaneous/References/Math/Topology/Cliques/Maximal%20Clique%20Problem.pdf
    """
    synset_packs = get_header_synsets(header)
    number_of_nodes = len(header)
    synset_graph = build_weighted_graph(synset_packs)
    edges_length_list = list(map(lambda x: len(x) - 1, synset_graph))

    max_weight = sum(edges_length_list)

    subgraph = get_max_subgraph(
        max_weight,
        number_of_nodes,
        edges_length_list,
        synset_graph
    )

    _header = set(sum(list(map(lambda x: [x[0], x[1]], subgraph)), []))
    new_header = []
    for synset_pack in synset_packs:
        (_, synsets) = synset_pack
        for synset in synsets:
            if synset.split(".")[0] in _header:
                new_header.append(synset)
    return new_header


def cluster_header_random(header):
    """
    Cluster synsets using palmetto.

    Randomly select permutation of the header and
    calculate coherence. Repeat until algorithm converges.
    """
    palmetto = Palmetto()
    synsets_pack = get_header_synsets(header)

    window_size = 3
    window = []
    maximum_coherence = 0
    index = 0
    no_change = 0
    best_permutation = []
    while True:
        random_permutation = _pick_random_synset_permutation(synsets_pack)
        coherence = palmetto.get_coherence(random_permutation)
        window.append(
            (
                random_permutation,
                coherence
            )
        )

        if index % window_size == 0:
            (local_best_permutation, local_maximum_coherence) = max(
                window,
                key=lambda x: x[1]
            )
            if local_maximum_coherence > maximum_coherence:
                maximum_coherence = local_maximum_coherence
                best_permutation = local_best_permutation
            else:
                no_change = no_change + 1
            window = []

        if no_change > 2:
            break

        index = index + 1
    return best_permutation


def _pick_random_synset_permutation(synsets_pack):
    permutation = []
    for (label, synsets) in synsets_pack:
        if synsets == []:
            permutation.append(label)
        else:
            _random_element = random.choice(synsets).name().split(".")[0]
            permutation.append(_random_element)

    return permutation


def cluster_header_naive(header):
    """
    Cluster synsets by maximum similarity.

    The problem is that it might get stuck in a local maximum.
    To overcome the problem it is necessary to employ more sophisticated
    clustering methods.
    """
    synsets_pack = get_header_synsets(header)
    (minimal_column, minimum_synsets) = _pick_minimal_column(synsets_pack)
    import ipdb; ipdb.set_trace()

    # fix the minimum column
    verbalized_headers = []
    for minimal_column_item in range(0, minimum_synsets):
        (_item, _synsets) = synsets_pack[minimal_column]
        _synset = _synsets[minimal_column_item]

        # find the shortest path to each column
        shortest_path = []
        shortest_path.append(
            (_convert_synset_to_header_item(_synset), minimal_column)
        )
        evaluated_columns = []
        evaluated_columns.append(minimal_column)
        next_synset = _synset
        (shortest_path, total_similarity) = _find_shortest_path(
            synsets_pack,
            next_synset,
            evaluated_columns,
            header,
            shortest_path
        )

        shortest_path = sorted(shortest_path, key=lambda x: x[1])
        verbalized_header = list(map(lambda x: x[0], shortest_path))
        verbalized_headers.append(
            (
                verbalized_header,
                total_similarity,
                len(evaluated_columns)
            )
        )
    return verbalized_headers


def _pick_minimal_column(synsets_pack):
    # Pick the column with minimum synsets
    minimal_column = 0
    minimum_synsets = 1000
    for index, synset_pack in enumerate(synsets_pack):
        (_, synsets) = synset_pack
        if len(synsets) > 0\
                and len(synsets) < minimum_synsets:
            minimum_synsets = len(synsets)
            minimal_column = index
    return (minimal_column, minimum_synsets)


def _find_shortest_path(
        synsets_pack,
        next_synset,
        evaluated_columns,
        header,
        shortest_path):
    total_similarity = 0
    while True:
        similarity_pairs = []
        for index, synset_pack in enumerate(synsets_pack):
            # skip evaluated columns
            if index in evaluated_columns:
                continue
            (_, synsets) = synset_pack
            closest_pair = _find_closest_synsets(
                [next_synset],
                synsets,
                index
            )
            similarity_pairs.append(closest_pair)

        # pick the closest element
        (closest_pair, similarity, index) = sorted(
            similarity_pairs,
            key=lambda x: x[1],
            reverse=True
        )[0]
        total_similarity += similarity

        if closest_pair == ():
            for index in range(0, len(header)):
                if index not in evaluated_columns:
                    shortest_path.append((header[index], index))
            break

        next_synset = closest_pair[1]
        shortest_path.append(
            (_convert_synset_to_header_item(next_synset), index)
        )

        evaluated_columns.append(index)
        if len(evaluated_columns) == len(synsets_pack):
            break
    return (shortest_path, total_similarity)


def _convert_synset_to_header_item(synset):
    return " ".join(synset.name().split(".")[0].split("_"))


def verbalize_header_naive(header):
    """Verbalize header items."""
    verbalized_headers = cluster_header_naive(header)
    top_header = sorted(
        verbalized_headers,
        key=operator.itemgetter(1, 2)
    )[0][0]

    return top_header


def verbalize_header_random(header):
    """Verbalize header using random algorithm."""
    return cluster_header_random(header)


def verbalize_header_palmetto(header):
    """Verbalize header using graph algorithm."""
    return cluster_header_palmetto_walker(header)


def _find_closest_synsets(synsets_1, synsets_2, index):
    closest_pair = ()
    max_similarity = 0
    if synsets_1 == [] or synsets_2 == []:
        return (closest_pair, 0, index)
    for _synset_1 in synsets_1:
        for _synset_2 in synsets_2:
            similarity = _calculate_similarity(_synset_1, _synset_2)
            if similarity > max_similarity:
                max_similarity = similarity
                closest_pair = (_synset_1, _synset_2)
    return (closest_pair, similarity, index)


def _calculate_similarity(synset_1, synset_2):
    similarity = synset_1.path_similarity(synset_2)
    if similarity is None:
        return 0
    else:
        return similarity


def load_test_data():
    """Load test headers from CSV file."""
    table_headers_file = FileReader(TABLE_HEADERS_FILE)
    table_headers = table_headers_file.readlines()
    # pylint: disable=unnecessary-lambda
    table_headers = list(map(lambda x: x.strip(), table_headers))
    # pylint: disable=eval-used
    table_headers = list(map(lambda x: eval(x), table_headers))
    return table_headers


def get_max_complexity_naive():
    """
    Calculate amount of combinations for the header permutations.

    i.e. if header is ["country", "city", "population"] and the synsets
    got [5, 6, 10] elements, then the complexity will be 5*6*10
    Max complexity is: 1120863744000
    """
    table_headers = load_test_data()
    maximum_complexity = 0
    for table_header in table_headers:
        complexity = 1
        synset_packs = get_header_synsets(table_header)
        for (_, synsets) in synset_packs:
            complexity = complexity * len(synsets)

        if maximum_complexity < complexity:
            maximum_complexity = complexity

    return maximum_complexity


def get_max_complexity_combinations():
    """
    Calculate amount of combinations for the header permutations.

    i.e. if header is ["country", "city", "population"] and the synsets
    got [5, 6, 10] elements, then the complexity will be
    5*6 + 5*10 + 6*10
    Max complexity is: 8056
    """
    table_headers = load_test_data()
    maximum_complexity = 0
    for table_header in table_headers:
        complexity = 0
        synset_packs = get_header_synsets(table_header)
        for outer_index in range(0, len(synset_packs)):
            outer_synset_pack_len = len(synset_packs[outer_index][1])
            for inner_index in range(outer_index, len(synset_packs)):
                inner_synset_pack_len = len(synset_packs[inner_index][1])
                complexity += outer_synset_pack_len * inner_synset_pack_len

        if maximum_complexity < complexity:
            maximum_complexity = complexity

    return maximum_complexity
