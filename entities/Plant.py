
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