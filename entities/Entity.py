from itertools import product
import yaml
import math
import random
from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .GOLGrid import GOLGrid


class Entity:
    def __init__(self, x: int, y: int, base_ttl: Optional[int] = None) -> None:
        """
        Base object class.
        """
        self.x = x
        self.y = y
        self.ttl = base_ttl
        self.base_ttl = base_ttl
    
    def should_be_removed(self) -> bool:
        """
        Check if the object should be removed from the simulation.

        args:
            None
        returns:
            True if the object should be removed, False otherwise
        """
        return self.ttl is not None and self.ttl <= 0

    def reset_ttl(self) -> None:
        """
        Reset the ttl of the object.

        args:
            None
        returns:
            None, reset the ttl of the object
        """
        self.ttl = self.base_ttl

    def get_next_position(self, gol_grid: 'GOLGrid') -> Tuple[int, int]:
        """
        Get the new position of the object.

        args:
            grid: The grid object of the simulation.
        returns:
            The new position of the object.
        """
        pass

    def update(self, gol_grid: 'GOLGrid') -> Tuple[bool, int, int]:
        """
        Update the object.

        args:
            grid: The grid object of the simulation.
        returns:
            keep: a boolean indicating if the object should be kept in the simulation.
            new_x: the new x position of the object.
            new_y: the new y position of the object.
        """
        pass


