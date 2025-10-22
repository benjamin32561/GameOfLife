from typing import TYPE_CHECKING, Optional, Tuple

from entities.mobile_entity import MobileEntity
from entities.herbivore import Herbivore
from entities.plant import Plant
from entities.predator import Predator

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid


class Omnivore(MobileEntity):
    def __init__(self, x: int, y: int, base_ttl: Optional[int] = None, sight_radius: Optional[int] = None, T_cooldown: Optional[int] = None) -> None:
        """
        Omnivore object class.

        Omnivores die after T_omnivore steps 
        Omnivores move towards the closest plant/herbivore/predator they can see in a (R_omnivore_sight) radius, if they don’t have a plant/herbivore/predator in sight, they move randomly.
        When an omnivore reaches a plant/herbivore/predator, it eats it, refueling its life span
        Omnivores reproduce when reaching another omnivore, staying in the same space and spawning another omnivore in a random neighboring cell.
        After reproducing, they can’t reproduce anymore for mating_cool_down steps.
        """
        super().__init__(x, y, base_ttl, sight_radius)
        self.mating_cool_down = 0
        self.base_mating_cool_down = T_cooldown
    
    def can_mate(self) -> bool:
        """
        Check if the omnivore can mate.
        """
        return self.mating_cool_down <= 0

    def reset_mating_cooldown(self) -> None:
        """
        Reset the mating cooldown of the omnivore.
        """
        self.mating_cool_down = self.base_mating_cool_down
    
    def update(self, gol_grid: 'GOLGrid') -> Tuple[bool, int, int]:
        """
        Update the omnivore.

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

        # move towards the closest plant or randomly
        new_x, new_y = self.get_next_position(gol_grid, [Plant, Herbivore, Predator])

        # check if cell contains a plant, herbivore or predator, if so, eat it
        is_plant = gol_grid.is_object_type_in_cell(new_x, new_y, Plant)
        is_herbivore = gol_grid.is_object_type_in_cell(new_x, new_y, Herbivore)
        is_predator = gol_grid.is_object_type_in_cell(new_x, new_y, Predator)
        if is_plant or is_herbivore or is_predator:
            objects_eaten = sum([len([obj for obj in gol_grid.grid[new_x][new_y] if isinstance(obj, obj_type)]) for obj_type in [Plant, Herbivore, Predator]])
            gol_grid.grid[new_x][new_y] = [obj for obj in gol_grid.grid[new_x][new_y] if not isinstance(obj, Plant) and not isinstance(obj, Herbivore) and not isinstance(obj, Predator)]
            self.reset_ttl()
            if is_plant:
                gol_grid.record_stat('plant_eaten_by_omnivore', 1)
            elif is_herbivore:
                gol_grid.record_stat('herbivore_eaten_by_omnivore', 1)
            elif is_predator:
                gol_grid.record_stat('predator_eaten_by_omnivore', 1)
        
        # check if next position contains a omnivore, if so,
        # reproduce, spawning another omnivore in a random neighboring cell.
        if gol_grid.is_object_type_in_cell(new_x, new_y, Omnivore) and self.can_mate():
            # check if there is at least one other omnivore in the cell that can mate, if so,
            # reproduce, reset their cooldown and create a new omnivore
            mateable_omnivores = [omnivore for omnivore in gol_grid.grid[new_x][new_y] if isinstance(omnivore, Omnivore) and omnivore.can_mate()]

            if len(mateable_omnivores) >= 1:
                mate_omnivore = mateable_omnivores[0]
                # reset mating cooldown for both omnivores
                mate_omnivore.reset_mating_cooldown()
                self.reset_mating_cooldown()

                # generate a new omnivore in the grid
                success = gol_grid.add_entity_in_range(Omnivore, new_x, new_y, range_distance=1, exclude_center=True)
                if success:
                    gol_grid.record_stat('omnivore_reproduced', 1)

        return True, new_x, new_y