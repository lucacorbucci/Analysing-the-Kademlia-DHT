# coding=utf-8
"""
    Codice per avviare le analisi del grafo
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
import pandas as pd


def startAnalysis(graph, index = -1):
    """
    Qua viene passato il grafo su cui deve essere svolta l'analisi, vengono svolte due tipi di analisi, quella sul grafo 
    completo e qualla sugli snapshot.
    Sugli snapshot:
        - Numero di nodi
        - Numero di archi
        - Numero delle componenti connesse
        - Numero delle strongly connected component
        - Diametro del grafo
        - Lunghezza media dei cammini minimi tra i nodi 

    Grafo completo:
        - Tutte quelle degli snapshot
        - Distribuzione del grado entrante
        - Distribuzione del grado uscente
        - Centralità: armonica, IN-Degree e Out-Degree
        - Clustering Coefficient
    
    Arguments:
        graph {NXGraph} -- Grafo su cui vogliamo fare l'analisi
    
    Keyword Arguments:
        index {int} -- Intero che viene passato quando devo fare l'analisi temporale, mi indica su quale slot
        stiamo lavorando (default: {-1})
    """
    print "INDEX ", index
    print 
    
    
    with open('./results/' + str(index) + '20results.txt', 'w') as writer:
        
        # Queste analisi le faccio sia sul grafo completo che sugli snapshot
        
        writer.write("Numero Archi " + str(graph.number_of_edges()) + "\n")

        writer.write("Numero Nodi " + str(len(graph)) + "\n")
            
        writer.write("Connected Components " + str(nx.number_connected_components(graph.to_undirected())) + "\n")

        writer.write("Strongly Connected Components " + str(nx.number_strongly_connected_components(graph)) + "\n")

        writer.write("Diameter " + str(nx.diameter(graph.to_undirected())) + "\n")

        writer.write("Average Shortest Path Length " + str(nx.average_shortest_path_length(graph.to_undirected())) + "\n")
        
        writer.write("Average Clustering" + str(nx.average_clustering(graph.to_undirected())))
        
        # Queste analisi le faccio solamente sul grafo completo
        #if(index < 0):
         #   plot_inDegree_dist(graph, index)
          #  plot_outDegree_dist(graph, index)
           # plot_inDegree_hist(graph, index)
            #plot_outDegree_hist(graph, index)

            
            #writer.write("Centralità Armonica " + str(nx.harmonic_centrality(graph)) + "\n")

            #writer.write("IN Degree Centrality " + str(nx.in_degree_centrality(graph)) + "\n")

            #writer.write("OUT Degree Centrality " + str(nx.out_degree_centrality(graph)) + "\n")


           
            
        '''
        options = {
                'node_color': 'black',
                'node_size': 5,
                'width': 0.5,
            }
        '''
        #plt.subplot()
        #nx.draw_circular(graph, **options)
        #plt.savefig("./results/" + str(index) + "Grafo" + str(len(graph)) + ".png", bbox_inches='tight')
    

        


def plot_inDegree_dist(G, index = ""):
    """
    Viene calcolato il grado entrante dei nodi del grafo e poi si produce un grafo 
    con la distribuzione in scala logaritmica 
    
    Arguments:
        G {NXGraph} -- Grafo su cui facciamo l'analisi
    
    Keyword Arguments:
        index {int} -- Intero che viene passato quando devo fare l'analisi temporale, mi indica su quale slot
        stiamo lavorando (default: {-1})
    """
    f3 = plt.figure()
    degrees = [G.in_degree(n) for n in G.nodes()]
    tmp = {x:degrees.count(x) for x in degrees}
    degree, numNodes = tmp.keys(), tmp.values()

    df = pd.DataFrame()

    df['x'] = degree
    df['y'] = numNodes
    df.head()

    sns.set_style("ticks")
    
    fig, ax = plt.subplots(figsize=(11.7, 8.27))
    plt.title("IN Degree Distribution " + str(len(G)) + " nodes")
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(27)

    g = sns.regplot('x', 'y', data=df, fit_reg=False, ax=ax)
    
    g.set_xscale('symlog')
    g.set_yscale('symlog')

    plt.xlabel('Grado')
    plt.ylabel('Nodi')
    
    plt.xlim(0, 10000)
    plt.ylim(-1, 10000)

    plt.savefig("./results/" + str(index) + "InDegreeDistribution" + str(len(G)) + ".png", bbox_inches='tight')


def plot_inDegree_hist(G, index = ""):
    """
    Creazione dell'istogramma che mostra la distribuzione del grado
    entrante nel grafo
    
    Arguments:
        G {NXGraph} -- Grafo su cui facciamo l'analisi
    
    Keyword Arguments:
        index {int} -- Intero che viene passato quando devo fare l'analisi temporale, mi indica su quale slot
        stiamo lavorando (default: {-1})
    """
    f2 = plt.figure()
    degrees = [G.in_degree(n) for n in G.nodes()]

    plt.hist(degrees)
    plt.savefig("./results/" + str(index) + "HIST INDegreeDistribution" + str(len(G)) + ".png", bbox_inches='tight')


def plot_outDegree_dist(G, index = ""):
    """
    Viene calcolato il grado uscente dei nodi del grafo e poi si produce un grafico,
    con la distribuzione in scala logaritmica 
    
    Arguments:
        G {NXGraph} -- Grafo su cui facciamo l'analisi
    
    Keyword Arguments:
        index {int} -- Intero che viene passato quando devo fare l'analisi temporale, mi indica su quale slot
        stiamo lavorando (default: {-1})
    """
    f1 = plt.figure()
    degrees = [G.out_degree(n) for n in G.nodes()]
    tmp = {x:degrees.count(x) for x in degrees}
    degree, numNodes = tmp.keys(), tmp.values()

    df = pd.DataFrame()

    df['x'] = degree
    df['y'] = numNodes
    df.head()

    sns.set_style("ticks")
    
    fig, ax = plt.subplots(figsize=(11.7, 8.27))
    plt.title("OUT Degree Distribution " + str(len(G)) + " nodes")
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels() + ax.get_yticklabels()):
        item.set_fontsize(27)

    g = sns.regplot('x', 'y', data=df, fit_reg=False, ax=ax)
    
    g.set_xscale('symlog')
    g.set_yscale('symlog')

    plt.xlabel('Grado')
    plt.ylabel('Nodi')
    
    plt.xlim(0, 10000)
    plt.ylim(-1, 10000)

    plt.savefig("./results/" + str(index) + "OUTDegreeDistribution" + str(len(G)) + ".png", bbox_inches='tight')

  
def plot_outDegree_hist(G, index = ""):
    """
    Creazione dell'istogramma che mostra la distribuzione del grado
    uscente nel grafo
    
    Arguments:
        G {NXGraph} -- Grafo su cui facciamo l'analisi
    
    Keyword Arguments:
        index {int} -- Intero che viene passato quando devo fare l'analisi temporale, mi indica su quale slot
        stiamo lavorando (default: {-1})
    """
    f1 = plt.figure()
    degrees = [G.out_degree(n) for n in G.nodes()]

    plt.hist(degrees)
    plt.savefig("./results/" + str(index) + "HIST OUTDegreeDistribution" + str(len(G)) + ".png", bbox_inches='tight')
