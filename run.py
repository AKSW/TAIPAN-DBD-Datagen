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
for i in range(0, 5):
    header = headers[i]
    print(header)
    print(verbalize_header_palmetto(header))

import ipdb; ipdb.set_trace()
