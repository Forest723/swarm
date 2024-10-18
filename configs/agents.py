import sys
import os

# Add the parent directory (emergency/) to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from configs.tools import escalate_to_human, generate_evacuation_plan, allocate_resources, case_resolved, initiate_shelter_search
from swarm import Agent

# Function to transfer to the Evacuation Agent
def transfer_to_evacuation():
    return evacuation_agent

# Function to transfer to the Resource Allocation Agent
def transfer_to_resource_allocation():
    return resource_allocation_agent

# Function to transfer back to Triage Agent (for resetting or rerouting)
def transfer_to_triage():
    return triage_agent

# Triage Agent Definition
def triage_instructions(context_variables):
    emergency_context = context_variables.get("emergency_context", None)
    response_context = context_variables.get("response_context", None)
    return f"You are responsible for triaging the emergency request and determining whether to transfer it to the evacuation team or resource allocation team. When you need more information to triage the request, ask direct questions without explaining why you're asking. Do not share your thought process with the user. Emergency context: {emergency_context}, Response context: {response_context}"

# Triage Agent: Decides whether to transfer to Evacuation or Resource Allocation
triage_agent = Agent(
    name="Triage Agent",
    instructions=triage_instructions,
    functions=[transfer_to_evacuation, transfer_to_resource_allocation],
)

# Evacuation Agent: Plans evacuations and finds shelters
evacuation_agent = Agent(
    name="Evacuation Agent",
    instructions="You handle evacuation requests. Provide evacuation plans and initiate shelter searches as needed.",
    functions=[generate_evacuation_plan, initiate_shelter_search, escalate_to_human, case_resolved],
)

# Resource Allocation Agent: Allocates emergency resources
resource_allocation_agent = Agent(
    name="Resource Allocation Agent",
    instructions="You handle resource allocation. Allocate resources like medical supplies, food, and shelter.",
    functions=[allocate_resources, escalate_to_human, case_resolved],
)