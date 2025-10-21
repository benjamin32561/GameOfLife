from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid


class BaseAlert:
    """
    Base class for all alert types in the simulation.
    Alerts monitor the simulation state and generate messages based on conditions.
    """
    
    def __init__(self, save_path: Optional[str] = None) -> None:
        """
        Initialize the base alert with an empty message and optional save path.
        
        Args:
            save_path: Optional path to save alert data to disk
        """
        self.message = ""
        self.save_path = save_path

    def save_to_disk(self) -> None:
        """
        Save the alert data to disk.
        
        Default implementation does nothing - subclasses override if they need to save.
        """
        pass

    def get_message(self, gol_grid: 'GOLGrid') -> Optional[str]:
        """
        Get the alert message based on the current grid state.
        
        Args:
            gol_grid: The grid object of the simulation
            
        Returns:
            Alert message string if condition is met, None otherwise
        """
        pass