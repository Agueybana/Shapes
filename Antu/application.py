# Import necessary libraries
import csv

# Define the database of quartz information
quartz_database = [
    {"name": "Quartz 1", "zodiac": ["Aries", "Leo"], "description": "Description of Quartz 1."},
    {"name": "Quartz 2", "zodiac": ["Gemini", "Virgo"], "description": "Description of Quartz 2."},
    # Add more quartz entries as needed
]

# Function to get user input and provide quartz recommendations
def get_quartz_recommendation():
    # Get user input
    zodiac_sign = input("Enter your zodiac sign: ")
    problem = input("Describe your personal problem: ")

    # Find matching quartz based on user input
    recommendations = []
    for quartz in quartz_database:
        if zodiac_sign in quartz["zodiac"]:
            recommendations.append(quartz)

    # Display recommendations
    if recommendations:
        print("Recommended Quartz:")
        for recommendation in recommendations:
            print(f"- {recommendation['name']}: {recommendation['description']}")
    else:
        print("No recommendations found for your input.")

# Example usage
get_quartz_recommendation()
