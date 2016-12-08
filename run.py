# from opentablebench.DataGeneratorRunner import DataGeneratorRunner
#
# RUNNER = DataGeneratorRunner()
# RUNNER.run()

# from opentablebench.NLTKInterface import \
#    calculate_maximum_complexity_combinations, \
#    calculate_maximum_complexity_naive
#
# print calculate_maximum_complexity_naive()
# print calculate_maximum_complexity_combinations()
#
#from opentablebench.NLTKInterface import verbalize_header_palmetto
#from opentablebench.NLTKInterface import verbalize_header_random
#from opentablebench.NLTKInterface import verbalize_header_naive
#from opentablebench.NLTKInterface import load_test_data
#header = ["label", "type", "subject"]
#headers = load_test_data()
#header = headers[0]
#print(header)
#print(verbalize_header_naive(header))

from opentablebench.TreeWalker import distribute_weight

_n = distribute_weight(3,4)
import ipdb; ipdb.set_trace()
