from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid

from alerts.base_alert import BaseAlert


class ExampleAlert(BaseAlert):
    """
    Alert triggered when a specific example alert is triggered.
    """
    
    def __init__(self, save_path: Optional[str] = None) -> None:
        """
        Initialize alert for tracking example alert.

        Args:
            save_path: Optional path to save alert data (not used for this alert type)
            
        Returns:
            None, initialized the alert
        """
        super().__init__(save_path=save_path)
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

