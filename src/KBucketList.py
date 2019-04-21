# coding=utf-8

class kBucketList():
    """
    Classe che descrive la K-Bucket list.
    La k-Bucket list è un array con una dimensione massima,
    ogni nuovo elemento viene inserito alla fine e se la lista è piena 
    si controlla se il primo elemento della lista è ancora attivo o no.
    Se non è attivo lo tolgo e metto il nuovo elemento, altrimenti sposto 
    il primo elemento della lista alla fine.

    Attributes:
        k = dimensione massima della k-bucket list
    """


    def __init__(self, k):
        self.length = 0
        self.maxLength = k
        self.array = []

    
    def insert(self, node):
        """
        Inserimento all'interno della k Bucket List.
        Se la lista è piena controllo se il primo nodo è ancora attivo, se è attivo scarto il nuovo
        e sposto la testa in coda alla lista. Se non è più attivo elimino la testa 
        e metto in coda il nuovo nodo.
        
        Arguments:
            node: Nodo da inserire nella k bucket list
        """


        if(node not in self.array and self.length < self.maxLength):
            self.array.append(node)
            self.length+=1
            return True
        else:
            return False
    
    def getNodes(self):
        tmp = []
        for nodes in self.array:
            tmp.append(nodes.id)
        return tmp


    def getMappedNodes(self, graph):
        tmp = []
        for nodes in self.array:
            if(graph.mapID.has_key(nodes.id)):
                tmp.append(graph.mapID[nodes.id])
            else:
                id = graph.getCounter()
                graph.incrementCounter()
                graph.mapID[nodes.id] = id
                tmp.append(id)
        return tmp

    def printKBucketList(self):
        """
        Funzione di debug per la stampa della bucket list
        """
        print len(self.array)
        for node in self.array:
            print "@@@@@@@@", node.id

        

    def isFull(self):
        """
        Controlla se la coda è piena o no
        
        Returns:
            Boolean: true se la lista è piena, false altrimenti
        """
        return True if (self.maxLength == self.length) else False

    def isEmpty(self):
        """
        Controlla se la coda è vuota o no.
        Returns:
            Boolean: true se la lista è vuota, false altrimenti
        """
        
        return True if (self.length == 0) else False
