from itertools import product
import yaml
import math
import random


class Entity:
    def __init__(self, x, y, base_ttl=None):
        """
        Base object class.
        """
        self.x = x
        self.y = y
        self.ttl = base_ttl
        self.base_ttl = base_ttl
    
    def should_be_removed(self):
        """
        Check if the object should be removed from the simulation.

        args:
            None
        returns:
            True if the object should be removed, False otherwise
        """
        return self.ttl is not None and self.ttl <= 0

    def reset_ttl(self):
        """
        Reset the ttl of the object.

        args:
            None
        returns:
            None, reset the ttl of the object
        """
        self.ttl = self.base_ttl

    def get_next_position(self, gol_grid):
        """
        Get the new position of the object.

        args:
            grid: The grid object of the simulation.
        returns:
            The new position of the object.
        """
        pass

    def update(self, gol_grid):
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


