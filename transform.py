from VisolarioData import VisolarioData
import json

visolario = VisolarioData('input/tier1.txt', 'input/links.csv', 'input/as_details.json')
visolario.partition()
print json.dumps(visolario.get_hierarchy(['ipv', 'rir']))