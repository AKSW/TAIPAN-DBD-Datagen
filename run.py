# from opentablebench.DataGeneratorRunner import DataGeneratorRunner
#
# RUNNER = DataGeneratorRunner()
# RUNNER.run()

from opentablebench.NLTKInterface import cluster_header_random
from opentablebench.NLTKInterface import load_test_data
from opentablebench.NLTKInterface import \
    calculate_maximum_complexity_combinations, \
    calculate_maximum_complexity_naive

# print calculate_maximum_complexity_naive()
# print calculate_maximum_complexity_combinations()

headers = load_test_data()
print headers[0]
print cluster_header_random(headers[0])
