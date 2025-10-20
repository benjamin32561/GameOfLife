from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid


class BaseAlert:
    """
    Base class for all alert types in the simulation.
    Alerts monitor the simulation state and generate messages based on conditions.
    """
    
    def __init__(self) -> None:
        """
        Initialize the base alert with an empty message.
        """
        self.message = ""

    def get_message(self, gol_grid: 'GOLGrid') -> Optional[str]:
        """
        Get the alert message based on the current grid state.
        
        Args:
            gol_grid: The grid object of the simulation
            
        Returns:
            Alert message string if condition is met, None otherwise
        """
        pass