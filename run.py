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
from opentablebench.NLTKInterface import cluster_header
from opentablebench.NLTKInterface import load_test_data
headers = load_test_data()
header = headers[0]
print(header)
print(cluster_header(header))
