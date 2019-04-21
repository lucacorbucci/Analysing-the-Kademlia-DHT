# coding=utf-8

from KBucketList import kBucketList
from Node import *


class RoutingTable():
    """
    Classe che modella la routing table di un nodo della
    rete kademlia.

    Arguments:
        idLen: massima lunghezza in bit degli id dei nodi sdella rete
        bucketListLen: lunghezza di ogni k-bucket list dei nodi
        node: identificatore associato alla routing table
    """

    def __init__(self, idLen, bucketListLen, node):
        """
        Inizializzazione della routing table
        
        Arguments:
            idLen: il numero di bit di ogni identificatore
            bucketListLen: indica la lunghezza di ogni kBucketList
            node: il nodo associato a questa routing table
        """
        self.routingTable = [kBucketList(bucketListLen) for y in range(idLen)]
        self.node = node
        self.numContacts = 0

    def incrementNumContacts(self):
        """
        Aumenta il contatore dei contatti del nodo.
        """

        self.numContacts += 1

    def decrementNumContacts(self):
        """
        Decrementa il contatore dei contatti del nodo.
        """
        self.numContacts -= 1

    def printRoutingTable(self):
        print "numContacts: ", self.numContacts
        
        for kbucket in self.routingTable:
            if kbucket.isEmpty():
                print "---"
            else:
                kbucket.printKBucketList()
                print "****"


    def getRoutingTable(self, graph):
        nodes = []
        for kbucket in self.routingTable:

            nodes += kbucket.getMappedNodes(graph)
        return nodes
