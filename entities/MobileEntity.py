import math
import random
from typing import TYPE_CHECKING, Optional, Tuple, Type

from .Entity import Entity

if TYPE_CHECKING:
    from .GOLGrid import GOLGrid


class MobileEntity(Entity):
    def __init__(self, x: int, y: int, base_ttl: Optional[int] = None, sight_radius: Optional[int] = None) -> None:
        """
        Mobile entity object class.

        args:
            x: X position
            y: Y position
            base_ttl: Number of steps before dying (None = infinite)
            sight_radius: The radius of the sight of the entity.
        returns:
            None, initialized the mobile entity object
        """
        super().__init__(x, y, base_ttl)
        self.sight_radius = sight_radius

    def get_random_step(self, gol_grid: 'GOLGrid') -> Tuple[int, int]:
        """
        Get a random step for a given position.

        args:
            gol_grid: the grid object of the simulation
        returns:
            the x and y coordinates of the random step
        """
        all_possible_steps = gol_grid.get_all_possible_steps(self.x, self.y)
        return random.choice(all_possible_steps) 

    def get_closest_object_coordinates(self, gol_grid: 'GOLGrid', object_type: Type[Entity]) -> Tuple[int, int]:
        """
        Find the closest object of a given type.

        args:
            gol_grid: the grid object of the simulation
            object_type: the type of object to find

        returns:
            the x and y position of the closest object
            -1, -1 if no object is found
        """
        all_cells_with_objects = gol_grid.get_all_cells_with_type(object_type)
        
        # get closest one
        closest_coords = (-1, -1)
        closest_distance = float('inf')
        for x, y in all_cells_with_objects:
            distance = math.sqrt((self.x-x)**2+(self.y-y)**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_coords = (x, y)
        return closest_coords

    def get_next_position_towards_object(self, gol_grid: 'GOLGrid', target_x: int, target_y: int) -> Tuple[int, int]:
        """
        Get the next position moving one step towards a target.

        args:
            gol_grid: the grid object of the simulation
            target_x: the x position of the desired position to move towards
            target_y: the y position of the desired position to move towards
        returns:
            the x and y coordinates of the next position (one step from current position)
        """
        # Get all possible steps from CURRENT position (self.x, self.y)
        all_possible_steps = gol_grid.get_all_possible_steps(self.x, self.y)
        
        # Find which step gets us closest to the target
        closest_step = None
        closest_distance = float('inf')
        for step_x, step_y in all_possible_steps:
            # Calculate distance from this potential step to the target
            distance = math.sqrt((step_x - target_x)**2 + (step_y - target_y)**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_step = (step_x, step_y)
        return closest_step

    def get_next_position(self, gol_grid: 'GOLGrid', object_type: Type[Entity]) -> Tuple[int, int]:
        """
        Find the closest object of a given type in a given radius.

        args:
            gol_grid: The grid object of the simulation.
            object_type: The type of object to find.
        returns:
            The x and y coordinates of the closest object.
            -1, -1 if no object is found.
        """
        closest_object_x, closest_object_y = self.get_closest_object_coordinates(gol_grid, object_type)
        if closest_object_x != -1 and closest_object_y != -1:
            return self.get_next_position_towards_object(gol_grid, closest_object_x, closest_object_y)
        else:
            return self.get_random_step(gol_grid)
