"""
Conway's Game of Life - Basic Simulation
Sprint 1: Simple single-file implementation
"""

import sys


def load_grid_from_file(filepath):
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


def display_grid(grid, generation):
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


def count_live_neighbors(grid, x, y):
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


def apply_rules(grid, x, y):
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


def step(grid):
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


def main():
    """
    Main entry point - run the Game of Life simulation.
    """
    if len(sys.argv) < 2:
        print("Usage: python gol_basic_simulation.py <initial_state_file> [num_steps]")
        print("\nExample:")
        print("  python gol_basic_simulation.py init_states/glider.txt 10")
        print("\nArguments:")
        print("  initial_state_file: Path to txt file with initial configuration")
        print("  num_steps: Number of generations to run (default: 10)")
        sys.exit(1)
    
    filepath = sys.argv[1]
    num_steps = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    try:
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
        
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
