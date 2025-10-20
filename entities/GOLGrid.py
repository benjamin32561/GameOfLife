from itertools import product
import yaml
import random
import numpy as np
import cv2
from typing import List, Tuple, Dict, Optional, Any, Type
from .Plant import Plant
from .Herbivore import Herbivore
from .Predator import Predator
from .Entity import Entity


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
    def __init__(self, init_file_path: Optional[str] = None) -> None:
        """
        GOLGrid class.
        """
        self.grid = None
        self.width = None
        self.height = None

        self.config = self.load_from_file(init_file_path)
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

    def create_plant(self, x: int, y: int) -> Plant:
        """
        Create a plant object.
        """
        return Plant(x, y, self.config['parameters']['plant_lifespan'])
    
    def create_herbivore(self, x: int, y: int) -> Herbivore:
        """
        Create a herbivore object.
        """
        return Herbivore(x, y,
            self.config['parameters']['T_herbivore'],
            self.config['parameters']['R_herbivore_sight'],
            self.config['parameters']['T_cooldown_herbivore']
        )
    
    def create_predator(self, x: int, y: int) -> Predator:
        """
        Create a predator object.
        """
        return Predator(x, y,
            self.config['parameters']['T_predator'],
            self.config['parameters']['R_predator_sight']
        )

    def init_grid_state(self, config: Dict[str, Any]) -> None:
        """
        Create initial state from configuration.
        
        args:
            config: the configuration
        returns:
            None, updated the internal grid with the initial state
        """

        # Add plants
        for plant_data in config['initial_state']['plants']:
            x, y = plant_data['x'], plant_data['y']
            plant = self.create_plant(x, y)
            self.grid[x][y].append(plant)
        
        # Add herbivores
        for herb_data in config['initial_state']['herbivores']:
            x, y = herb_data['x'], herb_data['y']
            herbivore = self.create_herbivore(x, y)
            self.grid[x][y].append(herbivore)
        
        # Add predators
        for pred_data in config['initial_state']['predators']:
            x, y = pred_data['x'], pred_data['y']
            predator = self.create_predator(x, y)
            self.grid[x][y].append(predator)
    
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

    def is_object_type_in_cell(self, x: int, y: int, object_type: Type[Entity]) -> bool:
        """
        Check if an object of a given type is in a given cell.
        """
        return len(self.grid[x][y]) > 0 and any(isinstance(entity, object_type) for entity in self.grid[x][y])

    def randomly_add_plant(self) -> None:
        """
        Randomly add a plant to the grid.
        Generating random number between 0 and 1, if it is more than 0.5, add a plant to the grid.

        args:
            None
        returns:
            None, added a plant to the grid
        """
        if random.random() > 0.5:
            empty_cells = self.get_all_empty_cells()
            if empty_cells:
                x, y = random.choice(empty_cells)
                self.grid[x][y].append(self.create_plant(x, y))

    def add_herbivore_to_random_neighboor(self, x: int, y: int) -> bool:
        """
        When 2 herbivores are in the same cell, they reproduce, staying in the same space and spawning another herbivore in a random neighboring cell.
        The new herbivore need to be created in a random neighboring cell, but not on the same cell as the mating herbivores.

        args:
            x: the x position of the mating herbivores
            y: the y position of the matingherbivores
        returns:
            None, added a herbivore to the grid
        """
        x_range = range(max(0, x - 1), min(self.width, x + 2))
        y_range = range(max(0, y - 1), min(self.height, y + 2))
        all_possible_steps = [(x, y) for x, y in product(x_range, y_range) if validate_coordinates(x, y, self.grid)]
        all_possible_steps.remove((x, y))
        if all_possible_steps:
            x, y = random.choice(all_possible_steps)
            self.grid[x][y].append(self.create_herbivore(x, y))
        else:
            return False
        return True

    def update(self) -> None:
        """
        Update the grid with type-based order: Predators -> Herbivores -> Plants
        Uses in-place updates to avoid grid copying and solve async issues.
        
        args:
            None
        returns:
            None, updated the internal grid with the next state
        """
        # Phase 1: Update all Predators first
        self._update_entities_by_type(Predator)
        
        # Phase 2: Update all Herbivores (after predators have moved/died)
        self._update_entities_by_type(Herbivore)
        
        # Phase 3: Update all Plants (after herbivores have moved/eaten)
        self._update_entities_by_type(Plant)

        # randomly create a plant
        self.randomly_add_plant()
    
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
    
    def get_grid_stats(self) -> Dict[str, int]:
        """
        Get statistics about the current grid state.
        
        Returns:
            Dictionary with entity counts
        """
        plant_count = 0
        herbivore_count = 0
        predator_count = 0
        
        for x in range(self.width):
            for y in range(self.height):
                for entity in self.grid[x][y]:
                    if isinstance(entity, Predator):
                        predator_count += 1
                    elif isinstance(entity, Herbivore):
                        herbivore_count += 1
                    elif isinstance(entity, Plant):
                        plant_count += 1
        
        return {
            'plants': plant_count,
            'herbivores': herbivore_count,
            'predators': predator_count
        }
    
    def print_grid(self) -> None:
        """
        Print a simple representation of the grid.
        """
        print(f"Grid Stats: {self.get_grid_stats()}")
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                cell = self.grid[x][y]
                if not cell:
                    row += "."
                elif len(cell) == 1:
                    entity = cell[0]
                    if isinstance(entity, Plant):
                        row += "P"
                    elif isinstance(entity, Herbivore):
                        row += "H"
                    elif isinstance(entity, Predator):
                        row += "X"
                    else:
                        row += "."
                else:
                    row += str(len(cell))
            print(row)

    def grid_to_image(self, cell_size: int = 40) -> np.ndarray:
        """
        Convert GOLGrid to an image with color-coded entities.
        
        Args:
            gol_grid: GOLGrid object
            cell_size: Size of each cell in pixels
            
        Returns:
            numpy array representing the image (BGR format)
        """
        height = self.height
        width = self.width
        
        # Create image (height * cell_size, width * cell_size, 3 channels)
        img_height = height * cell_size
        img_width = width * cell_size
        image = np.zeros((img_height, img_width, 3), dtype=np.uint8)
        
        # Background color (dark green for nature theme)
        image[:] = [34, 139, 34]  # Forest green (BGR)
        
        # Color scheme:
        # Plants: Bright green
        # Herbivores: Yellow
        # Predators: Red
        
        for y in range(height):
            for x in range(width):
                y1 = y * cell_size
                y2 = y1 + cell_size
                x1 = x * cell_size
                x2 = x1 + cell_size
                
                cell_entities = self.grid[x][y]
                
                if not cell_entities:
                    # Empty cell - dark background
                    image[y1:y2, x1:x2] = [20, 60, 20]  # Dark green
                else:
                    # Determine dominant entity type
                    has_predator = any(isinstance(e, Predator) for e in cell_entities)
                    has_herbivore = any(isinstance(e, Herbivore) for e in cell_entities)
                    has_plant = any(isinstance(e, Plant) for e in cell_entities)
                    
                    if has_predator:
                        # Red for predators
                        image[y1:y2, x1:x2] = [0, 0, 255]  # Red (BGR)
                    elif has_herbivore:
                        # Yellow for herbivores
                        image[y1:y2, x1:x2] = [0, 255, 255]  # Yellow (BGR)
                    elif has_plant:
                        # Bright green for plants
                        image[y1:y2, x1:x2] = [0, 255, 0]  # Bright green (BGR)
                    
                    # If multiple entity types, add markers
                    if len([e for e in cell_entities if isinstance(e, (Plant, Herbivore, Predator))]) > 1:
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