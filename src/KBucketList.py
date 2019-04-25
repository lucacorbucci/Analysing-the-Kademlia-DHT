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
        Ci sono due possibilità, se mode=1 allora vuol dire che quando inserisco un nuovo nodo
        devo controllare se la k-bucket list è piena, in quel caso non aggiungo il nuovo nodo.
        Se invece mode=0 allora, se la k-bucket list è piena tolgo il primo nodo della lista (che sarebbe il più vecchio)
        e aggiungo in fondo alla coda il nuovo nodo.
        Se c'è spazio nella coda aggiungo il nodo in fondo alla lista in entrambi i casi.
        
        Arguments:
            node: Nodo da inserire nella k bucket list
        Returns:
            [Int] -- 1 se ho effettuato un inserimento nella lista e se aumento anche il numero di nodi
            che sono contenuti all'interno della lista.
            0 se inserisco il nuovo nodo nela lista sostituendo il vecchio, quindi non devo aumentare il numero 
            di nodi che sono presenti nella lista.
            -1 se non inserisco il nodo nella lista.
        """

        # Caso in cui mantengo i più vecchi nella KBucket List
        if(self.mode == 1):
            if(node not in self.array and self.length < self.maxLength):
                self.array.append(node)
                self.length+=1
                return 1
            else:
                return -1
        else:
            if(node not in self.array and self.length < self.maxLength):
                self.array.append(node)
                self.length+=1
                return 1
            elif (node not in self.array and self.length == self.maxLength):
                x = self.array.pop(0)
                
                self.array.append(node)
                return 0
            else:
                return -1

    
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
