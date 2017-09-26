from VisolarioData import VisolarioData
import csv
import json

as_details = {}

# Loading TIER 1
with open('input/tier1.txt') as tier1_data:
  tier1 = set(tier1_data.read().split('\n'))

# Loading Autonomous System details
with open('input/as_details.json') as as_details_data:
  for d in json.load(as_details_data):
    # Derive geolocation as the concatenation of country ISO codes
    if len(d['geolocation']) == 0:
      d['geo'] = ""
    else:
      d['geo'] = reduce(
        (lambda x, y: x + "|" + y),
        map(lambda x: x['code'], sorted(d['geolocation'], key=lambda x: x['code']))
      )
    # Remove useless data
    d.pop('subnets_announced', None)
    # Add AS to index
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
print json.dumps(visolario.get_hierarchy(['ipv', 'rir', 'geo']))