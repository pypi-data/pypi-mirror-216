import typing
from pygame_ecs.components.base_component import BaseComponent
from pygame_ecs.managers.component_manager import ComponentInstanceType
from pygame_ecs.managers.entity_manager import EntityManager
from pygame_ecs.entity import Entity


class BaseSystem:
    # typing.Type specifies that it will take subclasses of this class
    def __init__(
        self, required_component_types: list[typing.Type[BaseComponent]]
    ) -> None:
        self.required_component_types = required_component_types
        self.entity_manager: EntityManager

    def update(
        self,
        entity: Entity,
        entity_components: dict[typing.Type[BaseComponent], ComponentInstanceType],
    ):
        pass

    def __str__(self) -> str:
        return f"<{type(self).__name__}>"
