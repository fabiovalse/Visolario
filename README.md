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

The script partitions the graph _G_ into _n_ groups _P1_, _P2_, ..., _Pn_ according to the following procedure:
1. The first partition _P1_ is given by the set of ASes belonging to the Tier1;
2. _P2_ is computed starting from _P1_ and it is given by the nodes directly linked (i.e., connected with a path of one link) to the ones contained in _P1_;
3. _Pn_ is computed starting from from _Pn-1_ and it is given by the nodes directly linked to the ones contained inf _Pn-1_.
4. This process is repetedly computed until no nodes remain.
