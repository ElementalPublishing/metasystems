from ecs import (
    ECS, Entity, DescriptionComponent, InputComponent, OutputComponent, SourceCodeComponent,
    TagComponent, DependencyComponent, StatusComponent, ConfigComponent, ResultComponent,
    DocumentationComponent, TimestampComponent, AuthorComponent, VisualizationComponent,
    SecurityComponent, AnalyticsComponent, Component
)
import datetime
import json
import os
from datetime import datetime

# --- Core ECS Classes and Components ---

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

# --- Unique Components ---

class ScheduleComponent(Component):
    """Holds scheduling info for timed or periodic systems."""
    def __init__(self, cron=None, interval_seconds=None):
        self.cron = cron
        self.interval_seconds = interval_seconds

class EventComponent(Component):
    """Tracks events this entity can emit or respond to."""
    def __init__(self, events=None):
        self.events = events or []

class HistoryComponent(Component):
    """Keeps a log of actions or state changes."""
    def __init__(self, history=None):
        self.history = history or []

# --- ECS Entity and Manager ---

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
        # Add unique/demo components (optional, for demonstration)
        entity.add_component(ScheduleComponent, ScheduleComponent())
        entity.add_component(EventComponent, EventComponent())
        entity.add_component(HistoryComponent, HistoryComponent())
        self.entities.append(entity)
        return entity

    def find_entity(self, name):
        for entity in self.entities:
            if entity.name == name:
                return entity
        return None

    def list_entities(self):
        return [entity.name for entity in self.entities]

# --- Example Systems (see systems.py for more) ---

class InputPromptSystem:
    def __init__(self, ecs):
        self.ecs = ecs

    def run(self):
        print("=== Input Prompt System ===")
        for entity in self.ecs.entities:
            input_comp = entity.get_component(InputComponent)
            if input_comp and input_comp.inputs:
                print(f"\nEntity: {entity.name}")
                for inp in input_comp.inputs:
                    print(f"  - {inp.get('description', 'Input required')}")

class OutputDisplaySystem:
    """Displays all outputs for each entity."""
    def __init__(self, ecs):
        self.ecs = ecs

    def run(self):
        print("=== Output Display System ===")
        for entity in self.ecs.entities:
            output_comp = entity.get_component(OutputComponent)
            if output_comp and output_comp.outputs:
                print(f"\nEntity: {entity.name}")
                for out in output_comp.outputs:
                    desc = out.get('description', 'Output')
                    out_type = out.get('type', 'unknown')
                    print(f"  - [{out_type}] {desc}")
            else:
                print(f"\nEntity: {entity.name} has no outputs.")

class StatusUpdateSystem:
    """Allows updating and displaying the status of entities."""
    def __init__(self, ecs):
        self.ecs = ecs

    def run(self):
        print("=== Status Update System ===")
        for entity in self.ecs.entities:
            status_comp = entity.get_component(StatusComponent)
            current_status = status_comp.status if status_comp else "unknown"
            print(f"\nEntity: {entity.name} (Current status: {current_status})")
            # Prompt user for a new status (or press Enter to keep current)
            new_status = input(f"Enter new status for {entity.name} (or press Enter to keep '{current_status}'): ").strip()
            if new_status and status_comp:
                status_comp.status = new_status
                print(f"Status for {entity.name} updated to '{new_status}'")
            else:
                print(f"Status for {entity.name} remains '{current_status}'")