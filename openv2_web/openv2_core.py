"""OpenV2 growth simulation, separated from its web and plotting interface."""

import numpy as np
from scipy.stats import qmc

import eucDistOV
import newNodeOV2


ATTRACTION_DISTANCE = 10.0
KILL_DISTANCE = 5.0
SEGMENT_LENGTH = 1.0
ATTRACTORS_PER_10000_UM2 = 1000


def _initial_attractors(nx, ny, seed):
    no_att = int(ATTRACTORS_PER_10000_UM2 * ((nx * ny) / 10000))

    # Match the quasi-random Halton method used by the supplied openv2.py.
    sampler = qmc.Halton(d=2, scramble=True, seed=seed)
    sampler.fast_forward(1000)
    points = sampler.random(n=no_att * 101)[::101][:no_att]
    attractors = points * np.array([nx, ny])
    return attractors


def _initial_nodes(nx, ny, seed):
    rng = np.random.default_rng(seed)
    low = np.array([nx * 0.4, ny * 0.4])
    high = np.array([nx * 0.6, ny * 0.6])
    starting_nodes = rng.uniform(low=low, high=high, size=(1, 2))

    all_nodes = np.full((starting_nodes.shape[0], 5), np.nan)
    all_nodes[:, 0:2] = starting_nodes
    all_nodes[:, 4] = np.arange(1, all_nodes.shape[0] + 1)
    return starting_nodes, all_nodes


def _snapshot(iteration, attractors, all_nodes):
    return {
        "iteration": iteration,
        "attractors": attractors.copy(),
        "nodes": all_nodes[:, 0:2].copy(),
    }


def run_openv2(nx, ny, seed=42, max_iterations=400):
    """Run the growth algorithm and return a sequence of animation frames."""
    nx = int(nx)
    ny = int(ny)
    if nx <= 0 or ny <= 0:
        raise ValueError("Nx and Ny must be positive integers.")

    starting_attractors = _initial_attractors(nx, ny, seed)
    starting_nodes, all_nodes = _initial_nodes(nx, ny, seed + 1)
    attractors = starting_attractors
    frames = [_snapshot(0, attractors, all_nodes)]
    iterations = 0
    stop_reason = "No new nodes were added."

    for iteration in range(1, max_iterations + 1):
        min_distances, nearest_node_indices = eucDistOV.nearest_nodes(
            all_nodes, attractors
        )

        updated_attractors = attractors[min_distances > KILL_DISTANCE, :]
        influencing_mask = (
            (min_distances > KILL_DISTANCE)
            & (min_distances < ATTRACTION_DISTANCE)
        )
        influencing_att = np.column_stack((
            attractors[influencing_mask, :],
            nearest_node_indices[influencing_mask],
        ))

        previous_node_count = all_nodes.shape[0]
        all_nodes = newNodeOV2.newNodeOV2(
            influencing_att,
            all_nodes,
            SEGMENT_LENGTH,
        )
        iterations = iteration
        frames.append(_snapshot(iteration, updated_attractors, all_nodes))

        # Compare row counts: this directly checks whether the iteration
        # actually added nodes, unlike counting unique x-coordinate values.
        if all_nodes.shape[0] == previous_node_count:
            stop_reason = "Growth stopped because this iteration added no nodes."
            break

        attractors = updated_attractors
    else:
        stop_reason = f"Stopped at the safety limit of {max_iterations} iterations."

    return {
        "nx": nx,
        "ny": ny,
        "seed": seed,
        "initial_attractor_count": starting_attractors.shape[0],
        "initial_node_count": starting_nodes.shape[0],
        "final_node_count": all_nodes.shape[0],
        "remaining_attractor_count": frames[-1]["attractors"].shape[0],
        "iterations": iterations,
        "stop_reason": stop_reason,
        "frames": frames,
    }
