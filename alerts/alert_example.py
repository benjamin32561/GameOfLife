from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid

from alerts.base_alert import BaseAlert


class ExampleAlert(BaseAlert):
    """
    Alert triggered when a specific example alert is triggered.
    """
    
    def __init__(self) -> None:
        """
        Initialize alert for tracking example alert.

        Args:
            None
            
        Returns:
            None, initialized the alert
        """
        super().__init__()
        self.message = "Example alert"
    
    def get_message(self, gol_grid: 'GOLGrid') -> Optional[str]:
        """
        Check if the example alert is triggered.
        
        Args:
            gol_grid: The grid object of the simulation
            
        Returns:
            Alert message if example alert is triggered, None otherwise
        """
        return self.message

