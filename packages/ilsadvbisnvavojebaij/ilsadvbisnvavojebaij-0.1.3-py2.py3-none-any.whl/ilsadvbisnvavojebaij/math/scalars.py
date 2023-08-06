from typing import TypeAlias

from ..utils.logging import logger

Number: TypeAlias = int | float


def add(a: Number, b: Number) -> Number:
    logger.info("Adding scalars")
    return a + b


def subtract(a: Number, b: Number) -> Number:
    logger.info("Subtracting scalars")
    return a - b


def multiply(a: Number, b: Number) -> Number:
    logger.info("Multiplying scalars")
    return a * b


def divide(a: Number, b: Number) -> Number:
    logger.info("Dividing scalars")
    return a / b
