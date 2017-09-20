# Visolario

[Isolario](https://isolario.it/) is a project aimed to observe, collect and analyse real-time Internet routing data. The _Visolario_ project is a collaboration between Isolario and the WAFI research group of the Institute of Informatics and Telematics of the CNR in Pisa focused on finding visual representations suited for the visualization of the Autonomous System (AS) topology and the BGP routing data.

This repository documents how data coming from the [Isolario project](https://isolario.it/) has to be properly pre-processed in order to be visualized.


### Transform.py

#### Input
The [transform script](transform.py) takes as input three files:
- [tier1.txt](input/tier1.txt) contains the list of AS numbers belonging to the [Tier1](https://en.wikipedia.org/wiki/Tier_1_network);
- [links.csv](input/links.csv) defines relationships between ASes (file produced by Isolario);
- [as_details.json](input/as_details.json) contains all the information about ASes (file produced by Isolario).

#### Graph partitioning
Starting from [links.csv](input/links.csv), it is possible to create a graph where nodes are ASes while links the relationships between them.

The script partitions the graph _G_ into _n_ groups _P<sub>1</sub>_, _P<sub>2</sub>_, ..., _P<sub>n</sub>_ according to the following procedure:
1. The first partition _P<sub>1</sub>_ is given by the set of ASes belonging to the Tier1;
2. _P<sub>2</sub>_ is computed starting from _P<sub>1</sub>_ and it is given by the nodes directly linked (i.e., connected with a path of one link) to the ones contained in _P<sub>1</sub>_;
3. _P<sub>n</sub>_ is computed starting from from _P<sub>n-1</sub>_ and it is given by the nodes directly linked to the ones contained inf _P<sub>n-1</sub>_;
4. This process is repetedly computed until no nodes remain.

#### Hierarchy
Partitions are hierarchically structured using the Python [nesting package](https://pypi.python.org/pypi/nesting/0.1.0). The ASes of each partitions are grouped into a hierarchically tree structure defined using AS attributes. For instance, the IP version or the regional Internet registry (RIR) can be used to this aim.

#### Output
The script prints on the standard output the hierarchy as a JSON file. A possible output is structured as follows:
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