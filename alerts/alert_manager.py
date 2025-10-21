from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid

from alerts.base_alert import BaseAlert


class AlertManager:
    """
    Manages multiple alerts and processes them during simulation.
    """
    
    def __init__(self) -> None:
        """
        Initialize the alert manager with an empty list of alerts.
        """
        self.alerts: List[BaseAlert] = []
    
    def add_alert(self, alert: BaseAlert) -> None:
        """
        Add an alert to the manager.
        
        Args:
            alert: The alert instance to add
        """
        self.alerts.append(alert)
    
    def check_alerts(self, gol_grid: 'GOLGrid') -> List[str]:
        """
        Check all alerts and collect messages.
        
        Args:
            gol_grid: The grid object of the simulation
            
        Returns:
            List of alert messages that were triggered
        """
        messages = []
        for alert in self.alerts:
            message = alert.get_message(gol_grid)
            if message:
                messages.append(message)
        return messages
    
    def print_alerts(self, gol_grid: 'GOLGrid') -> None:
        """
        Check alerts and print any triggered messages.
        
        Args:
            gol_grid: The grid object of the simulation
        """
        messages = self.check_alerts(gol_grid)
        for message in messages:
            print(f"⚠️  ALERT: {message}")
    
    def save_all(self) -> None:
        """
        Save all alerts to disk.
        Calls save_to_disk() on each alert (which may be a no-op for some alerts).
        """
        for alert in self.alerts:
            alert.save_to_disk()

