from typing import TypeAlias

import numpy as np
import numpy.typing as npt

from ..utils.logging import logger

Number: TypeAlias = int | float
NDArrayInt: TypeAlias = npt.NDArray[np.int_]
NDArrayFloat: TypeAlias = npt.NDArray[np.float_]
NDArrayNumber: TypeAlias = NDArrayInt | NDArrayFloat


def add(a: NDArrayNumber, b: NDArrayNumber) -> NDArrayNumber:
    logger.info("Adding vectors")
    return a + b


def subtract(a: NDArrayNumber, b: NDArrayNumber) -> NDArrayNumber:
    logger.info("Subtracting vectors")
    return a - b


def multiply(a: NDArrayNumber, b: NDArrayNumber) -> NDArrayNumber:
    logger.info("Multiplying vectors (component-wise)")
    return a * b


def divide(a: NDArrayNumber, b: NDArrayNumber) -> NDArrayNumber:
    logger.info("Dividing vectors (component-wise)")
    return a / b


def dot_prod(a: NDArrayNumber, b: NDArrayNumber) -> Number:
    logger.info("Computing dot product of vectors")
    return np.dot(a, b)
