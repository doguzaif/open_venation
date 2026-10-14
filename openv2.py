# openV2

#python packages
import numpy as np
from scipy.stats import qmc
import eucDistOV
import newNodeOV2
import matplotlib.pyplot as plt

# Implementation of the method described in the article below, titled
# "Fractal Trees - Space Colonisation":
# https://medium.com/@jason.webb/space-colonization-algorithm-in-javascript-6f683b743dc5

# Clear variables and close all figures (uncomment to enable):
# globals().clear()
# import matplotlib.pyplot as plt
# plt.close("all")

# BEGIN

# Create the medium, define attractors, and define starting nodes.

# First, create the medium by defining its edge lengths, Ny and Nx, in µm.
Nx = 150
Ny = 150

# Create a number of randomly positioned attractors in this medium.
# Note: There should be 1,500 attractors per 10,000 µm²
# (a medium measuring 100 µm × 100 µm).
noAtt = 1000 * ((Nx * Ny) / 10000)

# Choose the attractor-scatter method: "r" for random or "qr" for quasi-random.
method = "qr"

if method == "r":
    # Random attractor generation.
    # Alternative distribution, with attractors restricted to the upper 80% of the medium:
    # startingAttractors = np.column_stack((
    #     (Nx - 1) * np.random.rand(int(noAtt)) + 1,
    #     (Ny - Ny * 0.2) * np.random.rand(int(noAtt)) + Ny * 0.2,
    # ))

    startingAttractors = np.column_stack((
        (Nx - 1) * np.random.rand(int(noAtt)) + 1,
        (Ny - 1) * np.random.rand(int(noAtt)) + 1,
    ))
    titlestr = "Open Venetion Example - Randomly Scattered Attractors"

elif method == "qr":
    # Quasi-random attractor generation.
    # Requires: from scipy.stats import qmc
    sampler = qmc.Halton(d=2, scramble=True)
    sampler.fast_forward(1000)  # Skip the first 1,000 points.

    # MATLAB's Leap=1e2 skips 100 points between generated points.
    # Generate the sequence and take every 101st point.
    points = sampler.random(n=int(noAtt) * 101)[::101][:int(noAtt)]
    startingAttractors = points * np.array([Nx, Ny])

    titlestr = "Open Venetion Example - Quasi-Randomly Scattered Attractors"

# Create nodes.
noNodes = 1

# Alternative: place nodes along the center of the medium.
# startingNodes = np.column_stack((
#     np.full(noNodes, Nx / 2),
#     np.linspace(1, Ny * 0.3, noNodes),
# ))

# Alternative: place nodes randomly throughout the medium.
# startingNodes = np.column_stack((
#     (Nx - 1) * np.random.rand(noNodes) + 1,
#     (Ny - 1) * np.random.rand(noNodes) + 1,
# ))

# Place nodes randomly within the middle 20% of each dimension.
startingNodes = np.column_stack((
    (Nx * 0.6 - Nx * 0.4) * np.random.rand(noNodes) + Nx * 0.4,
    (Ny * 0.6 - Ny * 0.4) * np.random.rand(noNodes) + Ny * 0.4,
))

# Alternative: random x-position in the middle 20%, and y-position
# between 1 and Ny * 0.1.
# startingNodes = np.column_stack((
#     (Nx * 0.6 - Nx * 0.4) * np.random.rand(noNodes) + Nx * 0.4,
#     (Ny * 0.1 - 1) * np.random.rand(noNodes) + 1,
# ))

# Create a matrix for all nodes (children, parents, and index).
allNodes = np.zeros((startingNodes.shape[0], 5))
allNodes[:, 0:2] = startingNodes
allNodes[:, 4] = np.arange(1, allNodes.shape[0] + 1)

# Replace all zeros with NaN.
allNodes[allNodes == 0] = np.nan

# NODE GROWTH

# Define the maximum attraction distance and the kill distance.
attractionDistance = 10
killdistance = 5

# Define the segment distance between nodes.
segment = 1

# Start one figure for the visualization.
plt.ion()
fig, ax = plt.subplots(figsize=(12, 8))
plt.show(block=False)

# Loop to grow the network. Set k as the counter.
k = 1
condition = 1

while condition == 1:

    # Monitor the total number of nodes. This variable is part of the
    # loop termination criterion.
    check1 = np.unique(allNodes[:, 0]).size

    # STEP 1
    # Get the right set of attractors.

    # On the first iteration, use the attractors placed initially.
    if k == 1:
        attractors = startingAttractors
    # On later iterations, use the attractors remaining after those
    # within the kill distance have been removed.
    else:
        attractors = updatedAttractors

    # Store each attractor's distance to its closest node and that
    # node's index. The node index is in column 2.
    minDistances = np.zeros((attractors.shape[0], 2))

    # STEP 2
    # Find the closest node to each attractor.
    for a in range(attractors.shape[0]):
        # eucDistOV returns the distances from this attractor to each
        # node, the minimum distance, and the index of that node.
        _, minDistances[a, 0], minDistances[a, 1] = (
            eucDistOV.euc_dist_ov(
                allNodes,
                attractors[a, 0],
                attractors[a, 1],
            )
        )

    # STEP 3
    # Remove attractors within the kill distance and identify those
    # that will induce growth.

    # Keep attractors outside the kill distance for the next iteration.
    updatedAttractors = attractors[minDistances[:, 0] > killdistance, :]

    # Select attractors whose closest node is within the attraction range.
    # The third column contains references to their associated nodes in allNodes.
    influencing_mask = (
        (minDistances[:, 0] > killdistance)
        & (minDistances[:, 0] < attractionDistance)
    )
    influencingAtt = np.column_stack((
        attractors[influencing_mask, :],
        minDistances[influencing_mask, 1],
    ))

    # GENERATE NEW NODES
    # Grow the associated nodes for the influencing attractors.
    # Each node can produce only one new node, which prevents excessive
    # branch splitting.
    allNodes = newNodeOV2.newNodeOV2(
        influencingAtt,
        allNodes,
        segment,
    )

    # Update the counter.
    k += 1

    # VISUALIZE this iteration in the same figure.
    # ax.clear() is the Matplotlib equivalent of clearing the current
    # plotting area before redrawing it.
    ax.clear()

    leg_att = ax.scatter(
        updatedAttractors[:, 0],
        updatedAttractors[:, 1],
        s=36,
        color=(0.4660, 0.6740, 0.1880),
        marker=".",
    )
    leg_nodes, = ax.plot(
        allNodes[:, 0],
        allNodes[:, 1],
        "k.",
    )
    leg_roots = ax.scatter(
        startingNodes[:, 0],
        startingNodes[:, 1],
        s=200,
        color=(0.6350, 0.0780, 0.1840),
        marker="x",
        linewidths=3,
    )

    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-(Nx * 0.1), Nx * 1.1)
    ax.set_ylim(-(Ny * 0.1), Ny * 1.1)
    ax.tick_params(axis="both", labelsize=18)
    ax.set_ylabel(r"Distance ($\mu$m)")
    ax.set_xlabel(r"Distance ($\mu$m)")
    ax.set_title("Open Venation Pattern Generation")

    # Briefly display the updated figure before continuing the loop.
    plt.pause(0.015)

    # Monitor the number of unique x-coordinates, as in the MATLAB code.
    check2 = np.unique(allNodes[:, 0]).size

    # If this value has not changed, terminate the loop.
    if check1 == check2:
        condition = 2

# Final visualization steps, after the loop ends.
plt.ioff()

ax.set_title(titlestr)
ax.legend(
    [leg_att, leg_roots, leg_nodes],
    ["Attractors", "Roots", "Nodes"],
)
ax.set_xlabel(
    "Distance (µm)\n"
    f"Iterations = {k}, "
    f"Attractors initially {noAtt}, "
    f"ultimately {updatedAttractors.shape[0]}, "
    f"Nodes initially {noNodes}, "
    f"ultimately {allNodes.shape[0]}"
)
ax.set_ylabel(r"Distance ($\mu$m)")
ax.tick_params(axis="both", labelsize=15)

fig.tight_layout()
plt.show()


'''

    # VISUALIZE
    fig, ax = plt.subplots()
ax.clear()

leg_att = ax.scatter(
    updatedAttractors[:, 0],
    updatedAttractors[:, 1],
    s=36,
    color=(0.4660, 0.6740, 0.1880),
    marker=".",
)
leg_nodes, = ax.plot(
    allNodes[:, 0],
    allNodes[:, 1],
    "k.",
)
leg_roots = ax.scatter(
    startingNodes[:, 0],
    startingNodes[:, 1],
    s=200,
    color=(0.6350, 0.0780, 0.1840),
    marker="x",
    linewidths=3,
)

ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-(Nx * 0.1), Nx * 1.1)
ax.set_ylim(-(Ny * 0.1), Ny * 1.1)
ax.tick_params(axis="both", labelsize=18)

ax.set_title("Open Venation Pattern Generation")


# Briefly display the updated figure before continuing the loop.
plt.pause(0.015)

# Monitor the total number of nodes. This is used in the loop
# termination criterion.
check2 = np.unique(allNodes[:, 0]).size

# If the total number of nodes remains unchanged, terminate the operation.
if check1 == check2:
    condition = 2
    
'''