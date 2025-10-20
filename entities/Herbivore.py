
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

                # generate a new herbivore in the grid
                gol_grid.add_herbivore_to_random_neighboor(new_x, new_y)

        # check if next position has a plant in it, if so 
        if gol_grid.is_object_type_in_cell(new_x, new_y, Plant):
            gol_grid.grid[new_x][new_y] = [obj for obj in gol_grid.grid[new_x][new_y] if not isinstance(obj, Plant)]
            self.reset_ttl()

        return True, new_x, new_y