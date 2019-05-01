# coding=utf-8
"""
    Classe main in cui troviamo la creazione del coordinatore e le varie richieste che vengono
    inviate al coordinatore per inserire i nodi nella rete. 
    A seconda del tipo di analisi che vogliamo effettuare verrà chiamata la funzione startAnalysis
    in modo differente.
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Coordinator import *
from Node import *
import binascii
from Map import *
import networkx as nx
import matplotlib.pyplot as plt
import Analysis as Analysis



def simpleGraph():
    """
        Simulazione più semplice, abbiamo un numero di nodi e li inseriamo tutti all'interno
        della rete creando poi il grafo e svolgendo le analisi sul grafo
    """

    # Per n-1 volte deve essere eseguita la fase di costruzione della routing table.
    for i in range(numNodes-1):
        # Generazione del nodo che vuole entrare nella rete
        joiningNode = coordinator.generateNode(idLen)      
        # Calcolo del nodo bootstrap
        bootstrapNode = coordinator.generateBootstrapNode()
        # Inserimento del nuovo nodo nella rete
        coordinator.join(joiningNode, bootstrapNode)

    createGraph(-1)

def temporalGraph():
    """
    Simulazione dell'inserimento dei nodi all'interno della rete. Vengono inseriti un numero di nodi 
    e poi si svolge l'analisi sul grafo parziale. In questo modo è possibile studiare l'evoluzione della
    rete e del grafo a mano a mano che vengono inseriti i nuovi nodi
    """
    nTime = numNodes / numSlot

    for n in range (0, numSlot):
        if(n==0):
            t = nTime -1
        else:
            t = nTime
        for i in range(t):
            # Generazione del nodo che vuole entrare nella rete
            joiningNode = coordinator.generateNode(idLen)      
            # Calcolo del nodo bootstrap
            bootstrapNode = coordinator.generateBootstrapNode()
            # Inserimento del nuovo nodo nella rete
            coordinator.join(joiningNode, bootstrapNode)

        createGraph(n)
    


def createGraph(index):
    """
    Creazione del grafo utilizzando i dati riguardanti gli archi che sono stati memorizzati nel file
    graph.txt. Se index è maggiore di 0 stiamo facendo un'analisi temporale e quindi passiamo l'indice 
    all'analisi per poter nominare i file che verranno creati.
    Se invece index<0 allora stiamo facendo un'analisi completa e non c'è bisogno di passare index al
    codice dell'analisi
    
    Arguments:
        index {int} -- Indica quale slot temporale stiamo analizzando
    """
    # Ogni id dei nodi presenti nel grafo viene mappato in un intero
    mapping = Map()
    global coordinator
    coordinator.getAllData(mapping)

    #Creazione del grafo prendendo gli archi dal file in cui li ho salvati
    graph = nx.DiGraph()
    with open('./results/graph.txt', 'r') as file:
        for line in file:
            arrayLine = line.strip('\n').split(" ")
            graph.add_edge(arrayLine[0], arrayLine[1])

    if(index >= 0):
        Analysis.startAnalysis(graph, index=index)
    else:
        Analysis.startAnalysis(graph)



def checkInput():
    """
    Controlliamo che vengano dati tutti i parametri necessari per l'esecuzione del codice e poi
    controlliamo che i parametri in input non siano minori di 0

    Returns:
        Boolean -- True se non ci sono errori, false altrimenti
    """
    global numNodes 
    global idLen 
    global maxBucketList
    global simple
    global numSlot 
    global mode


    if(len(sys.argv) < 5):
        print ('''Usage: python Main.py nodeNumber bitsOfTheIdentifier maxBucketList KBucketListManagment typeOfAnalysis numSlot
            nodeNumber: (Intero > 0) Numero di nodi che vogliamo inserire nella rete
            bitsOfTheIdentifier: (Intero > 0) lunghezza di ogni identificatore dei nodi 
            maxBucketList: (Intero > 0) lunghezza massima delle bucket List 
            KBucketListManagment (mode): Gestione della KBucketList, scrivere 1 per mantenere i nodi più vecchi e 0 per inserire i nuovi e 2 per una scelta random
            typeOfAnalysis: Tipo di analisi, scrivere 1 per l'analisi semplice e 0 per la temporale
            numSlot: (Intero > 0) specificare in quanti slot dividere i dati da inserire nella rete (scegliere un numero divisibile per nodeNumber)''')
    else:
        numNodes = int(sys.argv[1])
        idLen = int(sys.argv[2])
        maxBucketList = int(sys.argv[3])
        mode = int(sys.argv[4])

        if (int(sys.argv[5])==1):
            simple=True
        elif (int(sys.argv[5])==0):
            simple=False
        
        if(simple==False):
            numSlot = int(sys.argv[6])
            if(numSlot < 0):
                print "numSlot: input non valido"
    
        if(numNodes < 0 or idLen < 0 or maxBucketList < 0 or simple<0 or simple > 1 or mode < 0 or mode > 2):
            print "Input non valido"
            return False
        else:
            return True

########################################################################################
# MAIN:
# Qua Avviamo il coordinatore, l'inserimento dei nodi e l'analisi del grafo che viene generato
########################################################################################

numNodes = ""
idLen = ""
maxBucketList = ""
simple = ""
numSlot = ""
mode = ""

print idLen

if(checkInput()):
    if(numNodes > pow(2,idLen)):
        print "Lunghezza degli identificatori non sufficiente"
    else:
        # Creazione del coordinatore 
        coordinator = coordinator(numNodes, idLen, maxBucketList, mode)
        
        if(simple):
            simpleGraph()
        else:
            temporalGraph()
            

