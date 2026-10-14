import numpy as np
import vectorNorm as vectorNorm

# newNodeOV2
#
# 8/11
#
# This function is meant to work with the openV2 script to produce new nodes.

def newNodeOV2(influencingAtt, allNodes, segment):

    # Get a list of unique indices for the influenced nodes.
    uniqueNodeIndices = np.unique(influencingAtt[:, -1])

    # Loop through these unique nodes and grow each one according to the
    # attractors that influence it.
    for nodeIndex in uniqueNodeIndices:

        # Get the node coordinates.
        nodeRows = allNodes[allNodes[:, 4] == nodeIndex]
        node = nodeRows[:, 0:2]

        # Get the list of attractors that influence this node.
        att = influencingAtt[influencingAtt[:, -1] == nodeIndex, 0:2]

        # Find the vectors between the node and its associated attractors.
        # Normalize each vector.
        vec = att - node
        normvec = np.zeros(vec.shape)

        # Normalize each of these vectors.
        for v in range(vec.shape[0]):
            normvec[v, :] = vectorNorm.vectorNorm(vec[v, :], segment)

        # Find the vector between the parent and child nodes. If it is NaN,
        # replace it with [0, 0].
        parentvec = node - nodeRows[:, 2:4]
        if np.isnan(np.mean(parentvec)):
            parentvec = np.array([[0.0, 0.0]])

        # Sum the normalized attractor vectors and the parent vector,
        # then normalize the result.
        normvec = np.sum(normvec, axis=0) + parentvec
        normvec = vectorNorm.vectorNorm(normvec, segment)

        # Add the final normalized vector to the current node to get the
        # newest node.
        newnode = node + normvec

        # Append the new node, set its parent coordinates, and assign its index.
        newRow = np.full((1, 5), np.nan)
        newRow[0, 0:2] = newnode
        newRow[0, 2:4] = node
        newRow[0, 4] = allNodes[-1, 4] + 1
        allNodes = np.vstack((allNodes, newRow))

    return allNodes