# Recall issues
The strategy is to divide an conquer by:

1. extracting linguistic items, marking forgotten data
2. to cluster recalled linguistic data to given RI dictionary, 
3. return to marked and forgotten data,
4. search for string-level actually forgotten data and retrieve it. 

The clustering filter uses WEs and two hierarchies of centroids. The first one is the class (activation, repression, regulation) and the second one is each registered morphological variation of the verbs expressing each class (RI). Clusters are thus formed by ranking cosine similarities from embedded linguistic items to cluster centroids.
