from VisolarioData import VisolarioData
import json

as_details = {}

# Loading TIER 1
with open('input/tier1.txt') as tier1_data:
  tier1 = set(tier1_data.read().split('\n'))

# Loading Autonomous System details
with open('input/as_details.json') as as_details_data:
  for d in json.load(as_details_data):
    as_details[d['AS_number']] = d

# Loading topology file
  with open('input/links.csv') as links_data:
    reader = csv.reader(links_data, delimiter=' ')
    topology = list(reader)

# Create a VisolarioData instance
visolario = VisolarioData(tier1, topology, as_details)

# Partition data
visolario.partition()

# Hierarchically structure data
print json.dumps(visolario.get_hierarchy(['ipv', 'rir']))