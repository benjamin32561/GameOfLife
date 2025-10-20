from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid

from alerts.base_alert import BaseAlert


class EntityAboveThreshold(BaseAlert):
    """
    Alert triggered when an entity type's population exceeds a threshold.
    Can use normalized density (per cell) or absolute count.
    """
    
    def __init__(self, entity: str, threshold: float, norm: bool = True) -> None:
        """
        Initialize alert for tracking entity population thresholds.

        Args:
            entity: The type of entity to monitor ('plants', 'herbivores', or 'predators')
            threshold: If norm=True, this is density (0.0-1.0, entities per cell)
                      If norm=False, this is absolute count
            norm: If True, normalize threshold by grid size (density-based)
                 If False, use absolute count
            
        Returns:
            None, initialized the alert
        """
        super().__init__()
        self.entity = entity
        self.threshold = threshold
        self.norm = norm
        self.alerted = False  # Track if we've already alerted to avoid spam
    
    def _check_normalized_threshold(self, gol_grid: 'GOLGrid', current_count: int) -> Optional[str]:
        """
        Check threshold using normalized density (entities per cell).

        Args:
            gol_grid: The grid object of the simulation
            current_count: Current entity count

        Returns:
            Alert message if threshold exceeded, None otherwise
        """
        grid_size = gol_grid.width * gol_grid.height
        current_density = current_count / grid_size
        threshold_exceeded = current_density > self.threshold
        
        if threshold_exceeded and not self.alerted:
            self.alerted = True
            self.message = f"{self.entity.capitalize()} density exceeded {self.threshold:.2%} (current: {current_density:.2%}, count: {current_count}/{grid_size} cells)"
            return self.message
        elif not threshold_exceeded:
            self.alerted = False
        
        return None
    
    def _check_absolute_threshold(self, current_count: int) -> Optional[str]:
        """
        Check threshold using absolute entity count.

        Args:
            current_count: Current entity count

        Returns:
            Alert message if threshold exceeded, None otherwise
        """
        threshold_exceeded = current_count > self.threshold
        
        if threshold_exceeded and not self.alerted:
            self.alerted = True
            self.message = f"{self.entity.capitalize()} population exceeded {int(self.threshold)} (current: {current_count})"
            return self.message
        elif not threshold_exceeded:
            self.alerted = False
        
        return None
    
    def get_message(self, gol_grid: 'GOLGrid') -> Optional[str]:
        """
        Check if the entity population exceeds the threshold.
        Only alerts once when crossing the threshold to avoid repeated messages.
        Delegates to normalized or absolute threshold check based on configuration.

        Args:
            gol_grid: The grid object of the simulation

        Returns:
            Alert message if threshold is exceeded (first time), None otherwise
        """
        grid_stats = gol_grid.get_grid_stats()
        current_count = grid_stats[self.entity]
        
        if self.norm:
            return self._check_normalized_threshold(gol_grid, current_count)
        else:
            return self._check_absolute_threshold(current_count)

