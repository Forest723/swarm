def escalate_to_human(reason=None):
    """Escalates the situation to a human emergency coordinator."""
    return f"Escalating to human coordinator: {reason}" if reason else "Escalating to human coordinator"


def generate_evacuation_plan(context_variables):
    """Generates an evacuation plan based on the emergency context."""
    location = context_variables.get("location", "unknown")
    affected_population = context_variables.get("affected_population", "unknown")
    return f"Evacuation plan for {location} with a population of {affected_population}. Prioritize high-risk areas and establish shelter points."


def allocate_resources(resource_type, quantity):
    """Allocates resources such as medical supplies, food, etc."""
    return f"Allocated {quantity} units of {resource_type}."


def case_resolved():
    """Marks the case as resolved."""
    return "Case resolved. No further actions required."


def initiate_shelter_search():
    """Finds available shelters for displaced people."""
    return "Shelters located. Dispatching details to the evacuation team."