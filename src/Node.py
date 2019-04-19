# coding=utf-8

class Node():
    """
    Classe che modella il nodo presente all'interno della rete 
    di Kademlia.

    Arguments:
        id: id del nodo che viene creato
    """


    def __init__(self, id):
        self.id = id
    
    def printNode(self):
        """
            Stampa dell'id del nodo
        """
        print self.id

    def findNode(self,id):
        pass
    

