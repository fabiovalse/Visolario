[Isolario](https://isolario.it/) is a project aimed to observe, collect and analyse real-time Internet routing data. The _Visolario_ project is a collaboration between Isolario and the WAFI research group of the Institute of Informatics and Telematics of the CNR in Pisa focused on finding visual representations suited for the visualization of the Autonomous System (AS) topology and the BGP routing data.

This repository documents how data coming from the [Isolario project](https://isolario.it/) has to be properly pre-processed in order to be visualized.

The [transform script](transform.py) takes as input three files:
- [tier1.txt](input/tier1.txt) contains the list of AS numbers belonging to the [Tier1](https://en.wikipedia.org/wiki/Tier_1_network);
- [links.csv](input/links.csv) defines relationships between ASes (file produced by Isolario);
- [as_details.json](input/as_details.json) contains all the information about ASes (file produced by Isolario).

Given the [links.csv file](input/links.csv) it is possible to create a graph where nodes are ASes and links the relationships between them. The transform scripts partions the graph according to the following procedure. The first partition _P1_ is given by the set of ASes belonging to the Tier1. _P2_ is computed starting from _P1_ and it contains all the nodes directly linked (i.e., connected with a path of one link) to the ones of _P1_. _Pn_ is computed starting from from _Pn-1_ and it contains all the nodes directly linked to the ones of _Pn-1_. This process is repetedly computed until no nodes remain.