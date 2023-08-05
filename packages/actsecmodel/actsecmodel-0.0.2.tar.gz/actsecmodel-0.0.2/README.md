# ActSecModel Package

This package contains most of the key code that I used in the first half of 2023 for the Reddit Deliberation Project. 
The fucntions are explained here, guides for setting up variables to be compatible with these functions are explained, and an example is given at the bottom. 
Any code that I used that isn't here was already part of another package, like matplotlib or networkx. 

# SETTING UP VARIABLES/ARRAYS

In order to be compatible with the code as I have written it, I would recommend following this set up. 
Use the following code to initialise your actor and comments lists: 
```
actorList = [i for i in range(noActors)]
commentsList = [i for i in range(noActors,(noActors+timeSteps))]
```
This ensures that each potential actor and potential comment are initialised in advance, which was one of the properties of the method I used, and it means each actor and comment's ID matches its row/column in the adjacency array. This code is captured in the function initialise_lists for convenience. 

The commentOwnersList is a list that contains each actor who posted a comment in the order that they posted them. The index of each actor corresponds to the index of the comment in the commentList that they posted. 


# FUNCTIONS NOT IN THIS PACKAGE

Functions for the actor layer measures are all contained in the Network X package, and are listed below: 
```
cliques = len(list(nx.enumerate_all_cliques(A.to_undirected())))
transitivity = nx.transitivity(A)
reciprocity = nx.overall_reciprocity(A)
clustering = nx.average_clustering(A)
```
I used matplotlib and Gephi for all the graphing and visuals. A tutorial for the 95% confidence elipses is under this link https://matplotlib.org/stable/gallery/statistics/confidence_ellipse.html, since that took me longer to find on account of being in the examples section of the documentation, rather than the reference. 


# FUNCTION DOCUMENTATION

### ACTIVATION FUNCTIONS

##### activation(binsList):

A fucntion that choses an actor for activation. 
- *binslist.* A list containing the probability bins for each actor to fall into. Each item in the list should be the cumulative probability of the respective actor being chosen. 
- RETURNS: The integer index of the actor chosen for activation (in my program, each actor was assigned a number from 0 upwards, so this index was also the actor's ID, and later code relfects this. The same was not true for comments)

##### uniform_bins(n):

A fucntion that creates the binsList for uniform activation.
- *n.* The number of actors. 
- RETURNS: The list binsList for uniform activation

##### zipfs_bins(n, s):

A fucntion that creates the binsList for Zipf's Law activation.
- *n.* The number of actors. 
- *s.* The Zipf's constant. 
- RETURNS: The list binsList for Zipf's Law activation


### SELECTION FUNCTIONS

##### uniform_selection(allCurrentComments):

A function for choosing a comment with uniform selection. 
- *allCurrentComments.* A list containing all comments that have currently been made
- RETURNS: The integer index of the comment chosen for selection

##### barabasi_albert_selection(commentNetwork, allCurrentComments):

A function for choosing a comment with Barabasi-Albert selection. 
- *commentNetwork.* The discussion layer of the current NetworkX network
- *allCurrentComments.* A list containing all comments that have currently been made
- RETURNS: The integer index of the comment chosen for selection

##### bianconi_barabasi_layer_selection(commentNetwork, allCurrentComments):

A function for choosing a comment with level selection. 
- *commentNetwork.* The discussion layer of the current NetworkX network
- *allCurrentComments.* A list containing all comments that have currently been made
- RETURNS: The index of the comment chosen for selection

##### bianconi_barabasi_recency_selection(commentNetwork, allCurrentComments):

A function for choosing a comment with recency selection. 
- *commentNetwork.* The discussion layer of the current NetworkX network
- *allCurrentComments.* A list containing all comments that have currently been made
- RETURNS: The integer index of the comment chosen for selection


### GENERAL FUNCTIONS

##### generalised_harmonic_sum(N,s):

A function to find the generalised harmonic sum. 
- *N.* The number of values to be summed over
- *s.* The power of the denominator
- RETURNS: The float value of the generalised harmonic sum over the first N terms. 

##### initialise_lists(nActors, tSteps):

A function to initialise the actor and comments lists for a predetermined number of actors and comments. 
- *nActors.* The total number of actors
- *tSteps.* The total number of timesteps (and thus total number of comments)
- RETURNS: The actor and comments lists, in that order, separated by a comma. 

##### iterate_reddit_network(currentTimeStep, adjacencyMatrix, activatedActor, selectedCommentValue, commentOwnersList, commentsList):

A function that receives the activated actor and selected commennt and updates the adjacency matrix accordingly.
- *currentTimeStep.* An integer for the current timestep
- *adjacencyMatrix.* The current adjacency matrix for the multilayer network
- *activatedActor.* The actor chosen for activation. In my case, the index and actor ID were identical, so I simply fed in the index
- *selectedCommentValue.* The index in the commentsList for the selected comment
- *commentOwnersList.* The list of comment owners (see top)
- *commentsList.* The commentsList list representing the list of all comments
- RETURNS: The updated adjacency matrix. 

##### width_and_depth(rootNode, commentsGraph):

A function to find the mean and maximum width and depth measures from a discussion layer graph. 
- *rootNode.* The root node/initial post of the discussion layer graph. 
- *commentsGraph.* The NetworkX graph for the discussion layer. 
- RETURNS: The following list: [maxWidth, meanWidth, maxDepth, meanDepth]

##### standard_actsecmodel(tSteps, nActors, aBinsList, selectionType):

The function I used in my model, that completely iterates through a set number of timesteps, for a set number of actors, for the activation and selection types available in this package. 
- *tStepss.* The number of timesteps to run for. 
- *nActors.* The number of actors in the actor layer (note that not all actors may participate)
- *aBinsList.* The binsList list for the activation type being used 
- *selectionType.* A string to determine which selection type to be used, choosing from 'uniform', 'barabsi', 'layer', or 'recency'
- RETURNS: The following list: [maxWidth, meanWidth, maxDepth, meanDepth, developmentArray, cliques, transitivity, reciprocity, clustering, actorDevelopmentArray]. The maxWidth, meanWidth, maxDepth, meanDepth, cliques, transitivity, reciprocity, and clustering measures are all terminal. developmentArray is a Numpy array that contains the development of the discussion layer measures over time. actorDevelopmentArray is a Numpy array that contains the development of the actor layer measures over time. 



## EXAMPLE CODE
```
# INITIALISING
timeSteps = 25
noActors = 20

actorList = [i for i in range(noActors)]
commentsList = [i for i in range(noActors,(noActors+timeSteps))]

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
```