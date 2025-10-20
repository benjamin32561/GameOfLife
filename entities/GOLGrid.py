from itertools import product
import yaml
import random
from .Plant import Plant
from .Herbivore import Herbivore
from .Predator import Predator


def validate_coordinates(x, y, grid):
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
    def __init__(self, init_file_path=None):
        """
        GOLGrid class.
        """
        self.grid = None
        self.width = None
        self.height = None

        self.config = self.load_from_file(init_file_path)
        self.init_grid_parameters(self.config)
        self.init_grid_state(self.config)
    
    def load_from_file(self, file_path):
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

    def init_grid_parameters(self, config):
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

    def create_plant(self, x, y):
        """
        Create a plant object.
        """
        return Plant(x, y, self.config['parameters']['plant_lifespan'])
    
    def create_herbivore(self, x, y):
        """
        Create a herbivore object.
        """
        return Herbivore(x, y,
            self.config['parameters']['T_herbivore'],
            self.config['parameters']['R_herbivore_sight'],
            self.config['parameters']['T_cooldown_herbivore']
        )
    
    def create_predator(self, x, y):
        """
        Create a predator object.
        """
        return Predator(x, y,
            self.config['parameters']['T_predator'],
            self.config['parameters']['R_predator_sight']
        )

    def init_grid_state(self, config):
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
    
    def get_all_possible_steps(self, x, y):
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

    def get_all_cells_with_type(self, object_type):
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

    def get_all_empty_cells(self):
        """
        Get all empty cells in the grid.
        """
        return [(x, y) for x, y in product(range(self.width), range(self.height)) if len(self.grid[x][y]) == 0]

    def is_object_type_in_cell(self, x, y, object_type):
        """
        Check if an object of a given type is in a given cell.
        """
        return len(self.grid[x][y]) > 0 and any(isinstance(entity, object_type) for entity in self.grid[x][y])

    def randomly_add_plant(self):
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

    def add_herbivore_to_random_neighboor(self, x, y):
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

    def update(self):
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
    
    def _update_entities_by_type(self, entity_type):
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
    
    def get_grid_stats(self):
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
    
    def print_grid(self):
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
