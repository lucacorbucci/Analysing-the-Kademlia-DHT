# Analysing the Kademlia DHT

### Peer to Peer Systems and Blockchains Midterm
### Academic Year 2018-19

The mid term consists in a study of the Kademlia Distributed Hash Table. 
The first part of the assignment requires to write a simulation of the construction of the Kademlia routing tables.
The second part of the assignment requires to built a directed graph using the informations contained in the routing tables.
The last part of the assignment requires to study this graph.

The entire project is written in Python, you can try simulation using the following command:


```
python __init__.py 50 15 20 2 1
```

The first parameter is the number of the nodes that we want to insert in the network. The second parameter is the lenght
of the identifier of each node. The third parameter is the lenght of the KBucket List.
The other parameters are described in the final report.

The final report (written in italian) is [Here](https://github.com/lucacorbucci/Analysing-the-Kademlia-DHT/blob/master/Relazione/Relazione.pdf).

In the folder ./docs you can find the documentation of this project. I generate the documentation using pdoc and
i also wrote a [post](https://medium.com/@Tankado95/how-to-generate-a-documentation-for-python-code-using-pdoc-60f681d14d6e).
about this.
