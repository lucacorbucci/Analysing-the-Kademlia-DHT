# coding=utf-8
"""
    Main Class
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from Coordinator import *
from Node import *
import binascii

if(len(sys.argv) < 3):
    print "Usage: python Main.py nodeNumber bitsOfTheIdentifier"
else:
    numNodes = int(sys.argv[1])
    idLen = int(sys.argv[2])
    
    # Creazione del coordinatore 
    coordinator = coordinator(numNodes, idLen)
    


    # Per n-1 volte deve essere eseguita la fase di costruzione della
    # routing table.
    for i in range(numNodes-1):
        # Generazione del nodo che vuole entrare nella rete
        joiningNode = coordinator.generateNode(idLen)      
        # Calcolo del nodo bootstrap
        bootstrapNode = coordinator.generateBootstrapNode()
        print "bootstrap", bootstrapNode.id
        # Inserimento del nuovo nodo nella rete
        coordinator.join(joiningNode, bootstrapNode)
        #print "bootstrap Node: ", bootstrapNode.id
        #print "joining Node: ", joiningNode.id
    coordinator.debug()
    
