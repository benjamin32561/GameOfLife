from itertools import product
import yaml


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
        all_possible_steps = [(x, y) for x, y in product(x_range, y_range) if validate_coordinates(x, y, grid)]
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
            if len(self.grid[x][y]) > 0 and any(isinstance(entity, object_type) for entity in self.grid[x][y])
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

    def randomly_add_object(self, object_to_add):
        """
        Randomly add an object to the grid.
        Generating random number between 0 and 1, if it is more the 0.5, add a plant to the grid.

        args:
            None
        returns:
            None, added a plant to the grid
        """

        if random.random() > 0.5:
            empty_cells = self.get_all_empty_cells()
            if empty_cells:
                x, y = random.choice(empty_cells)
                self.grid[x][y].append(object_to_add)

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
        Update the grid.
        
        args:
            None
        returns:
            None, updated the internal grid with the next state
        """
        updated_grid = [[[] for _ in range(self.width)] for _ in range(self.height)]
        for x, y in product(range(self.width), range(self.height)):
            while self.grid[x][y]:
                entity = self.grid[x][y].pop() # remove current entity so it will ignore it's own existence when updating
                to_keep, new_x, new_y = entity.update(self)
                if to_keep:
                    updated_grid[new_x][new_y].append(entity)
        self.grid = updated_grid

class Entity:
    def __init__(self, x, y, base_ttl=None):
        """
        Base object class.
        """
        self.x = x
        self.y = y
        self.ttl = base_ttl
        self.base_ttl = base_ttl
    
    def should_be_removed(self):
        """
        Check if the object should be removed from the simulation.

        args:
            None
        returns:
            True if the object should be removed, False otherwise
        """
        return self.ttl is not None and self.ttl <= 0

    def reset_ttl(self):
        """
        Reset the ttl of the object.

        args:
            None
        returns:
            None, reset the ttl of the object
        """
        self.ttl = self.base_ttl

    def get_next_position(self, gol_grid):
        """
        Get the new position of the object.

        args:
            grid: The grid object of the simulation.
        returns:
            The new position of the object.
        """
        pass

    def update(self, gol_grid):
        """
        Update the object.

        args:
            grid: The grid object of the simulation.
        returns:
            keep: a boolean indicating if the object should be kept in the simulation.
            new_x: the new x position of the object.
            new_y: the new y position of the object.
        """
        pass


class Plant(Entity):
    def __init__(self, x, y, base_ttl=None):
        """
        Plant object class.
        
        Args:
            x: X position
            y: Y position
            base_ttl: Number of steps before dying (None = infinite)
        """
        super().__init__(x, y, base_ttl)
    
    def get_next_position(self, gol_grid):
        """
        Get the new position of the plant.
        Plants don't move, so the new position is the same as the current position.
        """
        return self.x, self.y
    
    def update(self, gol_grid):
        """
        Update the plant.
        Plants don't move, but age and can be eaten.
        
        args:
            gol_grid: The grid object of the simulation.
        returns:
            keep: a boolean indicating if the object should be kept in the simulation.
        """
        if self.should_be_removed():
            return False, -1, -1  # Remove from simulation
        
        # reduce ttl
        self.ttl -= 1

        # Plants don't move
        return True, self.x, self.y

class MobileEntity(Entity):
    def __init__(self, x, y, base_ttl=None, sight_radius=None):
        """
        Mobile entity object class.

        args:
            x: X position
            y: Y position
            base_ttl: Number of steps before dying (None = infinite)
            sight_radius: The radius of the sight of the entity.
        returns:
            None, initialized the mobile entity object
        """
        super().__init__(x, y, base_ttl)
        self.sight_radius = sight_radius

    def get_random_step(self, gol_grid):
        """
        Get a random step for a given position.

        args:
            gol_grid: the grid object of the simulation
        returns:
            the x and y coordinates of the random step
        """
        all_possible_steps = gol_grid.get_all_possible_steps(self.x, self.y)
        return random.choice(all_possible_steps) 

    def get_closest_plant_coordinates(self, gol_grid, object_type):
        """
        find the closest object of a given type in a given radius

        args:
            gol_grid: the grid object of the simulation
            object_type: the type of object to find

        returns:
            the x and y position of the closest object
            -1, -1 if no object is found
        """
        all_cells_with_plants = gol_grid.get_all_cells_with_type(Plant)
        
        # get closest one in a radius
        closest_coords = (-1, -1)
        closest_distance = float('inf')
        for x, y in all_cells_with_plants:
            distance = math.sqrt((self.x-x)**2+(self.y-y)**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_coords = (x, y)
        return closest_coords

    def get_next_position_towards_object(self, gol_grid, x, y):
        """
        Get the next position moving to the nearest 

        args:
            gol_grid: the grid object of the simulation
            x: the x position of the desired position to move towards
            y: the y position of the desired position to move towards
        returns:
            the x and y coordinates of the next position
        """
        all_possible_steps = gol_grid.get_all_possible_steps(grid, x, y)
        closest_step = None
        closest_distance = float('inf')
        for step in all_possible_steps:
            distance = math.sqrt((step[0]-x)**2+(step[1]-y)**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_step = step
        return closest_step

    def get_next_position(self, gol_grid, object_type):
        """
        Find the closest object of a given type in a given radius.

        args:
            gol_grid: The grid object of the simulation.
            object_type: The type of object to find.
        returns:
            The x and y coordinates of the closest object.
            -1, -1 if no object is found.
        """
        closest_object_x, closest_object_y = self.find_closest_object_coordinates(grid, object_type)
        if closest_object_x != -1 and closest_object_y != -1:
            return self.get_next_position_towards_object(grid, closest_object_x, closest_object_y)
        else:
            return self.get_random_step(grid)

class Herbivore(MobileEntity):
    def __init__(self, x, y, base_ttl=None, sight_radius=None, T_cooldown=None):
        """
        Herbivore object class.

        Herbivores die after T_herbivore steps 
        Herbivores move towards the closest plant they can see in a (R_herbivore_sight) radius, if they don’t have a plant in sight, they move randomly.
        When an herbivore reaches a plant, it eats it, refueling its life span
        Herbivores reproduce when reaching another herbivore, staying in the same space and spawning another herbivore in a random neighboring cell.
        After reproducing, they can’t reproduce anymore for T_cooldown steps.
        """
        super().__init__(x, y, base_ttl, sight_radius)
        self.T_cooldown = 0
        self.base_T_cooldown = T_cooldown
    
    def can_mate(self):
        """
        Check if the herbivore can mate.
        """
        return self.T_cooldown <= 0

    def reset_mating_cooldown(self):
        """
        Reset the mating cooldown of the herbivore.
        """
        self.T_cooldown = self.base_T_cooldown
    
    def update(self, gol_grid):
        """
        Update the herbivore.

        args:
            gol_grid: the grid object of the simulation
        returns:
            keep: a boolean indicating if the object should be kept in the simulation.
            new_x: the new x position of the object.
            new_y: the new y position of the object.
        """
        if self.should_be_removed():
            return False, -1, -1  # Remove from simulation
        
        # reduce ttl
        self.ttl -= 1

        # move towards the closest plant
        new_x, new_y = self.get_next_position(gol_grid, Plant)
        
        # check if next position contains a herbivore, if so,
        # reproduce, spawning another herbivore in a random neighboring cell.
        if gol_grid.is_object_type_in_cell(new_x, new_y, Herbivore) and self.can_mate():
            # check if there is at least one other herbivore in the cell that can mate, if so,
            # reproduce, reset their cooldown and create a new herbivore
            mateable_herbivores = [herbivore for herbivore in gol_grid.grid[new_x][new_y] if isinstance(herbivore, Herbivore) and herbivore.can_mate()]

            if len(mateable_herbivores) >= 1:
                mate_herbivore = mateable_herbivores[0]
                # reset mating cooldown for both herbivors
                mate_herbivore.reset_mating_cooldown()
                self.reset_mating_cooldown()

                # generate a new herbivorein the grid
                gol_grid.add_herbivore_to_random_neighboor()

        # check if next position has a plant in it, if so 
        if gol_grid.is_object_type_in_cell(new_x, new_y, Plant):
            grid.grid[new_x][new_y] = [obj for obj in grid.grid[new_x][new_y] if not isinstance(obj, Plant)]
            self.reset_ttl()

        return True, new_x, new_y

class Predator(MobileEntity):
    def __init__(self, x, y, base_ttl=None, sight_radius=None):
        """
        Predator object class.
        """
        super().__init__(x, y, base_ttl, sight_radius)
    
    def update(self, gol_grid):
        """
        Update the predator.

        args:
            gol_grid: the grid object of the simulation
        returns:
            keep: a boolean indicating if the object should be kept in the simulation.
            new_x: the new x position of the object.
            new_y: the new y position of the object.
        """
        if self.should_be_removed():
            return False, -1, -1  # Remove from simulation
        
        # reduce ttl
        self.ttl -= 1

        # move towards the closest plant
        new_x, new_y = self.get_next_position(gol_grid, Herbivore)
        
        # check if next position contains a herbivore, if so,
        # remove it, and reset the ttl of the current predator
        if gol_grid.is_object_type_in_cell(new_x, new_y, Herbivore):
            grid.grid[new_x][new_y] = [obj for obj in grid.grid[new_x][new_y] if not isinstance(obj, Herbivore)]

            self.reset_ttl()

        return True, new_x, new_y