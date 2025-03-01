import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Sample function to load user data (in CSV format)
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Function to check meal time consistency
def check_meal_timing(data):
    data['meal_time'] = pd.to_datetime(data['time'])
    data['hour'] = data['meal_time'].dt.hour
    data['minute'] = data['meal_time'].dt.minute
    meal_time_diff = data['meal_time'].diff().fillna(pd.Timedelta(seconds=0))
    
    irregularities = meal_time_diff > timedelta(hours=5)  # meals more than 5 hours apart are irregular
    irregular_meals = data[irregularities]
    return irregular_meals

# Function to analyze calorie intake for irregularities
def check_calorie_intake(data):
    # Assuming a column 'calories' exists in the data
    irregular_calorie_patterns = []
    for i in range(1, len(data)):
        prev_calories = data.loc[i-1, 'calories']
        curr_calories = data.loc[i, 'calories']
        if abs(curr_calories - prev_calories) > 500:  # Large fluctuation in calorie intake
            irregular_calorie_patterns.append(data.iloc[i])
    
    return pd.DataFrame(irregular_calorie_patterns)

# Function to suggest improvements
def suggest_improvements(irregular_meals, irregular_calorie_patterns):
    suggestions = []
    
    if not irregular_meals.empty:
        suggestions.append("Consider having more consistent meal times to stabilize your eating patterns.")
    
    if not irregular_calorie_patterns.empty:
        suggestions.append("Avoid large fluctuations in calorie intake. Try to keep your meals balanced in calories.")
    
    if len(suggestions) == 0:
        suggestions.append("Your eating pattern seems stable! Keep up the good work!")
    
    return suggestions

# Main function to process and generate report
def analyze_eating_pattern(file_path):
    # Load user data
    data = load_data(file_path)
    
    # Check for irregular meal timings
    irregular_meals = check_meal_timing(data)
    
    # Check for irregular calorie intake
    irregular_calorie_patterns = check_calorie_intake(data)
    
    # Generate suggestions
    suggestions = suggest_improvements(irregular_meals, irregular_calorie_patterns)
    
    # Print the report
    print("Analysis Report:")
    print(f"Total Meals Logged: {len(data)}")
    
    if not irregular_meals.empty:
        print(f"\nIrregular Meal Timings:")
        print(irregular_meals[['meal_time', 'hour', 'minute']])
    
    if not irregular_calorie_patterns.empty:
        print(f"\nIrregular Calorie Intake Patterns:")
        print(irregular_calorie_patterns[['time', 'calories']])
    
    print(f"\nSuggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion}")

# Example usage
file_path = 'myfitnesspal_data.csv'  # Path to the user’s CSV data exported from MyFitnessPal
analyze_eating_pattern(file_path)
