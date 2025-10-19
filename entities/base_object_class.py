class BaseObject:
    def __init__(self):
        """
        Base object class.
        """
    
    def update(self, grid):
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


class Plant(BaseObject):
    def __init__(self, lifespan=None):
        """
        Plant object class.
        
        Args:
            x: X position
            y: Y position
            lifespan: Number of steps before dying (None = infinite)
        """
        super().__init__()
        self.lifespan = lifespan
        self.age = 0
    
    def update(self, grid):
        """
        Update the plant.
        Plants don't move, but age and can be eaten.
        
        args:
            grid: The grid object of the simulation.
        returns:
            keep: a boolean indicating if the object should be kept in the simulation.
        """
        
        # Check if plant dies of old age
        if self.lifespan is not None and self.age >= self.lifespan:
            return False  # Remove from simulation
        
        # Plants don't move
        return True

class Herbivores(BaseObject):
    def __init__(self, T_herbivore, R_herbivore_sight, T_cooldown):
        """
        Herbivore object class.

        Herbivores die after T_herbivore steps 
        Herbivores move towards the closest plant they can see in a (R_herbivore_sight) radius, if they don’t have a plant in sight, they move randomly.
        When an herbivore reaches a plant, it eats it, refueling its life span
        Herbivores reproduce when reaching another herbivore, staying in the same space and spawning another herbivore in a random neighboring cell.
        After reproducing, they can’t reproduce anymore for T_cooldown steps.
        """
        super().__init__()
        self.T_herbivore = T_herbivore
        self.R_herbivore_sight = R_herbivore_sight
        self.T_cooldown = 0
        self.base_T_cooldown = T_cooldown
        self.age = 0
    
    def update(self, grid):
        """
        Update the herbivore.
        """
        # Age the herbivore
        self.age += 1

        # Check if herbivore dies of old age
        if self.life_span <= 0:
            return False  # Remove from simulation
        
        # Check if herbivore was eaten
        if self.eaten:
            return False  # Remove from simulation
        
        pass