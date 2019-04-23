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


    def __init__(self, k, mode):
        self.length = 0
        self.maxLength = k
        self.array = []
        # Mode è 1 se voglio mantenere sempre quelli che ho messo prima
        # Vale 0 se invece voglio mettere nella KBucket List i più recenti quando è piena
        self.mode = mode

    
    def insert(self, node):
        """
        Inserimento all'interno della k Bucket List.
        Se la lista è piena controllo se il primo nodo è ancora attivo, se è attivo scarto il nuovo
        e sposto la testa in coda alla lista. Se non è più attivo elimino la testa 
        e metto in coda il nuovo nodo.
        
        Arguments:
            node: Nodo da inserire nella k bucket list
        """

        # Caso in cui mantengo i più vecchi nella KBucket List
        if(self.mode == 1):
            if(node not in self.array and self.length < self.maxLength):
                self.array.append(node)
                self.length+=1
                return True
            else:
                return False
        else:
            # Caso in cui metto i nuovi nella KBucketList
            if(node not in self.array and self.length < self.maxLength):
                self.array.append(node)
                self.length+=1
                return True
            elif (node not in self.array and self.length == self.maxLength):
                self.array.pop(0)
                self.array.append(node)
                return True
            else:
                return False

    
    def getNodes(self):
        """
        Funzione che restituisce i nodi presenti all'interno di una KBucket List
        
        Returns:
            [Array] -- Array con gli id dei nodi della K-Bucket List
        """
        tmp = []
        for nodes in self.array:
            tmp.append(nodes.id)
        return tmp


    def getMappedNodes(self, mappa):
        """
        Vengono restituiti i nodi che sono all'interno della KBucket List mappati 
        in un intero.
        
        Arguments:
            mappa {Map} -- mappa id-intero
        
        Returns:
            Array -- Array con i nodi rimappati in interi
        """
        tmp = []
        for nodes in self.array:
            if(mappa.mapID.has_key(nodes.id)):
                tmp.append(mappa.mapID[nodes.id])
            else:
                id = mappa.getCounter()
                mappa.incrementCounter()
                mappa.mapID[nodes.id] = id
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
            Boolean -- true se la lista è piena, false altrimenti
        """
        return True if (self.maxLength == self.length) else False

    def isEmpty(self):
        """
        Controlla se la coda è vuota o no.

        Returns:
            Boolean -- True se la lista è vuota, False altrimenti
        """
        
        return True if (self.length == 0) else False
