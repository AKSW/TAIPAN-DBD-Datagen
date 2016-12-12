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
from opentablebench.NLTKInterface import verbalize_header_palmetto
#from opentablebench.NLTKInterface import verbalize_header_random
#from opentablebench.NLTKInterface import verbalize_header_naive
from opentablebench.NLTKInterface import load_test_data
headers = load_test_data()
#for i, header in enumerate(headers):
#    if i < 1:
#        continue
#    print(i)
#    print(header)
#    print(verbalize_header_palmetto(header))
#    print("")

from opentablebench.TreeWalker import distribute_weight_recursive
for l in distribute_weight_recursive(64,15):
    pass

#import ipdb; ipdb.set_trace()
