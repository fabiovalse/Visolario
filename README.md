# Visolario

[Isolario](https://isolario.it/) is a project aimed to observe, collect and analyse real-time Internet routing data. The _Visolario_ project is a collaboration between Isolario and the WAFI research group of the Institute of Informatics and Telematics of the CNR in Pisa focused on finding visual representations suited for the visualization of the Autonomous System (AS) topology and the BGP routing data.

This repository documents how data coming from the [Isolario project](https://isolario.it/) has to be properly pre-processed in order to be visualized.


### VisolarioData

The [VisolarioData class](VisolarioData.py) allows to load, transform and analyse data coming from Isolario. To create a new instance:
```python
from VisolarioData import VisolarioData

visolario = VisolarioData(tier1, topology, as_details)
```
- *tier1* is a list of AS numbers;
- *topology* is a list of links expressed as lists containing first the source AS number and then the target AS number;
- *as_details* is a list of objects containing attributes about ASes such as AS number, regional Internet registry (RIR), name, IP versions and geolocation.

<a name="partition" href="#partition">#</a> __.partition()__\
Starting from the _topology_ input, it is possible to create a graph where nodes are ASes and links the relationships defined in _topology_. This method partitions the graph into _n_ groups _P<sub>1</sub>_, _P<sub>2</sub>_, ..., _P<sub>n</sub>_ according to the following procedure:
1. The first partition _P<sub>1</sub>_ is given by the set of ASes belonging to _tier1_;
2. _P<sub>2</sub>_ is computed starting from _P<sub>1</sub>_ and it is composed by the nodes directly linked to the ones contained in _P<sub>1</sub>_;
3. _P<sub>n</sub>_ is computed starting from _P<sub>n-1</sub>_ and it is composed by the nodes directly linked to the ones contained in _P<sub>n-1</sub>_. This step is iteratively computed until no nodes remain.

<a name="get_hierarchy" href="#get_hierarchy">#</a> __.get_hierarchy(keys)__\
The partitions created with the _.partition()_ method can be hierarchically structured using *get_hierarchy()*. The _keys_ input (a list of strings) defines which attributes (contained in *as_details*) will be used for grouping ASes. For instance, the IP version or the RIR can be used to this aim.
```python
visolario = VisolarioData(tier1, topology, as_details)
visolario.partition()
hierarchy = visolario.get_hierarchy(['ipv', 'rir'])
```
The method returns a tree where each partition is hierarchically structured according to the input _keys_. This method uses a D3.js porting of d3.nest called [nesting 0.1.0](https://pypi.python.org/pypi/nesting/0.1.0).

By printing the hierarchy it is possible to obtain a structure like:
```
{
  "children": [
    {
      "id": "group1",
      "children": [
        {
          "id": "v4",
          "children": [
            {
              "id": "ARIN",
              "children": [
                {
                  "ipv": "v4",
                  "rir": "ARIN",
                  "group": 1,
                  "id": "1",
                  "label": "LVLT-1 - Level 3 Communications, Inc."
                },
                ...
              ]
            },
            {
              "id": "RIPE NCC",
              "children": [...]
            },
            ...
          ]
        },
        {
          "id": "v4+v6",
          "children": [...]
        },
        {
          "id": "v6",
          "children": [...]
        }
      ]
    },
    ...
    {
      "id": "groupn",
      "children": [...]
    }
  ...
  ]
}
```

### transform.py
The [transform script](transform.py) is an example of how VisolarioData can be used. It loads three files:
- [tier1.txt](input/tier1.txt) contains the list of AS numbers belonging to the [Tier1](https://en.wikipedia.org/wiki/Tier_1_network);
- [links.csv](input/links.csv) defines relationships between ASes (file produced by Isolario);
- [as_details.json](input/as_details.json) contains all the information about ASes (file produced by Isolario).