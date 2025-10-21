"""
Nature Ecosystem Simulation
Sprint 2: Predator-Prey-Plant ecosystem simulation
"""
import os
import sys
from time import sleep

import cv2
import numpy as np

from alerts.alert_manager import AlertManager
from alerts.entity_above_threshold_alert import EntityAboveThreshold
from alerts.predator_eats_herbivore_alert import PredatorEatsHerbivoreAlert
from alerts.zero_stats_alert import ZeroStatsAlert
from entities.gol_grid import GOLGrid
from entities.herbivore import Herbivore
from entities.plant import Plant
from entities.predator import Predator

# Hard-coded configuration
CONFIG_FILE = "nature_example.yaml"
DELAY_BETWEEN_STEPS = 0.0  # seconds
OUTPUT_VIDEO = "t.mp4"  # Set to filename like "output.mp4" to record video


def main() -> None:
    """
    Main entry point - run the nature ecosystem simulation.
    """
    
    # Load configuration and initialize grid
    print(f"Loading configuration from: {CONFIG_FILE}")
    gol_grid = GOLGrid(CONFIG_FILE)
    
    # Setup alert system
    alert_manager = AlertManager()
    alert_manager.add_alert(ZeroStatsAlert('plants'))
    alert_manager.add_alert(ZeroStatsAlert('herbivores'))
    alert_manager.add_alert(ZeroStatsAlert('predators'))
    alert_manager.add_alert(PredatorEatsHerbivoreAlert())
    alert_manager.add_alert(EntityAboveThreshold('herbivores', 0.3))  # Alert when >30% of cells have herbivores
    alert_manager.add_alert(EntityAboveThreshold('predators', 0.15))  # Alert when >15% of cells have predators
    
    num_steps = gol_grid.config['simulation']['steps']
    
    print("Nature Ecosystem Simulation")
    print("=" * 60)
    print(f"Grid size: {gol_grid.width} x {gol_grid.height}")
    print(f"Running for {num_steps} steps")
    print(f"Delay between steps: {DELAY_BETWEEN_STEPS}s")
    print("\nLegend:")
    print("  P = Plant (green)")
    print("  H = Herbivore (yellow)")
    print("  X = Predator (red)")
    print("  . = Empty cell")
    print("  # = Multiple entities\n")
    
    # Setup video writer if output file specified
    video_writer = None
    if OUTPUT_VIDEO:
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(OUTPUT_VIDEO)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Get first frame to determine size
        first_frame = gol_grid.grid_to_image()
        height, width = first_frame.shape[:2]
        
        # Setup video writer (5 fps)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, 4.0, (width, height))
        
        print(f"Recording video to: {OUTPUT_VIDEO}")
        print(f"Video settings: {width}x{height} @ 4 fps\n")
        
        # Write first frame
        video_writer.write(first_frame)
    
    # Display initial state (step 0)
    print(f"\nStep 0:")
    gol_grid.print_grid()
    
    # Run simulation
    for step in range(1, num_steps + 1):
        # Update the grid
        gol_grid.update()
        
        # Display the new state
        print(f"\nStep {step}:")
        gol_grid.print_grid()
        
        # Check and print alerts
        alert_manager.print_alerts(gol_grid)
        
        # Write frame to video if recording
        if video_writer:
            frame = gol_grid.grid_to_image()
            video_writer.write(frame)
        
        # Check if ecosystem is extinct
        stats = gol_grid.get_grid_stats()
        population = stats['population']
        if population.get('plant', 0) == 0 and population.get('herbivore', 0) == 0 and population.get('predator', 0) == 0:
            print("\n*** Ecosystem extinct! Simulation ended early. ***")
            break
        
        sleep(DELAY_BETWEEN_STEPS)
    
    # Release video writer
    if video_writer:
        video_writer.release()
        print(f"\n✓ Video saved to: {OUTPUT_VIDEO}")
    
    print("\nSimulation complete!")
    print("\nFinal statistics:")
    final_stats = gol_grid.get_grid_stats()
    print(f"  Population: {final_stats['population']}")
    print(f"  Events: {final_stats['events']}")


if __name__ == "__main__":
    main()