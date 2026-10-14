import numpy as np

def euc_dist_ov(allnodes, x2, y2):
    """
    Simple code for calculating 2D Euclidean distance.
    allnodes is expected to be a 2D numpy array.
    """
    
    # 1. Calculate distances
    # Note: Python is 0-indexed. MATLAB's col 1 -> Python's col 0
    distances = np.sqrt((allnodes[:, 0] - x2)**2 + (allnodes[:, 1] - y2)**2)
    
    # 2. Concatenate into alldistances
    # np.column_stack elegantly combines 1D arrays and 2D slices as columns
    # MATLAB: [alldistances, allnodes(:,5), allnodes(:,1:2)]
    # Python: [distances,    allnodes[:,4], allnodes[:,0:2]]
    alldistances = np.column_stack((distances, allnodes[:, 4], allnodes[:, 0:2]))
    
    # 3. Find the minimum distance
    mindist = np.min(alldistances[:, 0])
    
    # 4. Get index as seen in allnodes matrix (5th column -> index 4)
    # np.argmin naturally finds the row index of the FIRST minimum value, 
    # which cleanly replaces MATLAB's find() and if size > 1 logic.
    min_row_idx = np.argmin(alldistances[:, 0])
    mindistidx = allnodes[min_row_idx, 4]
    
    return alldistances, mindist, mindistidx