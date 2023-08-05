### File containing functions for the Reddit project

from numpy import random
import networkx as nx
import numpy as np

# Activation Functions

def activation(binsList): 
    activationValue = random.rand()
    for i in range(len(binsList)):
        if activationValue < binsList[i]:
            return i

# Selection Functions

def uniform_selection(allCurrentComments):
    totalComments = len(allCurrentComments)
    selectionIndex = random.randint(0, totalComments)
    #targetComment = allComments[selectionValue]
    return selectionIndex

def barabasi_albert_selection(commentNetwork, allCurrentComments):
    networkUndirected = commentNetwork.to_undirected()
    denom = max(len(allCurrentComments)*2 - 2, 1)
    selectionBinsList = [len(list(networkUndirected.neighbors(allCurrentComments[i])))/denom for i in range(len(allCurrentComments))]
    for i in range(1,(len(selectionBinsList))):
        selectionBinsList[i] += selectionBinsList[i-1]
    selectionValue = random.rand()
    for i in range(len(allCurrentComments)):
        if selectionValue < selectionBinsList[i]:
            return i
            break
    return 0

def bianconi_barabasi_layer_selection(commentNetwork, allCurrentComments):
    networkUndirected = commentNetwork.to_undirected()
    root = allCurrentComments[0]
    tempList = [0]*len(allCurrentComments)
    #depth = nx.shortest_path_length(networkUndirected, root)
    #deepest = max(depth, key = depth.get)
    #depth = depth.get(deepest)
    for i in range(len(allCurrentComments)):
        tempList[i] = (len(list(networkUndirected.neighbors(allCurrentComments[i]))) * (1 / (nx.astar_path_length(networkUndirected, allCurrentComments[i], root) + 1)))
    denom = max(sum(tempList), 1)
    selectionBinsList = [tempList[i]/denom for i in range(len(allCurrentComments))]
    for i in range(1,(len(selectionBinsList))):
        selectionBinsList[i] += selectionBinsList[i-1]
    selectionValue = random.rand()
    for i in range(len(allCurrentComments)):
        if selectionValue < selectionBinsList[i]:
            return i
            break
    return 0

def bianconi_barabasi_recency_selection(commentNetwork, allCurrentComments):
    networkUndirected = commentNetwork.to_undirected()
    tempList = [0]*len(allCurrentComments)
    for i in range(len(allCurrentComments)):
        tempList[i] = (len(list(networkUndirected.neighbors(allCurrentComments[i]))) * (np.log(i+2)))
    denom = max(sum(tempList), 1)
    selectionBinsList = [tempList[i]/denom for i in range(len(allCurrentComments))]
    for i in range(1,(len(selectionBinsList))):
        selectionBinsList[i] += selectionBinsList[i-1]
    selectionValue = random.rand()
    for i in range(len(allCurrentComments)):
        if selectionValue < selectionBinsList[i]:
            return i
            break
    return 0

# Setting Bin Sizes

def uniform_bins(n):
    binsList = [(i/n) for i in range(1,n+1)]
    return binsList

def zipfs_bins(n, s):
    HarmonicSumN = generalised_harmonic_sum(n, s)
    binsList = [(generalised_harmonic_sum(i,s)/HarmonicSumN) for i in range(1,n+1)]
    return binsList

# General Functions

def generalised_harmonic_sum(N,s):
    sum = 0
    for i in range(1,N+1):
        sum += 1/(i**s)
    return sum

def get_predecessors(G,n,prevComments):             #Not used in any current methods
    p = set(nx.neighbors(G,n))
    p = p - set(prevComments)
    return list(p)


# Editable Program Building Blocks

def initialise_lists(nActors, tSteps):
    actorList = [i for i in range(nActors)]
    commentsList = [i for i in range(nActors,(nActors+tSteps))]
    return actorList, commentsList

def iterate_reddit_network(currentTimeStep, adjacencyMatrix, activatedActor, selectedCommentValue, commentOwnersList, commentsList):

    targetComment = commentsList[selectedCommentValue]
    commentOwnersList.append(activatedActor)

    adjacencyMatrix[commentsList[currentTimeStep]][targetComment] += 1                            #Comment to comment
    adjacencyMatrix[commentOwnersList[selectedCommentValue]][activatedActor] += 1           #Actor to actor
    adjacencyMatrix[commentsList[currentTimeStep]][activatedActor] += 1                             #Actor to comment

    return adjacencyMatrix

def width_and_depth(rootNode, commentsGraph):

    widthList = [1]
    depthList = []

    currentDepth = 1
    predecessors = [list(commentsGraph.predecessors(rootNode))]
    while predecessors != []:
        currentDepth += 1
        currentWidth = 0
        nextPredecessors = []
        for i in predecessors: 
            currentWidth += len(i)
            for j in i:
                currentNodePredecessors = list(commentsGraph.predecessors(j))
                if currentNodePredecessors == []:
                    depthList.append(currentDepth)
                else:
                    nextPredecessors.append(currentNodePredecessors)
        predecessors = nextPredecessors
        widthList.append(currentWidth)

    maxWidth = max(widthList)
    meanWidth = sum(widthList)/len(widthList)
    maxDepth = max(depthList)
    meanDepth = sum(depthList)/len(depthList)

    return [maxWidth, meanWidth, maxDepth, meanDepth]



# Standard Program

def standard_actsecmodel(tSteps, nActors, aBinsList, selectionType):
    # Initialise

    timeSteps = tSteps
    noActors = nActors
    developmentArray = np.zeros((timeSteps,4))
    actorDevelopmentArray = np.zeros((timeSteps,4))
    actorDevelopmentArray[0][0] = nActors
    for i in range(1,4):
        actorDevelopmentArray[0][i] = 0
    for i in range(4):
        developmentArray[0][i] = 1

    actorList = [i for i in range(noActors)]
    commentsList = [i for i in range(noActors,(noActors+timeSteps))]
    actorBinsList = aBinsList                                          #NOTE: Could probably put this outside the iterations and then feed it as an input

    adjacencyMatrix = np.zeros((noActors+timeSteps,noActors+timeSteps))                 #adjacencyMatrix[pointing to][pointing away from]
    adjacencyMatrix[noActors][0] += 1
    commentOwners = [0]

    # Run Iterations

    for t in range(1,timeSteps):
        currentActor = actorList[activation(actorBinsList)]
        
        # Comment Selection
        
        match selectionType:
            case 'uniform': 
                targetCommentValue = uniform_selection(commentOwners)           #The length of commentOwners is the same as the current number of comments (as the comments list begins with all the comments already)
            case 'barabasi':
                tempCommentsList = (commentsList[0:t])                          #A temporary comment list is created so that it's only as long as the current number of comments
                G = nx.from_numpy_array(adjacencyMatrix, create_using=nx.DiGraph)
                targetCommentValue = barabasi_albert_selection(G.subgraph(tempCommentsList), tempCommentsList)
            case 'layer':
                tempCommentsList = (commentsList[0:t])
                G = nx.from_numpy_array(adjacencyMatrix, create_using=nx.DiGraph)
                targetCommentValue = bianconi_barabasi_layer_selection(G.subgraph(tempCommentsList), tempCommentsList)
            case 'recency':
                tempCommentsList = (commentsList[0:t])
                G = nx.from_numpy_array(adjacencyMatrix, create_using=nx.DiGraph)
                targetCommentValue = bianconi_barabasi_recency_selection(G.subgraph(tempCommentsList), tempCommentsList)
            case _:
                raise Exception('Invalid selection type')
                
           
        targetComment = commentsList[targetCommentValue]
        commentOwners.append(currentActor)

        adjacencyMatrix[commentsList[t]][targetComment] += 1                            #Comment to comment
        adjacencyMatrix[commentOwners[targetCommentValue]][currentActor] += 1           #Actor to actor
        adjacencyMatrix[commentsList[t]][currentActor] += 1                             #Actor to comment

        # Create Graph From Adjacency Matrix

        G = nx.from_numpy_array(adjacencyMatrix, create_using=nx.DiGraph)
        C = G.subgraph(commentsList)

        # Find Depth and Width Measures

        widthList = [1]
        depthList = []
        root = commentsList[0]

        currentDepth = 1
        predecessors = [list(C.predecessors(root))]
        while predecessors != []:
            currentDepth += 1
            currentWidth = 0
            nextPredecessors = []
            for i in predecessors: 
                currentWidth += len(i)
                for j in i:
                    currentNodePredecessors = list(C.predecessors(j))
                    if currentNodePredecessors == []:
                        depthList.append(currentDepth)
                    else:
                        nextPredecessors.append(currentNodePredecessors)
            predecessors = nextPredecessors
            widthList.append(currentWidth)

        maxWidth = max(widthList)
        meanWidth = sum(widthList)/len(widthList)
        maxDepth = max(depthList)
        meanDepth = sum(depthList)/len(depthList)
        
        developmentArray[t][0] = maxWidth
        developmentArray[t][1] = meanWidth
        developmentArray[t][2] = maxDepth
        developmentArray[t][3] = meanDepth

        A = G.subgraph(actorList)
        cliques = len(list(nx.enumerate_all_cliques(A.to_undirected())))
        transitivity = nx.transitivity(A)
        reciprocity = nx.overall_reciprocity(A)
        clustering = nx.average_clustering(A)

        actorDevelopmentArray[t][0] = cliques
        actorDevelopmentArray[t][1] = transitivity
        actorDevelopmentArray[t][2] = reciprocity
        actorDevelopmentArray[t][3] = clustering

    return [maxWidth, meanWidth, maxDepth, meanDepth, developmentArray, cliques, transitivity, reciprocity, clustering, actorDevelopmentArray]




# Main Test

if __name__ == "__main__":
    # INITIALISING
    timeSteps = 25
    noActors = 20

    actorList, commentsList = initialise_lists(noActors, timeSteps)

    adjacencyMatrix = np.zeros((noActors+timeSteps,noActors+timeSteps))         #adjacencyMatrix[pointing to][pointing away from]
    adjacencyMatrix[noActors][0] += 1
    G = nx.from_numpy_array(adjacencyMatrix, create_using=nx.DiGraph)
    commentOwners = [0]

    binsList = zipfs_bins(noActors, 1)      #If activation depends on the state of the graph, move to within iterations

    widthDepthArray = np.zeros((timeSteps, 4))

    # ITERATIONS
    for t in range(1, timeSteps): 
        # ACTIVATION
        currentActor = activation(binsList)
        
        # SELECTION
        tempCommentsList = (commentsList[0:t])      #A temporary comment list is created so that it's only as long as the current number of comments
        targetCommentValue = barabasi_albert_selection(G.subgraph(tempCommentsList), tempCommentsList)

        # UPDATE MATRIX AND GRAPH
        adjacencyMatrix = iterate_reddit_network(t, adjacencyMatrix, currentActor, targetCommentValue, commentOwners, commentsList)
        G = nx.from_numpy_array(adjacencyMatrix, create_using=nx.DiGraph)
        C = G.subgraph(commentsList)

        # WIDTH, DEPTH, OR OTHER MEASURES
        tempWidthDepth = width_and_depth(commentsList[0], C)
        for j in range(4):
            widthDepthArray[t][j] = tempWidthDepth[j]
    
    # RESULTS
    print(widthDepthArray)

