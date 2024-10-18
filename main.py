import openai
import os
import random
from dotenv import load_dotenv
from configs.agents import triage_agent, triage_agent, evacuation_agent, resource_allocation_agent
from swarm.repl import run_demo_loop

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = openai.api_key

# Function to dynamically set initial context based on user input or predefined scenarios
def set_initial_context():
    print("=== SET UP THE EMERGENCY SCENARIO ===")
    
    # Let user choose the type of emergency
    emergency_type = input("Enter the type of emergency (e.g., Flood, Wildfire, Earthquake): ").capitalize()

    # User input for location and population
    location = input("Enter the location of the emergency: ")
    affected_population = int(input("Enter the affected population size: "))
    
    # Allow user to choose severity level or randomly assign one
    severity_level = input("Enter the severity level (Low, Medium, High) or press Enter for random: ")
    if not severity_level:
        severity_level = random.choice(["Low", "Medium", "High"])

    # Resources needed based on emergency type or custom input
    if emergency_type == "Flood":
        resources_needed = ["Evacuation", "Medical supplies", "Shelters"]
    elif emergency_type == "Wildfire":
        resources_needed = ["Evacuation", "Firefighting resources", "Medical aid"]
    else:
        resources_needed = input("Enter the resources needed (comma-separated): ").split(",")

    # Timing urgency (user-defined or based on emergency type)
    timing = input("Enter the urgency (Immediate, Critical, Normal): ")

    # Return dynamic context variables
    return {
        "emergency_context": {
            "emergency_type": emergency_type,
            "location": location,
            "severity_level": severity_level,
            "affected_population": affected_population,
            "resources_needed": resources_needed,
            "timing": timing
        },
        "response_context": {
            "status": "Emergency requires coordination between evacuation efforts and resource allocation",
            "evacuation_started": False,
            "resources_allocated": False
        }
    }

# Function to simulate event updates
def update_context(context):
    print("\n-- UPDATING CONTEXT --")
    new_event = input("Enter a new event (e.g., 'severity increases', 'new evac orders', 'resources depleted'): ")

    if "severity" in new_event:
        context['emergency_context']["severity_level"] = "Extreme"
        print("Severity level updated to EXTREME.")
    elif "evac orders" in new_event:
        context['emergency_context']["timing"] = "Critical - Immediate Evacuation Needed"
        print("New evacuation orders issued.")
    elif "resources depleted" in new_event:
        context['response_context']["resources_allocated"] = False
        print("Resources have been depleted, re-allocating needed.")
    
    return context

def main():
    print("Starting Emergency Management Simulation...")

    # Dynamically set the initial context using the user-defined setup
    context_variables = set_initial_context()

    # Event loop for ongoing emergency response
    while True:
        # Show current emergency context
        print("\nCurrent Emergency Context: ", context_variables["emergency_context"])
        print("Response Status: ", context_variables["response_context"])
        
        # Let the user input their next action or request
        user_input = input("\nWhat action should be taken next (e.g., 'Evacuate', 'Allocate resources', 'Status update')? ")

        # Handle the request dynamically
        if "evacuate" in user_input.lower():
            if not context_variables["response_context"]["evacuation_started"]:
                print("Evacuation initiated.")
                context_variables["response_context"]["evacuation_started"] = True
                run_demo_loop(evacuation_agent, context_variables=context_variables, debug=True)
            else:
                print("Evacuation already in progress.")
        
        elif "allocate" in user_input.lower():
            if not context_variables["response_context"]["resources_allocated"]:
                print("Allocating resources...")
                run_demo_loop(resource_allocation_agent, context_variables=context_variables, debug=True)
                context_variables["response_context"]["resources_allocated"] = True
            else:
                print("Resources already allocated.")
        
        elif "update" in user_input.lower():
            print("Providing status update...")
            run_demo_loop(triage_agent, context_variables=context_variables, debug=True)

        # Introduce new events and update context
        context_variables = update_context(context_variables)

        # Ask the user if they want to continue or end the simulation
        continue_simulation = input("\nContinue the simulation? (yes/no): ")
        if continue_simulation.lower() == "no":
            print("Ending simulation. Goodbye!")
            break

if __name__ == "__main__":
    main()