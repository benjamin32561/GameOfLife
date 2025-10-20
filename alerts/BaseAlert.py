from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities.GOLGrid import GOLGrid

class BaseAlert:
    def __init__(self) -> None:
        self.message = ""

    def get_message(self, gol_grid: 'GOLGrid') -> str:
        pass

"""
Alert when a Predator eats an Herbivore.
Alert when the number of plants exceeds 90% of the grid space.
The alerts should be printed to the console or logged appropriately.
"""

class ZeroStatsAlert(BaseAlert):
    def __init__(self, stats_type: str) -> None:
        """
        Alert when no more of a certain entity is alive.

        args:
            stats_type: the type of entity to alert on (plants, herbivores, predators)
        returns:
            None, initialized the alert
        """
        super().__init__()
        self.message = f"No {stats_type} entities left"
    
    def get_message(self, gol_grid: 'GOLGrid') -> str:
        grid_stats = gol_grid.get_grid_stats()
        return self.message if grid_stats[self.stats_type] == 0 else None

class PredatorEatsHerbivoreAlert(BaseAlert):
    def __init__(self) -> None:
        """
        Alert when a Predator eats an Herbivore.

        args:
            None
        returns:
            None, initialized the alert
        """
        super().__init__()
        self.message = "A Predator ate an Herbivore"
        self.previous_herbivore_coordinates = []
    
    def get_message(self, gol_grid: 'GOLGrid') -> str:
        