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
    print "Usage: python Main.py nodeNumber bitsOfTheIdentifier maxBucketList"
else:
    numNodes = int(sys.argv[1])
    idLen = int(sys.argv[2])
    maxBucketList = 20
    if(len(sys.argv) > 3):
        maxBucketList = int(sys.argv[3])
    
    if(numNodes > pow(2,idLen)):
        print "Lunghezza degli identificatori non sufficiente"
    else:
        # Creazione del coordinatore 
        coordinator = coordinator(numNodes, idLen, maxBucketList)
        

        
        # Per n-1 volte deve essere eseguita la fase di costruzione della
        # routing table.
        for i in range(numNodes-1):
            # Generazione del nodo che vuole entrare nella rete
            joiningNode = coordinator.generateNode(idLen)      
            # Calcolo del nodo bootstrap
            bootstrapNode = coordinator.generateBootstrapNode()
            #print ""
            #print "joininig: ", joiningNode.id
            #print "bootstrap", bootstrapNode.id
            # Inserimento del nuovo nodo nella rete
            coordinator.join(joiningNode, bootstrapNode)
            #print "bootstrap Node: ", bootstrapNode.id
            #print "joining Node: ", joiningNode.id
        coordinator.debug()
    
