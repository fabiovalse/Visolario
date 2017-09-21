from VisolarioData import VisolarioData
import csv
import json
import glob

as_details = {}
statistics = []

# Loading TIER 1
with open('input/tier1.txt') as tier1_data:
  tier1 = set(tier1_data.read().split('\n'))

# Loading Autonomous System details
with open('input/as_details.json') as as_details_data:
  for d in json.load(as_details_data):
    as_details[d['AS_number']] = d

# Get topology file paths
topology_files = glob.glob("./input/six_months_topologies/*")

# Loop over topology files
for topology_file in topology_files:
  print topology_file

  # Loading topology file
  with open(topology_file) as links_data:
    reader = csv.reader(links_data, delimiter=' ')
    topology = list(reader)

  if len(topology) > 0:
    # Create a VisolarioData instance
    visolario = VisolarioData(tier1, topology, as_details)
    
    # Partition data
    visolario.partition()
    
    # Log statistics about partitions
    s = visolario.get_statistics()
    s['date'] = topology_file.split('/')[-1]
    statistics.append(s)
  else:
    statistics.append({
      "date": topology_file.split('/')[-1],
      "empty": True
    })

print json.dumps(statistics)