import random
from itertools import product
from typing import Any, Dict, List, Tuple, Type

import cv2
import numpy as np
import yaml

from entities.entity import Entity
from entities.entity_factory import EntityFactory
from entities.herbivore import Herbivore
from entities.plant import Plant
from entities.predator import Predator


def validate_coordinates(x: int, y: int, grid: List[List[List[Entity]]]) -> bool:
    """
    validate the coordinates of the object

    args:
        x: x coordinate
        y: y coordinate
        grid: the grid object of the simulation
    returns:
        True if the coordinates are valid, False otherwise
    """
    if x < 0 or x >= len(grid) or y < 0 or y >= len(grid[0]):
        return False
    return True

class GOLGrid:
    def __init__(self, init_file_path: str) -> None:
        """
        GOLGrid class.
        
        Args:
            init_file_path: Path to the YAML configuration file (required)
        
        Note: All configuration is loaded from the YAML file.
        """
        self.grid = None
        self.width = None
        self.height = None
        self.herbivore_reproductions = 0
        self.config = self.load_from_file(init_file_path)
        self.factory = EntityFactory(self.config)
        
        # Load all configuration from YAML
        self.order_to_process = self._load_order_to_process_from_config()
        self.random_spawn_config = self._load_random_spawn_config_from_config()
        self.entity_color_map = self._load_entity_color_map_from_config()
        self.visualization_settings = self._load_visualization_settings_from_config()
        
        # Initialize statistics tracking
        self.statistics = {}
        self.reset_statistics()
        
        self.init_grid_parameters(self.config)
        self.init_grid_state(self.config)
    
    def load_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load simulation configuration from YAML file.

        args:
            file_path: the path to the YAML file
        returns:
            the configuration
        """
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    
    def _load_order_to_process_from_config(self) -> List[Type[Entity]]:
        """
        Load entity processing order from YAML configuration.
        Converts string entity names to class types using the factory's mapping.
        Assumes YAML contains all required settings.
        
        Returns:
            List of entity types in processing order
        """
        entity_names = self.config['simulation']['order_to_process']
        entity_types = []
        for name in entity_names:
            entity_types.append(self.factory.ENTITY_TYPE_MAP[name])
        return entity_types
    
    def _load_random_spawn_config_from_config(self) -> Dict[Type[Entity], Dict[str, Any]]:
        """
        Load random spawn configuration from YAML.
        Converts string entity names to class types using the factory's mapping.
        Assumes YAML contains all required settings.
        
        Returns:
            Dictionary mapping entity types to spawn configuration
        """
        yaml_spawn_config = self.config['simulation']['random_spawn_config']
        spawn_config = {}
        for entity_name, params in yaml_spawn_config.items():
            spawn_config[self.factory.ENTITY_TYPE_MAP[entity_name]] = params
        return spawn_config
    
    def _load_entity_color_map_from_config(self) -> Dict[str, Tuple[int, int, int]]:
        """
        Load entity color map from YAML.
        Converts color arrays to tuples.
        Assumes YAML contains all required settings.
        
        Returns:
            Dictionary mapping entity type names (lowercase) to BGR color tuples
        """
        yaml_color_map = self.config['simulation']['entity_color_map']
        color_map = {}
        for entity_name, color in yaml_color_map.items():
            # Convert list to tuple (YAML arrays become Python lists)
            color_map[entity_name.lower()] = tuple(color)
        return color_map
    
    def _load_visualization_settings_from_config(self) -> Dict[str, Any]:
        """
        Load visualization settings from YAML.
        Converts color arrays to tuples.
        Assumes YAML contains all required settings.
        
        Returns:
            Dictionary with visualization settings
        """
        vis_config = self.config['simulation']['visualization']
        return {
            'cell_size': vis_config['cell_size'],
            'empty_cell_color': tuple(vis_config['empty_cell_color']),
            'background_color': tuple(vis_config['background_color'])
        }

    def init_grid_parameters(self, config: Dict[str, Any]) -> None:
        """
        Initialize the grid parameters from the configuration.

        args:
            config: the configuration
        returns:
            None, initialized the grid parameters
        """
        self.width = config['simulation']['width']
        self.height = config['simulation']['height']
        self.grid = [[[] for _ in range(self.width)] for _ in range(self.height)]


    def init_grid_state(self, config: Dict[str, Any]) -> None:
        """
        Create initial state from configuration.
        The factory now handles the decision of which entities to create.
        
        args:
            config: the configuration (kept for interface consistency)
        returns:
            None, updated the internal grid with the initial state
        """
        # Let the factory decide which entities to create based on config
        entities = self.factory.create_initial_entities()
        
        # Place all entities in the grid
        for entity, x, y in entities:
            self.grid[x][y].append(entity)
    
    def get_all_possible_steps(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get all possible steps (step size is 1) for a given position.

        args:
            x: the x position of the entity
            y: the y position of the entity
        returns:
            list of all possible steps
        """
        x_range = range(max(0, x - 1), min(self.width, x + 2))
        y_range = range(max(0, y - 1), min(self.height, y + 2))
        all_possible_steps = [(x, y) for x, y in product(x_range, y_range) if validate_coordinates(x, y, self.grid)]
        return all_possible_steps

    def get_all_cells_with_type(self, object_type: Type[Entity]) -> List[Tuple[int, int]]:
        """
        Get all cell coordinates with an object of a given type.

        args:
            object_type: the type of object to find
        returns:
            list of cell coordinates
        """
        to_ret = []
        for x, y in product(range(self.width), range(self.height)):
            if any(isinstance(entity, object_type) for entity in self.grid[x][y]):
                to_ret.append((x,y))
        return to_ret

    def get_all_empty_cells(self) -> List[Tuple[int, int]]:
        """
        Get all empty cells in the grid.
        """
        return [(x, y) for x, y in product(range(self.width), range(self.height)) if len(self.grid[x][y]) == 0]
    
    def reset_statistics(self) -> None:
        """
        Reset all statistics to zero.
        This is called at initialization and can be called manually to reset tracking.
        Statistics are created dynamically as events occur, so this just clears the dictionary.
        """
        self.statistics = {}
    
    def record_stat(self, stat_name: str, value: int = 1) -> None:
        """
        Record a statistic event. Creates the stat if it doesn't exist.
        
        Args:
            stat_name: Name of the statistic to record
            value: Value to add to the statistic (default: 1)
        """
        if stat_name not in self.statistics:
            self.statistics[stat_name] = 0
        self.statistics[stat_name] += value

    def is_object_type_in_cell(self, x: int, y: int, object_type: Type[Entity]) -> bool:
        """
        Check if an object of a given type is in a given cell.
        """
        return len(self.grid[x][y]) > 0 and any(isinstance(entity, object_type) for entity in self.grid[x][y])

    def add_entity_in_range(self, entity_type: Type[Entity], center_x: int, center_y: int, 
                           range_distance: int = 0, exclude_center: bool = False,
                           only_empty_cells: bool = False) -> bool:
        """
        Add an entity of the specified type to a random cell within a given range.
        
        Args:
            entity_type: Type of entity to create (e.g., Plant, Herbivore, Predator)
            center_x: Center x coordinate
            center_y: Center y coordinate
            range_distance: Distance from center (0 = same cell, 1 = immediate neighbors, etc.)
            exclude_center: Whether to exclude the center cell from possible locations
            only_empty_cells: Whether to only consider empty cells
            
        Returns:
            True if entity was successfully added, False otherwise
        """
        # Calculate range bounds
        x_range = range(max(0, center_x - range_distance), min(self.width, center_x + range_distance + 1))
        y_range = range(max(0, center_y - range_distance), min(self.height, center_y + range_distance + 1))
        
        # Get all possible cells within range
        possible_cells = [(x, y) for x, y in product(x_range, y_range) 
                         if validate_coordinates(x, y, self.grid)]
        
        # Filter based on constraints
        if exclude_center and (center_x, center_y) in possible_cells:
            possible_cells.remove((center_x, center_y))
        
        if only_empty_cells:
            possible_cells = [(x, y) for x, y in possible_cells if len(self.grid[x][y]) == 0]
        
        # Add entity if possible
        if possible_cells:
            new_x, new_y = random.choice(possible_cells)
            entity = self.factory.create_entity(entity_type, new_x, new_y)
            self.grid[new_x][new_y].append(entity)
            return True
        return False
    
    def randomly_add_entity(self, entity_type: Type[Entity], probability: float = 0.5, 
                           only_empty_cells: bool = True) -> bool:
        """
        Randomly add an entity to the grid with a given probability.
        
        Args:
            entity_type: Type of entity to create (e.g., Plant, Herbivore, Predator)
            probability: Probability of adding the entity (0.0 to 1.0)
            only_empty_cells: Whether to only add to empty cells
            
        Returns:
            True if entity was added, False otherwise
        """
        if (1-random.random()) >= probability:
            return False
        
        # Get available cells
        if only_empty_cells:
            available_cells = self.get_all_empty_cells()
        else:
            available_cells = [(x, y) for x, y in product(range(self.width), range(self.height))]
        
        # Add entity if possible
        if available_cells:
            x, y = random.choice(available_cells)
            entity = self.factory.create_entity(entity_type, x, y)
            self.grid[x][y].append(entity)
            
            # Track spawning statistics
            entity_name = entity_type.__name__.lower()
            self.record_stat(f'{entity_name}_spawned', 1)
            
            return True
        return False

    def update(self) -> None:
        """
        Update the grid with type-based order (configured in order_to_process).
        Uses in-place updates to avoid grid copying and solve async issues.
        After updating all entities, randomly spawn new entities based on random_spawn_config.
        
        args:
            None
        returns:
            None, updated the internal grid with the next state
        """
        # Update all entities in the specified order
        for entity_type in self.order_to_process:
            self._update_entities_by_type(entity_type)

        # Randomly spawn new entities based on configuration
        for entity_type, spawn_params in self.random_spawn_config.items():
            self.randomly_add_entity(
                entity_type,
                probability=spawn_params.get('probability', 0.5),
                only_empty_cells=spawn_params.get('only_empty_cells', True)
            )
    
    def _update_entities_by_type(self, entity_type: Type[Entity]) -> None:
        """
        Update all entities of a specific type in-place.
        
        args:
            entity_type: The class type to update (Predator, Herbivore, Plant)
        returns:
            None, updates entities in-place
        """
        # Collect all entities of this type with their current positions
        entities_to_update = []
        for x, y in product(range(self.width), range(self.height)):
            for i, entity in enumerate(self.grid[x][y]):
                if isinstance(entity, entity_type):
                    entities_to_update.append((entity, x, y, i))
        
        # Sort by index in descending order to avoid index shifting issues
        entities_to_update.sort(key=lambda x: x[3], reverse=True)
        
        # Update each entity and track position changes
        for entity, old_x, old_y, index in entities_to_update:
            # Remove entity from old position
            self.grid[old_x][old_y].pop(index)
            
            # Update entity
            to_keep, new_x, new_y = entity.update(self)
            
            if to_keep:
                # Add entity to new position
                self.grid[new_x][new_y].append(entity)
                # Update entity's internal position
                entity.x = new_x
                entity.y = new_y
            else:
                # Entity died - track death statistics
                entity_name = entity_type.__name__.lower()
                self.record_stat(f'{entity_name}_died_naturally', 1)
    
    def get_population_counts(self) -> Dict[str, int]:
        """
        Get current population counts for all entity types (fully abstract).
        Dynamically counts any entity type present in the grid.
        
        Returns:
            Dictionary with entity type names as keys and counts as values
        """
        entity_counts = {}
        
        for x in range(self.width):
            for y in range(self.height):
                for entity in self.grid[x][y]:
                    # Get the entity type name (e.g., "Plant", "Herbivore", "Predator")
                    entity_type_name = type(entity).__name__.lower()
                    
                    # Initialize counter if this is the first entity of this type
                    if entity_type_name not in entity_counts:
                        entity_counts[entity_type_name] = 0
                    
                    # Increment the count
                    entity_counts[entity_type_name] += 1
        
        return entity_counts
    
    def get_grid_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the current grid state (fully abstract).
        Works with any entity types present in the grid.
        
        Returns:
            Dictionary with current population counts and cumulative event statistics
        """
        population = self.get_population_counts()
        total_population = sum(population.values())
        
        # Combine current population with cumulative statistics
        stats = {
            'population': {
                **population,  # Spread all entity type counts
                'total': total_population
            },
            'events': self.statistics.copy()
        }
        
        return stats
    
    def print_grid(self) -> None:
        """
        Print a simple representation of the grid (fully abstract).
        Uses first letter of entity type name for display.
        """
        stats = self.get_grid_stats()
        print(f"Population: {stats['population']}")
        print(f"Events: {stats['events']}")
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                cell = self.grid[x][y]
                if not cell:
                    row += "."
                elif len(cell) == 1:
                    entity = cell[0]
                    # Use first letter of entity type name (uppercase)
                    entity_type_name = type(entity).__name__
                    row += entity_type_name[0].upper() if entity_type_name else "?"
                else:
                    row += str(len(cell))
            print(row)

    def grid_to_image(self) -> np.ndarray:
        """
        Convert GOLGrid to an image with color-coded entities (fully abstract).
        Works with any entity types using the entity_color_map.
        All visualization settings are loaded from YAML configuration.
            
        Returns:
            numpy array representing the image (BGR format)
        """
        height = self.height
        width = self.width
        cell_size = self.visualization_settings['cell_size']
        empty_cell_color = self.visualization_settings['empty_cell_color']
        background_color = self.visualization_settings['background_color']
        
        # Create image (height * cell_size, width * cell_size, 3 channels)
        img_height = height * cell_size
        img_width = width * cell_size
        image = np.zeros((img_height, img_width, 3), dtype=np.uint8)
        
        # Background color
        image[:] = background_color
        
        for y in range(height):
            for x in range(width):
                y1 = y * cell_size
                y2 = y1 + cell_size
                x1 = x * cell_size
                x2 = x1 + cell_size
                
                cell_entities = self.grid[x][y]
                
                if not cell_entities:
                    # Empty cell
                    image[y1:y2, x1:x2] = empty_cell_color
                else:
                    # Determine dominant entity type based on processing order
                    # (entities processed first have visual priority)
                    cell_color = None
                    for entity_type in self.order_to_process:
                        if any(isinstance(e, entity_type) for e in cell_entities):
                            entity_type_name = entity_type.__name__.lower()
                            cell_color = self.entity_color_map.get(entity_type_name, (128, 128, 128))
                            break
                    
                    # If no color found in processing order, use first entity's type
                    if cell_color is None and cell_entities:
                        entity_type_name = type(cell_entities[0]).__name__.lower()
                        cell_color = self.entity_color_map.get(entity_type_name, (128, 128, 128))
                    
                    if cell_color:
                        image[y1:y2, x1:x2] = cell_color
                    
                    # If multiple entities, add visual indicator
                    if len(cell_entities) > 1:
                        # Draw a circle to indicate multiple entities
                        center = (x1 + cell_size // 2, y1 + cell_size // 2)
                        cv2.circle(image, center, cell_size // 4, (255, 255, 255), 2)
                        # Add count text
                        count = len(cell_entities)
                        cv2.putText(image, str(count), 
                                (x1 + cell_size // 3, y1 + 2 * cell_size // 3),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Draw grid lines
                cv2.rectangle(image, (x1, y1), (x2-1, y2-1), (100, 100, 100), 1)
        
        return image

