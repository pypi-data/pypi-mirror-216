from typing import Any

import numpy as np


def sanitize_float(field: str, value: Any) -> float:
    # make sure the value is YAML-serializable
    if value is not None:
        # float values
        if isinstance(value, float):
            pass
        # Numpy float values
        elif isinstance(value, (np.float32, np.float64)):
            value = float(value)
        # Numpy int values
        elif isinstance(value, (np.int8, np.int16, np.int32, np.int64, np.uint, int)):
            value = float(value)
        # unknown value
        else:
            raise ValueError(f"You cannot set the property '{field}' to an object "
                             f"of type '{type(value)}'")
    return value


def sanitize_color_float(field: str, value: Any) -> float:
    # make sure the value is YAML-serializable
    if value is not None:
        # float values
        if isinstance(value, float):
            pass
        # Numpy float values
        elif isinstance(value, (np.float32, np.float64)):
            value = float(value)
        # Numpy int values
        elif isinstance(value, (np.int8, np.int16, np.int32, np.int64, np.uint, int)):
            value = float(value) / 255.0
        # unknown value
        else:
            raise ValueError(f"You cannot set the property '{field}' to an object "
                             f"of type '{type(value)}'")
    return value
