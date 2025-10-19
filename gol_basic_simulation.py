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


def main():
    """
    Main entry point - testing load and display functions.
    """
    if len(sys.argv) < 2:
        print("Usage: python gol_basic_simulation.py <initial_state_file>")
        print("\nExample:")
        print("  python gol_basic_simulation.py init_states/glider.txt")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    try:
        # Load initial state
        print(f"Loading initial state from: {filepath}\n")
        grid = load_grid_from_file(filepath)
        
        # Display the loaded grid
        display_grid(grid, 0)
        
        # Print grid dimensions
        height = len(grid)
        width = len(grid[0]) if height > 0 else 0
        print(f"Grid dimensions: {height} rows x {width} columns")
        
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
