from typing import Any, Literal

def pydle(
    x: int,
    y: int,
    val: Any,
    colour: Literal[
        "white", "black", "red", "green", "blue",
        "yellow", "orange", "brown", "purple",
    ],
) -> None:
    """
    Set the character and colour of a cell in the 5x5 grid.

    Parameters
    ----------
    x : int
        The x-coordinate of the cell (0-4). Origin is top-left corner.
    y : int
        The y-coordinate of the cell (0-4). Origin is top-left corner.
    val : Any
        The value to be displayed in the cell, converted to a string.
        If None or empty string, the cell will be blank. If the string is
        longer than 2 characters, it will be truncated to the first 2
        characters.
    colour : str
        The colour of the cell. Must be one of the following: "white",
        "black", "red", "green", "blue", "yellow", "orange", "brown",
        "purple".
    """
    ...
