import csv
import json
from itertools import groupby
from nesting import Nest

json_output = {}
as_details = {}

tiers = []
tiers_links = []
tiers_internal_links = []

""" DATA loading
"""
with open('input/tier1.txt') as tier1_data:
  tiers.append(set(tier1_data.read().split('\n')))

with open('input/links.csv') as links_data:
  reader = csv.reader(links_data, delimiter=' ')
  links = list(reader)

with open('input/as_details.json') as as_details_data:
  for d in json.load(as_details_data):
    as_details[d['AS_number']] = d

""" Compute the set of the AUTONOMOUS SYSTEM
"""
ASs = set()
for l in links:
  ASs.add(l[0])
  ASs.add(l[1])

LINKS_AMOUNT = len(links)
ASS_AMOUNT = len(ASs)

""" Check if TIER1 is a subset of 
"""
assert ASs.issuperset(tiers[0]), "Tier1 is not completely contained in topology."

""" Computing TIERS
"""
index = 0

# Loop until no links remains
while len(links) > 0:
  # If there at least a link, a new TIER is created
  tiers.append(set())

  # Link sets initialization
  tiers_links.append(0)
  tiers_internal_links.append(0)
  new_links = []

  # Loop over remaining links
  for line in links:
    # source is in current tier
    if line[0] in tiers[index]:
      # target not in current tier
      if line[1] not in tiers[index]:
        tiers[index+1].add(line[1])
        tiers_links[index] += 1
      # both source and target in current tier
      else:
        tiers_internal_links[index] += 1
    # target is in current tier
    elif line[1] in tiers[index]:
      # source not in current tier
      if line[0] not in tiers[index]:
        tiers[index+1].add(line[0])
        tiers_links[index] += 1
      # both source and target in current tier
      else:
        tiers_internal_links[index] += 1
    # link not involves current tier
    else:
      new_links.append(line)

  # Update link set with a new one containing only the remaining links
  links = new_links
  index += 1

""" Check if the amount of AUTONOMOUS SYSTEMS generated fits the initial set amount
"""
ass_count = reduce((lambda x, y: x + y), map(lambda x: len(x), tiers))
assert ASS_AMOUNT == ass_count, "Bad total amount of ASs."

""" Check if the amount of LINKS generated fits the initial set amount
"""
links_count = reduce((lambda x, y: x + y), tiers_links+tiers_internal_links)
assert LINKS_AMOUNT == links_count, "Bad total amount of links."

""" If INTERNAL LINKS remain in the last tier, a new EMPTY TIER will be appended to the tier list
"""
if len(tiers[-1]) == 0:
  tiers = tiers[:-1]


""" LOGGING STATISTICS
    Uncomment to log statistics. For each TIER the following values are printed:
    - number of autonomous systems it contains
    - number of links connect it to other tiers
    - number of internal links connecting the autonomous systems it contains
"""
# for (i,t) in enumerate(tiers):
#   print "\nTIER-" + str(i+1)
#   print "- AS AMOUNT: " + str(len(t))
#   if i < len(tiers_links):
#     print "- LINKS: " + str(tiers_links[i])
#     print "- INTERNAL LINKS: " + str(tiers_internal_links[i])
# print "\nTOTAL AMOUNT of LINKS: " + str(LINKS_AMOUNT)
# print "TOTAL AMOUNT of AUTONOMOUS SYSTEMS: " + str(ASS_AMOUNT) + "\n"
# exit()


""" COMPUTE OUTPUT DATA
"""

""" Transforms the nested namedtuple structure returned by the Nest()
    function to a JSON serializable form.
"""
def transform(data):
  new_data = []

  for d in data:
    if str(type(d)) == "<class 'nesting.Entry'>":
      new_data.append({
        "id": d.key,
        "children": transform(d.values)
      })
    else:
      new_data.append(d)

  return new_data

""" Computes the nesting of the data according to keys
    passed to the Nest() function.
"""
def nest(data):
  result = (Nest()
    .key('ipv')
    .key('rir')
    .entries(data))
  return transform(result)

""" Computes the final JSON structure
"""
json_output['children'] = map(
  lambda (i,t): {
    "id": "group"+str(i+1),
    "children": nest(
        map(
          lambda as_number: {
            "id": as_number,
            "label": as_details[as_number]['name'] if as_number in as_details else '',
            "group": i+1,
            "ipv": as_details[as_number]['IP_versions'] if as_number in as_details else '',
            "rir": as_details[as_number]['RIR'] if as_number in as_details else '',
          }, t)
        )
  }, enumerate(tiers))

print json.dumps(json_output)