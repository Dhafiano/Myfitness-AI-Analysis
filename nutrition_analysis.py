import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# Step 1: Authenticate with MyFitnessPal API (Assuming OAuth)
def authenticate_to_mfp():
    # Pseudo OAuth steps (depends on API setup)
    oauth_token = 'user_oauth_token'  # Replace with actual token
    return oauth_token

# Step 2: Fetch user food log data from MyFitnessPal API
def fetch_food_logs(oauth_token):
    url = "https://api.myfitnesspal.com/v2/food_logs"
    headers = {
        'Authorization': f'Bearer {oauth_token}',
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Assuming data is a list of meals or logs; converting to DataFrame for further analysis
        return pd.DataFrame(data['food_logs'])  # Adjust the key as per actual response
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

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
def analyze_eating_pattern(file_path=None, oauth_token=None):
    if oauth_token:
        # Fetch food logs from MyFitnessPal API if OAuth token is provided
        user_data = fetch_food_logs(oauth_token)
        if user_data is None:
            print("No data available to analyze.")
            return
    elif file_path:
        # Load user data from CSV file
        user_data = pd.read_csv(file_path)
    else:
        print("No valid input data source provided.")
        return
    
    # Check for irregular meal timings
    irregular_meals = check_meal_timing(user_data)
    
    # Check for irregular calorie intake
    irregular_calorie_patterns = check_calorie_intake(user_data)
    
    # Generate suggestions
    suggestions = suggest_improvements(irregular_meals, irregular_calorie_patterns)
    
    # Print the report
    print("Analysis Report:")
    print(f"Total Meals Logged: {len(user_data)}")
    
    if not irregular_meals.empty:
        print(f"\nIrregular Meal Timings:")
        print(irregular_meals[['meal_time', 'hour', 'minute']])
    
    if not irregular_calorie_patterns.empty:
        print(f"\nIrregular Calorie Intake Patterns:")
        print(irregular_calorie_patterns[['time', 'calories']])
    
    print(f"\nSuggestions:")
    for suggestion in suggestions:
        print(f"- {suggestion}")

# Example usage:
oauth_token = authenticate_to_mfp()  # If you have a valid OAuth token
file_path = 'myfitnesspal_data.csv'  # If using a CSV file instead of MyFitnessPal API

# You can either call analyze_eating_pattern with a file or OAuth token
# If you have the OAuth token, use:
# analyze_eating_pattern(oauth_token=oauth_token)

# Or if you have a CSV file, use:
analyze_eating_pattern(file_path=file_path)
