"""
Conway's Game of Life - Basic Simulation
Sprint 1: Simple single-file implementation
"""

import sys
import argparse
from typing import List, Tuple
from itertools import product


def get_grid_dimensions(grid: List[List[int]]) -> Tuple[int, int]:
    """
    Get grid dimensions (height, width).
    
    Args:
        grid: 2D list representing the grid
        
    Returns:
        Tuple of (height, width)
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    return height, width


def is_valid_position(x: int, y: int, height: int, width: int) -> bool:
    """
    Check if position is within grid bounds.
    
    Args:
        x: Row index
        y: Column index
        height: Grid height
        width: Grid width
        
    Returns:
        True if position is valid, False otherwise
    """
    return 0 <= x < height and 0 <= y < width


def get_neighbor_offsets() -> List[Tuple[int, int]]:
    """
    Get all 8 neighbor offsets (excluding center).
    
    Returns:
        List of (dx, dy) tuples for 8-connectivity
    """
    return [(dx, dy) for dx, dy in product([-1, 0, 1], [-1, 0, 1]) 
            if not (dx == 0 and dy == 0)]


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
    height, width = get_grid_dimensions(grid)
    
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
    height, width = get_grid_dimensions(grid)
    count = 0
    
    # Check all 8 neighbors using itertools
    for dx, dy in get_neighbor_offsets():
        neighbor_x = x + dx
        neighbor_y = y + dy
        
        if is_valid_position(neighbor_x, neighbor_y, height, width):
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
    height, width = get_grid_dimensions(grid)
    
    # Create a fresh grid for the next generation
    next_grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Update each cell based on current state using itertools
    for x, y in product(range(height), range(width)):
        next_grid[x][y] = apply_rules(grid, x, y)
    
    return next_grid


def main() -> None:
    """
    Main entry point - run the Game of Life simulation.
    """
    parser = argparse.ArgumentParser(
        description="Conway's Game of Life - Basic Simulation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python gol_basic_simulation.py init_states/glider.txt
  python gol_basic_simulation.py init_states/glider.txt --steps 20
  python gol_basic_simulation.py init_states/pulsar.txt --steps 15
        """
    )
    
    parser.add_argument(
        'filepath',
        help='Path to txt file with initial configuration'
    )
    
    parser.add_argument(
        '--steps', '-s',
        type=int,
        default=10,
        help='Number of generations to run (default: 10)'
    )
    
    args = parser.parse_args()
    
    filepath = args.filepath
    num_steps = args.steps
    
    # Load initial state
    print(f"Loading initial state from: {filepath}")
    grid = load_grid_from_file(filepath)
        
    print("Conway's Game of Life - Basic Simulation")
    print("=" * 50)
    print(f"Running for {num_steps} generations\n")
    
    # Display initial state (generation 0)
    display_grid(grid, 0)
    
    # Run simulation for num_steps generations
    for t in range(1, num_steps + 1):
        # Create a fresh grid and update based on current grid
        grid = step(grid)
        # Display the new generation
        display_grid(grid, t)
    
    print("Simulation complete!")
       
if __name__ == "__main__":
    main()
