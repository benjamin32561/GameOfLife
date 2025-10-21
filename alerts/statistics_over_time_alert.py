from typing import TYPE_CHECKING, Optional, List

import matplotlib.pyplot as plt
import numpy as np

if TYPE_CHECKING:
    from entities.gol_grid import GOLGrid

from alerts.base_alert import BaseAlert


class StatisticsOverTimeAlert(BaseAlert):
    """
    Thie is an alert module for creating a lineplot of the statistics of the simulation over time.
    """
    
    def __init__(self, save_fig_path: str, keys_to_plot: Optional[List[str]] = None) -> None:
        """
        Initialize alert for tracking statistics over time of the simulation.

        Args:
            save_fig_path: The path to save the figure to
            keys_to_plot: The keys to plot, if None, all keys will be plotted. Keys must be in the grid_stats of the simulation.
            
        Returns:
            None, initialized the alert
        """
        super().__init__()
        self.message = "Statistics over time"
        self.save_fig_path = save_fig_path
        self.statistics_over_time = {}
        self.keys_to_plot = keys_to_plot

    def create_graph(self) -> None:
        """
        Create the graph with the new statistics.

        Args:
            None

        Returns:
            None, updated the graph with the new statistics
        """

        # Get the number of steps (assuming all keys have same length)
        first_key = list(self.statistics_over_time.keys())[0]
        t = np.arange(len(self.statistics_over_time[first_key]))
        
        plt.figure(figsize=(10, 6))
        for key in self.statistics_over_time.keys():
            if self.keys_to_plot is not None and key not in self.keys_to_plot:
                continue
            plt.plot(t, self.statistics_over_time[key], label=key.replace('_', ' ').title(), linewidth=2)
        
        plt.xlabel('Simulation Step', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.title('Statistics Over Time', fontsize=14, fontweight='bold')
        plt.legend(loc='best', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.save_fig_path, dpi=150)
        plt.close()
    
    def get_message(self, gol_grid: 'GOLGrid') -> Optional[str]:
        """
        Collect statistics at each step (but don't generate plot yet).
        
        Args:
            gol_grid: The grid object of the simulation
            
        Returns:
            None, just collecting data
        """
        current_stats = gol_grid.get_grid_stats()
        for key in current_stats.keys():
            if key not in self.statistics_over_time:
                self.statistics_over_time[key] = []
            self.statistics_over_time[key].append(current_stats[key])
        return None

