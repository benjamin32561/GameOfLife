from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid

from alerts.base_alert import BaseAlert


class TimelineSummaryAlert(BaseAlert):
    """
    Alert for writing a summary of events to a file.
    """
    
    def __init__(self, save_path: str) -> None:
        """
        Initialize alert for tracking timeline events.

        Args:
            save_path: Optional path to save timeline summary to disk
            
        Returns:
            None, initialized the alert
        """
        super().__init__(save_path=save_path)
        self.message = "Timeline summary"
        self.step = 0
        self.events = []
        """
        events is a list of tuples, each tuple contains:
        - step: the step number
        - description: a description of the event
        """
        self.previous_statistics = None
    
    def check_events(self, current_statistics: dict) -> None:
        """
        Compare the current statistics to the previous statistics.
        Handles nested structure with 'population' and 'events'.
        """
        if self.previous_statistics is None:
            self.previous_statistics = {
                'population': current_statistics['population'].copy(),
                'events': current_statistics['events'].copy()
            }
            return
        
        # Track population changes
        for key, value in current_statistics['population'].items():
            if key == 'total':  # Skip total, it's calculated
                continue
            prev_value = self.previous_statistics['population'].get(key, 0)
            if value != prev_value:
                self.events.append((self.step, f"{key.capitalize()} population changed from {prev_value} to {value}"))
                self.previous_statistics['population'][key] = value
        
        # Track significant events (new events since last check)
        for key, value in current_statistics['events'].items():
            prev_value = self.previous_statistics['events'].get(key, 0)
            if value > prev_value:
                count = value - prev_value
                event_name = key.replace('_', ' ').title()
                self.events.append((self.step, f"{event_name}: {count} (total: {value})"))
                self.previous_statistics['events'][key] = value

    def save_to_disk(self) -> None:
        """
        Save the timeline summary to disk.
        """
        if not self.save_path or not self.events:
            return
        
        with open(self.save_path, 'w') as f:
            f.write("Timeline Summary - Simulation Events\n")
            f.write("=" * 50 + "\n\n")
            for step, description in self.events:
                f.write(f"Step {step}: {description}\n")
    
    def get_message(self, gol_grid: 'GOLGrid') -> Optional[str]:
        """
        Track events during the simulation.
        
        Args:
            gol_grid: The grid object of the simulation
            
        Returns:
            None, just collecting events
        """
        self.step += 1
        self.check_events(gol_grid.get_grid_stats())
        
        return None

