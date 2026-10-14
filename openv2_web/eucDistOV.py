import numpy as np
from scipy.spatial import cKDTree


def euc_dist_ov(allnodes, x2, y2):
    """Return all node distances, the minimum, and its stored node index."""
    distances = np.sqrt(
        (allnodes[:, 0] - x2) ** 2 + (allnodes[:, 1] - y2) ** 2
    )
    alldistances = np.column_stack(
        (distances, allnodes[:, 4], allnodes[:, 0:2])
    )
    min_row_idx = int(np.argmin(distances))
    return alldistances, distances[min_row_idx], allnodes[min_row_idx, 4]


def nearest_nodes(allnodes, points):
    """Find each point's closest node in one spatial-tree query."""
    points = np.asarray(points, dtype=float).reshape(-1, 2)
    if points.shape[0] == 0:
        return np.empty(0), np.empty(0)

    tree = cKDTree(allnodes[:, 0:2])
    distances, row_indices = tree.query(points)
    stored_indices = allnodes[row_indices, 4]
    return distances, stored_indices
