from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid

from alerts.base_alert import BaseAlert


class ZeroStatsAlert(BaseAlert):
    """
    Alert triggered when a specific entity type reaches zero population.
    """
    
    def __init__(self, stats_type: str) -> None:
        """
        Initialize alert for tracking entity extinction.

        Args:
            stats_type: The type of entity to alert on ('plants', 'herbivores', or 'predators')
            
        Returns:
            None, initialized the alert
        """
        super().__init__(save_path=None)
        self.stats_type = stats_type
        self.message = f"No {stats_type} entities left"
    
    def get_message(self, gol_grid: 'GOLGrid') -> Optional[str]:
        """
        Check if the specified entity type has reached zero population.
        
        Args:
            gol_grid: The grid object of the simulation
            
        Returns:
            Alert message if entity count is zero, None otherwise
        """
        grid_stats = gol_grid.get_grid_stats()
        return self.message if grid_stats[self.stats_type] == 0 else None

