from typing import TYPE_CHECKING, Optional, Tuple

from entities.herbivore import Herbivore
from entities.mobile_entity import MobileEntity

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid


class Predator(MobileEntity):
    def __init__(self, x: int, y: int, base_ttl: Optional[int] = None, sight_radius: Optional[int] = None) -> None:
        """
        Predator object class.
        """
        super().__init__(x, y, base_ttl, sight_radius)
    
    def update(self, gol_grid: 'GOLGrid') -> Tuple[bool, int, int]:
        """
        Update the predator.

        args:
            gol_grid: the grid object of the simulation
        returns:
            keep: a boolean indicating if the object should be kept in the simulation.
            new_x: the new x position of the object.
            new_y: the new y position of the object.
        """
        if self.should_be_removed():
            return False, -1, -1  # Remove from simulation
        
        # reduce ttl
        self.ttl -= 1

        # move towards the closest plant
        new_x, new_y = self.get_next_position(gol_grid, Herbivore)
        
        # check if next position contains a herbivore, if so,
        # remove it, and reset the ttl of the current predator
        if gol_grid.is_object_type_in_cell(new_x, new_y, Herbivore):
            herbivores_eaten = len([obj for obj in gol_grid.grid[new_x][new_y] if isinstance(obj, Herbivore)])
            gol_grid.grid[new_x][new_y] = [obj for obj in gol_grid.grid[new_x][new_y] if not isinstance(obj, Herbivore)]
            self.reset_ttl()
            gol_grid.record_stat('herbivore_eaten_by_predator', herbivores_eaten)

        return True, new_x, new_y