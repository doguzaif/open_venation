import numpy as np

import vectorNorm


def newNodeOV2(influencingAtt, allNodes, segment):
    """Grow one child node from each uniquely influenced parent node."""
    if influencingAtt.shape[0] == 0:
        return allNodes

    uniqueNodeIndices = np.unique(influencingAtt[:, -1])

    for nodeIndex in uniqueNodeIndices:
        nodeRows = allNodes[allNodes[:, 4] == nodeIndex]
        if nodeRows.shape[0] == 0:
            continue

        # Keep coordinates one-dimensional (shape (2,)) to avoid accidental
        # (1, 2) broadcasting when combining vectors.
        nodeRow = nodeRows[0]
        node = nodeRow[0:2]
        att = influencingAtt[influencingAtt[:, -1] == nodeIndex, 0:2]

        vec = att - node
        normvec = np.zeros(vec.shape)
        for v in range(vec.shape[0]):
            normvec[v, :] = vectorNorm.vectorNorm(vec[v, :], segment)

        parentvec = node - nodeRow[2:4]
        if np.isnan(parentvec).any():
            parentvec = np.array([0.0, 0.0])

        combinedVector = np.sum(normvec, axis=0) + parentvec
        growthVector = vectorNorm.vectorNorm(combinedVector, segment)

        # Avoid appending a duplicate node if the influences cancel exactly.
        if np.allclose(growthVector, 0.0):
            continue

        newnode = node + growthVector

        newRow = np.full((1, 5), np.nan)
        newRow[0, 0:2] = newnode
        newRow[0, 2:4] = node
        newRow[0, 4] = allNodes[-1, 4] + 1
        allNodes = np.vstack((allNodes, newRow))

    return allNodes
