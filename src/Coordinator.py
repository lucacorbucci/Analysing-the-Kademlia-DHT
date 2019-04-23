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

    def __init__(self, numNodes, idLen, maxBucketList, mode):
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
            maxBucketList: lunghezza massima dei bucketList
            mode: gestione della KBucket List, se è 1 mantengo i più vecchi, se è 0 mantengo i più recenti
        """
        self.savedNodes = 0
        self.structure = {}
        self.numNodes = numNodes
        self.id = {}
        self.idLen = idLen
        self.maxBucketList = maxBucketList
        self.mode = mode

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
            self.structure[ID] = RoutingTable(self.idLen, self.maxBucketList, node, self.mode)
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

        #---- Prima parte: contatto il bootstrap
        
        position = self.findNode(joiningNode, bootstrapNode)
        routingTable = self.structure[joiningNode.id].routingTable
        res = []
        # Viene fatta una lookup per un id random verso il bootstrap node per ogni
        # bucket della routing table del joining node
        for i in range(0,self.idLen):
            randomID = self.generateBucketID(i)
            res += self.lookup(bootstrapNode, randomID)

        #Eliminiamo eventuali duplicati
        results = set(res)
        # Nei risultati della lookup non va considerato il joiningNode
        if(joiningNode.id in res):
            results.remove(joiningNode.id)

        # Inseriamo i nodi che arrivano dalla prima lookup all'interno della 
        # routing table del joiningNode    
        for id in results:
            self.addNodeInRoutingTable(id, joiningNode)

        #----Seconda Parte: contatto i nodi che mi ha mandato il bootstrap
        
        for i in range(0,self.idLen):
            # Consideriamo i bucket della routing table che non sono vuoti e che non 
            # hanno già il numero massimo di nodi all'interno
            if(not routingTable[i].isEmpty()):
                # prendo i nodi che stanno in quella routing table e genero un id random nel bucket i
                nodes = set(routingTable[i].getNodes())
                allNodes = nodes
                randomID = self.generateBucketID(i)
                res = []
                
                # Fino a che ho dei nodi da visitare nel bucket i prendo il primo nodo della coda
                # poi gli mando un findNode e poi faccio una lookup verso quel nodo mandando un id
                # random presente in quel bucket.
                while(len(nodes) > 0 and not routingTable[i].isFull()):
                    idNode = nodes.pop()
                    destNode = self.structure[idNode].node
                    self.findNode(joiningNode, destNode)
                    res += self.lookup(destNode, randomID)
                    

                    resSet = set(res)
                    if(joiningNode.id in res):
                        resSet.remove(joiningNode.id)
                    
                    # Quando ho i nodi restituiti dalla lookup li inserisco nella routing table
                    # e se finiscono nel bucket i devo inserirli anche nalla coda nodes
                    # in modo che posso contattarli di nuovo
                    for id in resSet:
                        self.addNodeInRoutingTable(id, joiningNode)
                        if(position <= i and id not in allNodes):
                            nodes.union(id)
                    allNodes = allNodes.union(set(res))
                

    def addNodeInRoutingTable(self, id, joiningNode):
        """
        Dobbiamo calcolare la posizione di id rispetto al joiningNode poi inseriamo all'interno della struttura
        di joiningNode il nodo che ha id come identificatore.
        
        Arguments:
            id: id del nodo che deve essere inserito all'interno della routing Table di joiningNode
            joiningNode: nodo che entra nella rete
        """
        joiningStructure = self.structure[joiningNode.id]
        node = self.structure[id].node
        position = self.computeDistance(joiningNode.id, id, True)
        if (joiningStructure.routingTable[position].insert(node)):
            (joiningStructure).incrementNumContacts()


    def lookup(self, node, randomID):
        """
        Viene calcolata la distanza tra il randomID e il nodo a cui viene inviata la lookup.
        Poi si prende il bucket dove si troverebbe il randomID e prendiamo i nodi che stanno in quel
        bucket, se poi non sono abbastanza allora ci spostiamo anche nei bucket vicini e prendiamo nodi fino
        a che non arriviamo al numero massimo che può essere restituito.
        
        Arguments:
            node: nodo destinatario della lookup
            randomID: ID random preso in un bucket della routing table del joining Node
        
        Returns:
            Array con i nodi che sono vicini a RandomID
        """
        bucketPosition = self.computeDistance(randomID, node.id, True)
        routingTable = self.structure[node.id].routingTable
        array = []
        if (not routingTable[bucketPosition].isEmpty()):
            array = routingTable[bucketPosition].getNodes()
        if(len(array)==self.maxBucketList):
            return array
        else:
            i = bucketPosition-1
            j = bucketPosition+1
            while((i>=0 or j<self.idLen) and len(array)<self.maxBucketList):
                if(i>=0 and len(array)<self.maxBucketList):
                    if (not routingTable[i].isEmpty()):
                        array += routingTable[i].getNodes()
                    i -= 1
                if(j < self.idLen and len(array)<self.maxBucketList):
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
      
    def getAllData(self, mappa):
        """
        Vengono generate le coppie id-id dove il primo è il nodo sorgente e il secondo
        è il nodo destinazione di un arco del grafo.
        Questi archi vengono memorizzati nel file graph.txt e possono essere anche restituiti in un dizionario
        che sarà nel formato:
        {id1:[1,2,3], id2:[4,6,7]}

        Arguments:
            graph {Map} -- mappa che utilizziamo per mappare gli ID dei nodi a degli interi
        
        Returns:
            Dictionary -- Dizionario che contiene gli archi del grafo
        """
        data = {}
        id = ""
        with open('./results/graph.txt', 'w') as writer:
    
            for key, value in self.structure.iteritems():
                if(mappa.mapID.has_key(key)):
                    id = mappa.mapID[key]
                else:
                    id = mappa.getCounter()
                    mappa.incrementCounter()
                    mappa.mapID[key] = id
                    
                contacts = value.getRoutingTable(mappa)
                data[id] = contacts
                for c in contacts:
                    writer.write(str(id) + " " + str(c) + "\n")
        return data
    
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

