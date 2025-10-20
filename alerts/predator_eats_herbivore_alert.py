from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid

from alerts.base_alert import BaseAlert
from entities.herbivore import Herbivore


class PredatorEatsHerbivoreAlert(BaseAlert):
    """
    Alert triggered when a predator eats a herbivore.
    Tracks herbivore positions between steps to detect consumption.
    """
    
    def __init__(self) -> None:
        """
        Initialize alert for tracking predator-herbivore interactions.

        Args:
            None
            
        Returns:
            None, initialized the alert
        """
        super().__init__()
        self.message = "A Predator ate an Herbivore"
        self.previous_herbivore_coordinates = []
    
    def get_message(self, gol_grid: 'GOLGrid') -> Optional[str]:
        """
        Detect if a predator ate a herbivore by comparing positions.
        This alert keeps the locations of all herbivores from the previous step.
        If a predator is now located where an herbivore was, one was eaten.

        Args:
            gol_grid: The grid object of the simulation

        Returns:
            Alert message if a herbivore was eaten, None otherwise
        """
        to_ret = None

        current_herbivore_coordinates = gol_grid.get_all_cells_with_type(Herbivore)
        if self.previous_herbivore_coordinates:
            for x, y in self.previous_herbivore_coordinates:
                if (x, y) not in current_herbivore_coordinates:
                    to_ret = self.message
                    break
        
        self.previous_herbivore_coordinates = current_herbivore_coordinates
        return to_ret

