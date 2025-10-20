from .Entity import Entity
import random
import math


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

    def get_closest_object_coordinates(self, gol_grid, object_type):
        """
        find the closest object of a given type in a given radius

        args:
            gol_grid: the grid object of the simulation
            object_type: the type of object to find

        returns:
            the x and y position of the closest object
            -1, -1 if no object is found
        """
        all_cells_with_plants = gol_grid.get_all_cells_with_type(object_type)
        
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
        all_possible_steps = gol_grid.get_all_possible_steps(x, y)
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
        closest_object_x, closest_object_y = self.get_closest_object_coordinates(gol_grid, object_type)
        if closest_object_x != -1 and closest_object_y != -1:
            return self.get_next_position_towards_object(gol_grid, closest_object_x, closest_object_y)
        else:
            return self.get_random_step(gol_grid)
