import numpy as np
# vectorNorm

def vectorNorm(vector, segment):
    vector = np.asarray(vector, dtype=float).reshape(2,)
    angle = np.degrees(
        np.arctan(np.abs(vector[1]) / np.abs(vector[0]))
    )

    if vector[0] > 0 and vector[1] > 0:
        # Find the normalized vector.
        normalisedVector = np.array([
            segment * np.cos(np.radians(angle)),
            segment * np.sin(np.radians(angle)),
        ])

    elif vector[0] < 0 and vector[1] > 0:
        normalisedVector = np.array([
            -(segment * np.cos(np.radians(angle))),
            segment * np.sin(np.radians(angle)),
        ])

    elif vector[0] < 0 and vector[1] < 0:
        normalisedVector = np.array([
            -(segment * np.cos(np.radians(angle))),
            -(segment * np.sin(np.radians(angle))),
        ])

    elif vector[0] > 0 and vector[1] < 0:
        normalisedVector = np.array([
            segment * np.cos(np.radians(angle)),
            -(segment * np.sin(np.radians(angle))),
        ])

    return normalisedVector