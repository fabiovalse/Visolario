import csv
import json
from nesting import Nest

class VisolarioData:
  as_details = {}
  partitions = []
  partitions_links = []
  partitions_internal_links = []

  def __init__(self, tier1_path, topology_path, as_details_path):
    self.tier1_path = tier1_path
    self.topology_path = topology_path
    self.as_details_path = as_details_path

    with open(self.tier1_path) as tier1_data:
      self.partitions.append(set(tier1_data.read().split('\n')))

    with open(self.topology_path) as links_data:
      reader = csv.reader(links_data, delimiter=' ')
      self.links = list(reader)

    with open(self.as_details_path) as as_details_data:
      for d in json.load(as_details_data):
        self.as_details[d['AS_number']] = d

    # Compute the set of Autonomous Systems (ASes)
    self.ASes = set()
    for l in self.links:
      self.ASes.add(l[0])
      self.ASes.add(l[1])

    global LINKS_AMOUNT
    global ASS_AMOUNT
    LINKS_AMOUNT = len(self.links)
    ASS_AMOUNT = len(self.ASes)

    self.check_tier1()    

  def check_tier1(self):
    """ Check if TIER1 is a subset of the set of all ASes.
    """
    assert self.ASes.issuperset(self.partitions[0]), "Tier1 is not completely contained in topology."

  def partition(self):
    """ Compute the graph partitioning and returns the list of partitions containing AS numbers.
    """
    # Computing partitions
    index = 0

    # Loop until no links remains
    while len(self.links) > 0:
      # If there at least a link, a new TIER is created
      self.partitions.append(set())

      # Link sets initialization
      self.partitions_links.append(0)
      self.partitions_internal_links.append(0)
      new_links = []

      # Loop over remaining links
      for line in self.links:
        # source is in current tier
        if line[0] in self.partitions[index]:
          # target not in current tier
          if line[1] not in self.partitions[index]:
            self.partitions[index+1].add(line[1])
            self.partitions_links[index] += 1
          # both source and target in current tier
          else:
            self.partitions_internal_links[index] += 1
        # target is in current tier
        elif line[1] in self.partitions[index]:
          # source not in current tier
          if line[0] not in self.partitions[index]:
            self.partitions[index+1].add(line[0])
            self.partitions_links[index] += 1
          # both source and target in current tier
          else:
            self.partitions_internal_links[index] += 1
        # link not involves current tier
        else:
          new_links.append(line)

      # Update link set with a new one containing only the remaining links
      self.links = new_links
      index += 1

    # Check if the amount of AUTONOMOUS SYSTEMS generated fits the initial set amount
    ass_count = reduce((lambda x, y: x + y), map(lambda x: len(x), self.partitions))
    assert ASS_AMOUNT == ass_count, "Bad total amount of ASs."

    # Check if the amount of LINKS generated fits the initial set amount
    links_count = reduce((lambda x, y: x + y), self.partitions_links+self.partitions_internal_links)
    assert LINKS_AMOUNT == links_count, "Bad total amount of links."

    # If INTERNAL LINKS remain in the last tier, a new EMPTY TIER will be appended to the tier list
    if len(self.partitions[-1]) == 0:
      self.partitions = self.partitions[:-1]
    
    return self.partitions

  def get_hierarchy(self, keys):
    """ Computes a hierarchical structure
    """
    json_output = {}

    json_output['children'] = map(
      lambda (i,t): {
        "id": "group"+str(i+1),
        "children": self.nest(
            map(
              lambda as_number: {
                "id": as_number,
                "label": self.as_details[as_number]['name'] if as_number in self.as_details else '',
                "group": i+1,
                "ipv": self.as_details[as_number]['IP_versions'] if as_number in self.as_details else '',
                "rir": self.as_details[as_number]['RIR'] if as_number in self.as_details else ''
              }, t),
            keys
          )
      }, enumerate(self.partitions))

    return json_output

  def nest(self, data, keys):
    """ Computes the nesting of the data according to keys passed to the Nest() function.
        The order of the keys is meaningful to define how the nesting process will group data.
    """
    nest = Nest()
    for k in keys:
      nest.key(k)
    result = nest.entries(data)

    return self.transform(result)

  def transform(self, data):
    """ Transforms the nested namedtuple structure returned by the Nest()
        function to a JSON structure.
    """
    new_data = []

    for d in data:
      if str(type(d)) == "<class 'nesting.Entry'>":
        new_data.append({
          "id": d.key,
          "children": self.transform(d.values)
        })
      else:
        new_data.append(d)

    return new_data