import json
import os
from datetime import datetime

class Component:
    pass

class DescriptionComponent(Component):
    def __init__(self, description):
        self.description = description

class InputComponent(Component):
    def __init__(self, inputs):
        self.inputs = inputs  # List of dicts

class OutputComponent(Component):
    def __init__(self, outputs):
        self.outputs = outputs  # List of dicts

class SourceCodeComponent(Component):
    def __init__(self, source_code):
        self.source_code = source_code

class TagComponent(Component):
    def __init__(self, tags):
        self.tags = tags  # List of strings

class DependencyComponent(Component):
    def __init__(self, dependencies):
        self.dependencies = dependencies  # List of system/entity names

class StatusComponent(Component):
    def __init__(self, status="idle"):
        self.status = status

class ConfigComponent(Component):
    def __init__(self, config):
        self.config = config  # Dict of config options

class ResultComponent(Component):
    def __init__(self, result):
        self.result = result

class DocumentationComponent(Component):
    def __init__(self, documentation):
        self.documentation = documentation

class TimestampComponent(Component):
    def __init__(self, created=None, last_run=None):
        self.created = created or datetime.now().isoformat()
        self.last_run = last_run

class AuthorComponent(Component):
    def __init__(self, author):
        self.author = author

# Awesome & Unique Components

class VisualizationComponent(Component):
    """Holds visualization or UI hints for the entity."""
    def __init__(self, hints):
        self.hints = hints  # Dict or list of visualization hints

class SecurityComponent(Component):
    """Tracks security or permission requirements."""
    def __init__(self, permissions):
        self.permissions = permissions  # List of permissions or roles

class AnalyticsComponent(Component):
    """Tracks usage analytics or performance metrics."""
    def __init__(self, metrics):
        self.metrics = metrics  # Dict of analytics data

class Entity:
    def __init__(self, name):
        self.name = name
        self.components = {}

    def add_component(self, component_type, component):
        self.components[component_type] = component

    def get_component(self, component_type):
        return self.components.get(component_type)

class ECS:
    def __init__(self):
        self.entities = []

    def load_from_json(self, json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entity = Entity(data.get("system", "unknown"))
        entity.add_component(DescriptionComponent, DescriptionComponent(data.get("description", "")))
        entity.add_component(InputComponent, InputComponent(data.get("detected_inputs", [])))
        entity.add_component(OutputComponent, OutputComponent(data.get("detected_outputs", [])))
        entity.add_component(SourceCodeComponent, SourceCodeComponent(data.get("source_code", "")))
        # Add some demo/empty components for demonstration
        entity.add_component(TagComponent, TagComponent(data.get("tags", [])))
        entity.add_component(DependencyComponent, DependencyComponent(data.get("dependencies", [])))
        entity.add_component(StatusComponent, StatusComponent(data.get("status", "idle")))
        entity.add_component(ConfigComponent, ConfigComponent(data.get("config", {})))
        entity.add_component(ResultComponent, ResultComponent(data.get("result", None)))
        entity.add_component(DocumentationComponent, DocumentationComponent(data.get("documentation", "")))
        entity.add_component(TimestampComponent, TimestampComponent(data.get("created", None), data.get("last_run", None)))
        entity.add_component(AuthorComponent, AuthorComponent(data.get("author", "")))
        entity.add_component(VisualizationComponent, VisualizationComponent(data.get("visualization_hints", {})))
        entity.add_component(SecurityComponent, SecurityComponent(data.get("permissions", [])))
        entity.add_component(AnalyticsComponent, AnalyticsComponent(data.get("metrics", {})))
        self.entities.append(entity)
        return entity

    def find_entity(self, name):
        for entity in self.entities:
            if entity.name == name:
                return entity
        return None

    def list_entities(self):
        return [entity.name for entity in self.entities]

# Example usage:
if __name__ == "__main__":
    ecs = ECS()
    # Load all *_analysis.json files in the current directory
    for fname in os.listdir(os.path.dirname(__file__)):
        if fname.endswith("_analysis.json"):
            ecs.load_from_json(os.path.join(os.path.dirname(__file__), fname))
    print("Loaded entities:", ecs.list_entities())
    # Print info for each entity
    for entity in ecs.entities:
        desc = entity.get_component(DescriptionComponent).description
        print(f"\nEntity: {entity.name}\nDescription: {desc}")