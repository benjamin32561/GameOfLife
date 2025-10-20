from typing import Dict, Any

from entities.herbivore import Herbivore
from entities.plant import Plant
from entities.predator import Predator


class EntityFactory:
    """
    Factory class for creating entity instances.
    Centralizes entity creation logic and configuration.
    """
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize the entity factory with configuration parameters.
        
        Args:
            config: Configuration dictionary containing entity parameters
        """
        self.config = config
        self.params = config['parameters']
    
    def create_plant(self, x: int, y: int) -> Plant:
        """
        Create a plant entity.
        
        Args:
            x: X position
            y: Y position
            
        Returns:
            Plant instance
        """
        return Plant(x, y, self.params['plant_lifespan'])
    
    def create_herbivore(self, x: int, y: int) -> Herbivore:
        """
        Create a herbivore entity.
        
        Args:
            x: X position
            y: Y position
            
        Returns:
            Herbivore instance
        """
        return Herbivore(
            x, y,
            self.params['T_herbivore'],
            self.params['R_herbivore_sight'],
            self.params['T_cooldown_herbivore']
        )
    
    def create_predator(self, x: int, y: int) -> Predator:
        """
        Create a predator entity.
        
        Args:
            x: X position
            y: Y position
            
        Returns:
            Predator instance
        """
        return Predator(
            x, y,
            self.params['T_predator'],
            self.params['R_predator_sight']
        )

