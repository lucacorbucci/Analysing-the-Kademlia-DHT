# coding=utf-8

from RoutingTable import *
from Node import *
import random
from random import choice
from Crypto.Hash import SHAKE256
from binascii import hexlify
from random import choice
from Exceptions import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class coordinator():

    """
    Coordinatore che si occupa di gestire la rete di Kademlia.

    La classe coordinatore gestisce l'arrivo di nuovi nodi nella rete
    e memorizza le routing table di tutti i nodi che fanno parte della rete.    

    Attributes:
        numNodes: numero di nodi che faranno parte della rete
        idLen: lunghezza dell'id di ognuno dei nodi
    """

    def __init__(self, numNodes, idLen):
        """
        Init della classe Coordinator.

        Quando viene creato il coordinato crea un primo nodo che prende un ID generato random
        e poi questo primo nodo viene inserito all'interno della struttura dati.

        La struttura che contiene i dati che riguardano i nodi nella rete è un dizionario <key, value>
        key lo assegnamo quando aggiungiamo il nodo nella rete, value è la routing table del nodo.
        In questo modo possiamo accedere velocemente alla routing table di un nodo.
        
        Arguments:
            numNodes: numero di nodi che faranno parte della rete
            idLen: lunghezza dell'id di ognuno dei nodi
        
        """
        self.savedNodes = 0
        self.structure = {}
        self.numNodes = numNodes
        self.id = {}
        self.idLen = idLen

        # Generazione del primo nodo che entra nella rete
        firstNode = Node(self.generateId(idLen))
        try:
            self.addNodeInStructure(firstNode.id, firstNode)
        except duplicateNode:
            print "Impossibile inserire il nodo nella rete. ID già presente"
        
    
    def addNodeInStructure(self, ID, node):
        """
        Inserimento di un nuovo nodo all'interno della struttura del coordinatore
        
        Arguments:
            node: il nodo da inserire all'interno della struttura
        """
        if(not self.structure.has_key(ID)):
            self.structure[ID] = RoutingTable(self.idLen, 20, node)
            self.savedNodes += 1
        else:   
            raise duplicateNode

    
    def generateBootstrapNode(self):
        """ 
        Generazione del nodo bootstrap, viene preso random un nodo che è 
        già presente all'interno della rete

        Returns:   
            l'identificatore del nodo bootstrap
        """
        if(self.savedNodes > 0):
            id = random.choice(list(self.structure.items()))
            return self.structure[id[0]].node

    
    def generateNode(self, len):
        """
        Generazione di un nuovo nodo con il suo id
        
        Arguments:
            len: lunghezza dell'id del nodo

        Returns:
            Il nuovo nodo che è stato creato
        """
        # TODO
        # if(Ho finito i possibili identificatori)
        
        id = self.generateId(len)
        
        return Node(id)
        
    
    def join(self, joiningNode, bootstrapNode):
        """
        Inserimento di un nuovo nodo nella rete.

        IL nuovo nodo invia findNode() al bootstrap node, questo poi restituisce
        una sequenza di K nodi che sono più vicini al nuovo nodo della rete che 
        va poi a contattare questi k nodi per farsi conoscere.
        La routing table viene popolata a mano a mano che vengono fatte
        le chiamate a findNode()

        Arguments:
            JoiningNode: nodo che deve entrare nella rete
            boostrapNode: nodo bootstrap
        
        """
        print joiningNode.id
        position = self.findNode(joiningNode, bootstrapNode)
        routingTable = self.structure[joiningNode.id].routingTable
        res = []
        for i in range(0,self.idLen):
            randomID = self.generateBucketID(i)
            res += self.lookup(bootstrapNode, randomID)
            print "reee" , res
        results = set(res)
        if(joiningNode.id in res):
            results.remove(joiningNode.id)
        for id in results:
            node = self.structure[id].node
            position = self.computeDistance(joiningNode.id, id, True)
            if (self.structure[joiningNode.id].routingTable[position].insert(node)):
                (self.structure[joiningNode.id]).incrementNumContacts()

        print "primo", results

        z = set(results)
        for nodes in z:
            destNode = self.structure[nodes].node
            self.findNode(joiningNode, destNode)
            tmp = self.lookup(destNode, randomID)
            z.union(set(tmp))

        for id in z:
            if(id != joiningNode.id):
                node = self.structure[id].node
                position = self.computeDistance(joiningNode.id, id, True)
                if (routingTable[position].insert(node)):
                    (self.structure[joiningNode.id]).incrementNumContacts()

        '''
        # Fino a che non trovo o che ho visto tutti i nodi del bucket considerato 
        # oppure che ho riempito il bucket devo fare delle lookup verso quel nodo 
        # e memorizzo un set di dati di nodi che poi inserisco nella mia routing table
        # Però devo tenere per ogni lookup che faccio solamente i migliori k  
        res = []
        final = []
        for i in range(0,self.idLen):
            if(not routingTable[i].isEmpty() and not routingTable[i].isFull()):
                # prendo i nodi che stanno in quella routing table e genero un id random nel bucket i
                nodes = set(routingTable[i].getNodes())
                randomID = self.generateBucketID(i)
                for idNode in nodes:
                    res = []
                    destNode = self.structure[idNode].node
                    self.findNode(joiningNode, destNode)
                    res += self.lookup(destNode, randomID)
                    final += res
                    nodes = nodes.union(set(res))
                   
        
        for id in final:
            if(id != joiningNode.id):
                node = self.structure[id].node
                position = self.computeDistance(joiningNode.id, id, True)
                if (routingTable[position].insert(node)):
                    (self.structure[joiningNode.id]).incrementNumContacts()
        '''
        




    def lookup(self, node, randomID):
        print "lookup"
        bucketPosition = self.computeDistance(randomID, node.id, True)
        routingTable = self.structure[node.id].routingTable
        array = []
        if (not routingTable[bucketPosition].isEmpty()):
            array = routingTable[bucketPosition].getNodes()
            print "array: ", array
        if(len(array)==20):
            return array
        else:
            i = bucketPosition-1
            j = bucketPosition+1
            while((i>=0 or j<self.idLen) and len(array)<20 ):
                print i,j,bucketPosition
                if(i>=0 and len(array)<20):
                    print routingTable[i].getNodes()
                    if (not routingTable[i].isEmpty()):
                        array += routingTable[i].getNodes()
                    i -= 1
                if(j < self.idLen and len(array)<20):
                    if (not routingTable[j].isEmpty()):
                        array += routingTable[j].getNodes()
                    j += 1

        return array
            

    def findNode(self, joiningNode, bootstrapNode):
        """
        Viene calcolata la posizione del nuovo nodo all'interno della routing
        table del nodo bootstrap (e viceversa). Inseriamo il nodo boostrap 
        all'interno della routing table del joiningNode (e viceversa).
        Poi vengono cercati i K nodi che sono più vicini al joiningNode.
        
        Arguments:
            joiningNode: nodo che vuole entrare nella rete
            bootstrapNode: nodo bootstrap
        
        Returns:
            la posizione del joiningNode nella routing table di Bootstrap Node
        """ 
        
        position = self.computeDistance(joiningNode.id,bootstrapNode.id, True)
        #print len(self.structure[bootstrapNode].routingTable)
        #print position
        if(self.structure[bootstrapNode.id].routingTable[position].insert(joiningNode)):
            (self.structure[bootstrapNode.id]).incrementNumContacts()
        if(not self.structure.has_key(joiningNode.id)):
            self.addNodeInStructure(joiningNode.id, joiningNode)

        if(self.structure[joiningNode.id].routingTable[position].insert(bootstrapNode)):
            (self.structure[joiningNode.id]).incrementNumContacts()

        return position

        

    def computeDistance(self, id1, id2, simple):
        """
        Calcolo della distanza tra due id 
        
        Arguments:
            id1: id del primo nodo
            id2: id del secondo nodo
        
        Returns:
            La distanza tra i due id. As esempio se lo xor tra i due
            id è 00010110 allora viene restituito 4 (posizione del primo 1s) che sarà
            la posizione dell'id all'interno della routing table.
        """
        if(simple):
            for i in range (0,len(id1)):
                if((int(id1[i],2) ^ int(id2[i],2))==1):
                    break

            return len(id1)-i-1
           
        else:
            pass

    
    def generateId(self, len):
        """
        Generazione dell'id di un nuovo nodo che entra nella rete.
        Viene generata una sequenza di bit di lunghezza len e si controlla che 
        l'id generato non sia stato già precedentemente assegnato
        
        Arguments:
            len: lunghezza dell'id del nodo
        
        Returns:
            id del nodo
        """
        bitID = ''.join(choice(['0', '1']) for _ in xrange(len))
        while(self.id.has_key(bitID)):
            bitID = ''.join(choice(['0', '1']) for _ in xrange(len))
        self.id[bitID] = ""
        return bitID
    
    def generateBucketID(self, i):
        """
        Generazione dell'id di un nodo che appartiene al bucket i 
        della routing table.
        Viene generato un id che ha almeno un 1 in posizione i,
        i successivi bit sono scelti random.
        Nel caso di i=0 si considera solamente il primo bit della sequenza
        che quindi sarà 0 o 1, poi il resto saranno tutti 0.
        
        Arguments:
            i: posizione del bucket all'interno della routing table
        
        Returns:
            id generato random e appartenente al bucket is
        """
        if(i==0):
            bitID = ''.join(choice(['0', '1']) for _ in xrange(i+1))
        else:
            bitID = ''.join(choice(['0', '1']) for _ in xrange(i))
            bitID = "1" + bitID
        
        randomID = bitID.zfill(self.idLen)
        
        return randomID
      
    
    def debug(self):
        """
        Funzione di debug usata per la stampa delle routing table
        """

        print ""
        print ""
        print ""
        for key, value in self.structure.iteritems():
            print "ID", key 
            print value.printRoutingTable()

