from VisolarioData import VisolarioData
import csv
import json
import glob
import datetime

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
topology_files = glob.glob("./input/stability_analysis/*")

# Order files by date
topology_files = sorted(
  map((lambda x: {"path": x, "date": x.split('/')[-1][:-4]}), topology_files),
  key=lambda x: datetime.datetime.strptime(x['date'], '%Y_%m_%d')
)

# Load current topology file
with open(topology_files[0]['path']) as links_data:
  reader = csv.reader(links_data, delimiter=' ')
  current_topology = list(reader)
  
  # Compute current day data
  current_day = VisolarioData(tier1, current_topology, as_details)
  current_partitions = current_day.partition()

next_partitions = []

# Loop over topology files
for (i, topology_file) in enumerate(topology_files[1:]):
  # Loading next topology file
  with open(topology_file['path']) as links_data:
    reader = csv.reader(links_data, delimiter=' ')
    next_topology = list(reader)

  # Avoid empty files
  if len(current_topology) > 0 and len(next_topology) > 0:  
    
    # Compute next day data
    next_day = VisolarioData(tier1, next_topology, as_details)
    next_partitions = next_day.partition()

    # Statistics about current topology
    s = current_day.get_statistics()
    
    # Add a date attribute
    s['date'] = topology_files[i]['date']
    
    # Compute the AS flows from the current partitions to the ones of the next day
    for (i,p) in enumerate(s['partitions']):
      p['flows'] = [len(current_partitions[i] & n) for n in next_partitions]

    print s
    print ""

    statistics.append(s)
  else:
    statistics.append({
      "date": topology_files[i]['date'],
      "empty": True
    })
  
  # Update current partitions
  current_day = next_day
  current_partitions = next_partitions

print json.dumps(statistics)