class BaseObject:
    def __init__(self, x, y):
        """
        Base object class.
        """
        self.x = x
        self.y = y
    
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
    def __init__(self, x, y, lifespan=None):
        """
        Plant object class.
        
        Args:
            x: X position
            y: Y position
            lifespan: Number of steps before dying (None = infinite)
        """
        super().__init__(x, y)
        self.lifespan = lifespan
        self.age = 0
        self.eaten = False
    
    def update(self, grid):
        """
        Update the plant.
        Plants don't move, but age and can be eaten.
        
        args:
            grid: The grid object of the simulation.
        returns:
            keep: a boolean indicating if the object should be kept in the simulation.
            new_x: the new x position of the object.
            new_y: the new y position of the object.
        """
        # Age the plant
        self.age += 1
        
        # Check if plant dies of old age
        if self.lifespan is not None and self.age >= self.lifespan:
            return False, self.x, self.y  # Remove from simulation
        
        # Check if plant was eaten
        if self.eaten:
            return False, self.x, self.y  # Remove from simulation
        
        # Plants don't move
        return True, self.x, self.y