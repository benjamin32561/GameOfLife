from typing import Dict, Any, List, Tuple, Type

from entities.entity import Entity
from entities.herbivore import Herbivore
from entities.omnivore import Omnivore
from entities.plant import Plant
from entities.predator import Predator


class EntityFactory:
    """
    Factory class for creating entity instances.
    Centralizes entity creation logic and configuration.
    """
    
    # Class-level entity type mapping for converting string names to classes
    ENTITY_TYPE_MAP = {
        'Omnivore': Omnivore,
        'Plant': Plant,
        'Herbivore': Herbivore,
        'Predator': Predator,
    }
    
    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize the entity factory with configuration parameters.
        
        Args:
            config: Configuration dictionary containing entity parameters
        """
        self.config = config
        self.params = config['parameters']
    
    def create_entity(self, entity_type: Type[Entity], x: int, y: int) -> Entity:
        """
        Create an entity of the specified type (generic factory method).
        
        Args:
            entity_type: The class type of entity to create
            x: X position
            y: Y position
            
        Returns:
            Entity instance of the specified type
            
        Raises:
            ValueError: If entity_type is not supported
        """
        if entity_type == Plant or entity_type is Plant:
            return self.create_plant(x, y)
        elif entity_type == Herbivore or entity_type is Herbivore:
            return self.create_herbivore(x, y)
        elif entity_type == Predator or entity_type is Predator:
            return self.create_predator(x, y)
        elif entity_type == Omnivore or entity_type is Omnivore:
            return self.create_omnivore(x, y)
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
    
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

    def create_omnivore(self, x: int, y: int) -> Omnivore:
        """
        Create an omnivore entity.
        
        Args:
            x: X position
            y: Y position
            
        Returns:
    
            Omnivore instance
        """
        return Omnivore(
            x, y,
            self.params['T_omnivore'],
            self.params['R_omnivore_sight'],
            self.params['T_cooldown_omnivore']
        )

    def create_initial_entities(self) -> List[Tuple[Entity, int, int]]:
        """
        Create all initial entities from configuration.
        This method centralizes the decision of which entities to create
        based on the configuration file.
        
        Returns:
            List of tuples (entity, x, y) for all initial entities
        """
        entities = []
        
        # Add plants
        for plant_data in self.config['initial_state']['plants']:
            x, y = plant_data['x'], plant_data['y']
            plant = self.create_plant(x, y)
            entities.append((plant, x, y))
        
        # Add herbivores
        for herb_data in self.config['initial_state']['herbivores']:
            x, y = herb_data['x'], herb_data['y']
            herbivore = self.create_herbivore(x, y)
            entities.append((herbivore, x, y))
        
        # Add predators
        for pred_data in self.config['initial_state']['predators']:
            x, y = pred_data['x'], pred_data['y']
            predator = self.create_predator(x, y)
            entities.append((predator, x, y))
        
        # Add omnivores
        for omn_data in self.config['initial_state']['omnivores']:
            x, y = omn_data['x'], omn_data['y']
            omnivore = self.create_omnivore(x, y)
            entities.append((omnivore, x, y))
        
        return entities

