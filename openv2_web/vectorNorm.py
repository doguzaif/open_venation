import numpy as np


def vectorNorm(vector, segment):
    """Scale a 2D vector to the requested length, preserving its quadrant."""
    vector = np.asarray(vector, dtype=float).reshape(2,)
    x, y = vector

    # Handle axis-aligned and zero vectors explicitly. The MATLAB function's
    # four quadrant cases do not assign a result for these inputs.
    if x == 0:
        if y > 0:
            return np.array([0.0, segment])
        if y < 0:
            return np.array([0.0, -segment])
        return np.array([0.0, 0.0])

    if y == 0:
        if x > 0:
            return np.array([segment, 0.0])
        return np.array([-segment, 0.0])

    angle = np.degrees(np.arctan(np.abs(y) / np.abs(x)))
    x_component = segment * np.cos(np.radians(angle))
    y_component = segment * np.sin(np.radians(angle))

    if x > 0 and y > 0:
        normalisedVector = np.array([x_component, y_component])
    elif x < 0 and y > 0:
        normalisedVector = np.array([-x_component, y_component])
    elif x < 0 and y < 0:
        normalisedVector = np.array([-x_component, -y_component])
    else:  # x > 0 and y < 0
        normalisedVector = np.array([x_component, -y_component])

    return normalisedVector
