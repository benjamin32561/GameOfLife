from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid

from alerts.base_alert import BaseAlert


class PredatorEatsHerbivoreAlert(BaseAlert):
    """
    Alert triggered when a predator eats a herbivore.
    Uses the statistics system to track herbivore consumption events.
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
        self.message = "A Predator ate a Herbivore"
        self.previous_herbivores_eaten = 0
    
    def get_message(self, gol_grid: 'GOLGrid') -> Optional[str]:
        """
        Detect if a predator ate a herbivore using the statistics system.
        The grid tracks 'herbivore_eaten_by_predator' events automatically.

        Args:
            gol_grid: The grid object of the simulation

        Returns:
            Alert message if a herbivore was eaten since last check, None otherwise
        """
        grid_stats = gol_grid.get_grid_stats()
        events = grid_stats['events']
        current_herbivores_eaten = events.get('herbivore_eaten_by_predator', 0)
        
        # Check if herbivores were eaten since last check
        if current_herbivores_eaten > self.previous_herbivores_eaten:
            count = current_herbivores_eaten - self.previous_herbivores_eaten
            self.previous_herbivores_eaten = current_herbivores_eaten
            if count == 1:
                return self.message
            else:
                return f"Predators ate {count} Herbivores"
        
        self.previous_herbivores_eaten = current_herbivores_eaten
        return None

