# utils/bmr.py

def calculate_bmr(age, gender, height, weight):
    """
    Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation.
    
    Parameters:
        age (int): Age in years
        gender (str): "male" or "female"
        height (float): Height in cm
        weight (float): Weight in kg
    
    Returns:
        float: BMR value
    """
    if gender.lower() == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:  # female
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return round(bmr, 2)


def calculate_tdee(bmr, activity_level="moderate"):
    """
    Calculate Total Daily Energy Expenditure (TDEE) based on activity level.
    
    Parameters:
        bmr (float): Basal Metabolic Rate
        activity_level (str): "sedentary", "light", "moderate", "active", "very_active"
    
    Returns:
        float: Estimated daily calorie requirement
    """
    activity_multipliers = {
        "sedentary": 1.2,       # little or no exercise
        "light": 1.375,         # light exercise/sports 1-3 days/week
        "moderate": 1.55,       # moderate exercise/sports 3-5 days/week
        "active": 1.725,        # hard exercise/sports 6-7 days/week
        "very_active": 1.9      # very hard exercise/sports or physical job
    }

    multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
    tdee = bmr * multiplier
    return round(tdee, 2)
