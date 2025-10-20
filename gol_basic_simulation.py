"""
Conway's Game of Life - Basic Simulation
Sprint 1: Simple single-file implementation
"""
import os
import sys
from time import sleep
from typing import List, Optional

import cv2
import numpy as np


def load_grid_from_file(filepath: str) -> List[List[int]]:
    """
    Load initial grid state from a text file.
    
    Args:
        filepath: Path to the text file
        
    Returns:
        2D list representing the grid (0 = dead, 1 = alive)
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Remove empty lines and strip whitespace
    lines = [line.rstrip() for line in lines if line.strip()]
    
    # Convert to 2D list of integers
    grid = []
    for line in lines:
        row = [1 if char == '1' else 0 for char in line]
        grid.append(row)
    
    return grid


def display_grid(grid: List[List[int]], generation: int) -> None:
    """
    Display the grid in the console.
    
    Args:
        grid: 2D list representing the grid
        generation: Current generation number
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    print(f"Generation {generation}:")
    
    # Top border
    print("+" + "-" * width + "+")
    
    # Grid rows
    for row in grid:
        print("|" + "".join(str(cell) for cell in row) + "|")
    
    # Bottom border
    print("+" + "-" * width + "+")
    print()


def count_live_neighbors(grid: List[List[int]], x: int, y: int) -> int:
    """
    Count the number of live neighbors for a cell at position (x, y).
    Uses 8-connectivity (all 8 surrounding cells).
    
    Args:
        grid: 2D list representing the grid
        x: Row index
        y: Column index
        
    Returns:
        Number of live neighbors
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    count = 0
    
    # Check all 8 neighbors
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            # Skip the cell itself
            if dx == 0 and dy == 0:
                continue
            
            neighbor_x = x + dx
            neighbor_y = y + dy
            
            # Check if neighbor is within bounds
            if 0 <= neighbor_x < height and 0 <= neighbor_y < width:
                if grid[neighbor_x][neighbor_y] == 1:
                    count += 1
    
    return count


def apply_rules(grid: List[List[int]], x: int, y: int) -> int:
    """
    Apply Conway's Game of Life rules to determine the next state of a cell.
    
    Rules:
    - Any live cell with fewer than two live neighbours dies
    - Any live cell with two or three live neighbours lives
    - Any live cell with more than three live neighbours dies
    - Any dead cell with exactly three live neighbours becomes alive
    
    Args:
        grid: Current grid state
        x: Row index
        y: Column index
        
    Returns:
        Next state of the cell (0 or 1)
    """
    current_state = grid[x][y]
    live_neighbors = count_live_neighbors(grid, x, y)
    
    if current_state == 1:
        # Cell is currently alive
        if live_neighbors < 2:
            return 0  # Dies from underpopulation
        elif live_neighbors in (2, 3):
            return 1  # Survives
        else:
            return 0  # Dies from overpopulation
    else:
        # Cell is currently dead
        if live_neighbors == 3:
            return 1  # Becomes alive through reproduction
        else:
            return 0  # Stays dead


def step(grid: List[List[int]]) -> List[List[int]]:
    """
    Execute one step of the simulation.
    Creates a fresh grid and updates it based on the current grid.
    
    Args:
        grid: Current grid state
        
    Returns:
        New grid with next generation state
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    # Create a fresh grid for the next generation
    next_grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Update each cell based on current state
    # Iterate top to bottom, left to right
    for x in range(height):
        for y in range(width):
            next_grid[x][y] = apply_rules(grid, x, y)
    
    return next_grid


def grid_to_image(grid: List[List[int]], cell_size: int = 20) -> np.ndarray:
    """
    Convert grid to an image.
    
    Args:
        grid: 2D list representing the grid
        cell_size: Size of each cell in pixels
        
    Returns:
        numpy array representing the image (BGR format)
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    
    # Create image (height * cell_size, width * cell_size, 3 channels)
    img_height = height * cell_size
    img_width = width * cell_size
    image = np.zeros((img_height, img_width, 3), dtype=np.uint8)
    
    # Fill cells
    for row in range(height):
        for col in range(width):
            y1 = row * cell_size
            y2 = y1 + cell_size
            x1 = col * cell_size
            x2 = x1 + cell_size
            
            # White for alive, black for dead
            if grid[row][col] == 1:
                image[y1:y2, x1:x2] = [255, 255, 255]  # White (BGR)
            else:
                image[y1:y2, x1:x2] = [0, 0, 0]  # Black (BGR)
            
            # Draw grid lines (gray)
            cv2.rectangle(image, (x1, y1), (x2-1, y2-1), (50, 50, 50), 1)
    
    return image


def main() -> None:
    """
    Main entry point - run the Game of Life simulation.
    """
    if len(sys.argv) < 2:
        print("Usage: python gol_basic_simulation.py <initial_state_file> [num_steps] [output_video]")
        print("\nExample:")
        print("  python gol_basic_simulation.py init_states/glider.txt 10")
        print("  python gol_basic_simulation.py init_states/glider.txt 50 output.mp4")
        print("\nArguments:")
        print("  initial_state_file: Path to txt file with initial configuration")
        print("  num_steps: Number of generations to run (default: 10)")
        print("  output_video: Optional path to save video file")
        sys.exit(1)
    
    filepath = sys.argv[1]
    num_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    output_video = sys.argv[3] if len(sys.argv) > 3 else None
    
    try:
        # Load initial state
        print(f"Loading initial state from: {filepath}")
        grid = load_grid_from_file(filepath)
        
        print("Conway's Game of Life - Basic Simulation")
        print("=" * 50)
        print(f"Running for {num_steps} generations\n")
        
        # Setup video writer if output file specified
        video_writer = None
        if output_video:
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_video)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Get first frame to determine size
            first_frame = grid_to_image(grid, cell_size=20)
            height, width = first_frame.shape[:2]
            
            # Setup video writer (5 fps as requested)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(output_video, fourcc, 5.0, (width, height))
            
            print(f"Recording video to: {output_video}")
            print(f"Video settings: {width}x{height} @ 5 fps\n")
            
            # Write first frame
            video_writer.write(first_frame)
        
        # Display initial state (generation 0)
        display_grid(grid, 0)
        
        # Run simulation for num_steps generations
        for t in range(1, num_steps + 1):
            # Create a fresh grid and update based on current grid
            grid = step(grid)
            
            # Display the new generation
            display_grid(grid, t)
            
            # Write frame to video if recording
            if video_writer:
                frame = grid_to_image(grid, cell_size=20)
                video_writer.write(frame)
            
            sleep(0.1)
        
        # Release video writer
        if video_writer:
            video_writer.release()
            print(f"\n✓ Video saved to: {output_video}")
        
        print("\nSimulation complete!")
        
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
