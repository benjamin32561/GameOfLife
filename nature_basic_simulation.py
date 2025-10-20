"""
Nature Ecosystem Simulation
Sprint 2: Predator-Prey-Plant ecosystem simulation
"""
import os
import sys
from time import sleep

import cv2
import numpy as np

from entities.GOLGrid import GOLGrid
from entities.Herbivore import Herbivore
from entities.Plant import Plant
from entities.Predator import Predator

# Hard-coded configuration
CONFIG_FILE = "nature_example.yaml"
DELAY_BETWEEN_STEPS = 0.0  # seconds
CELL_SIZE = 40  # pixels
OUTPUT_VIDEO = "t.mp4"  # Set to filename like "output.mp4" to record video


def main() -> None:
    """
    Main entry point - run the nature ecosystem simulation.
    """
    
    # Load configuration and initialize grid
    print(f"Loading configuration from: {CONFIG_FILE}")
    gol_grid = GOLGrid(CONFIG_FILE)
    
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
        first_frame = gol_grid.grid_to_image(cell_size=CELL_SIZE)
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
        
        # Write frame to video if recording
        if video_writer:
            frame = gol_grid.grid_to_image(cell_size=CELL_SIZE)
            video_writer.write(frame)
        
        # Check if ecosystem is extinct
        stats = gol_grid.get_grid_stats()
        if stats['plants'] == 0 and stats['herbivores'] == 0 and stats['predators'] == 0:
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
    print(f"  Plants: {final_stats['plants']}")
    print(f"  Herbivores: {final_stats['herbivores']}")
    print(f"  Predators: {final_stats['predators']}")


if __name__ == "__main__":
    main()