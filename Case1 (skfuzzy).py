# Imports
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Define linguistic variables and their ranges
temperature = ctrl.Antecedent(np.arange(30, 48, 1), 'Temperature')
headache = ctrl.Antecedent(np.arange(0, 11, 1), 'Headache')
age = ctrl.Antecedent(np.arange(0, 131, 1), 'Age')
urgency = ctrl.Consequent(np.arange(0, 101, 1), 'Urgency')

# Define membership functions for linguistic variables
#Temperature
temperature['low'] = fuzz.trapmf(temperature.universe, [0, 0, 35, 36]) 
temperature['normal'] = fuzz.trapmf(temperature.universe, [35, 36, 37, 38])
temperature['high'] = fuzz.trapmf(temperature.universe, [37, 41, 100, 100])
# Headache
headache['low'] = fuzz.trimf(headache.universe, [0, 0, 5])
headache['moderate'] = fuzz.trimf(headache.universe, [2, 5, 8])
headache['high'] = fuzz.trimf(headache.universe, [5, 10, 10])
# Age
age['young'] = fuzz.trapmf(age.universe, [0, 0, 15, 40])
age['middle_aged'] = fuzz.trimf(age.universe, [15, 40, 65])
age['old'] = fuzz.trapmf(age.universe, [40, 70, 130, 130])
# Urgency
urgency['not_urgent'] = fuzz.trimf(urgency.universe, [0, 0, 40])
urgency['less_urgent'] = fuzz.trimf(urgency.universe, [20, 40, 60])
urgency['urgent'] = fuzz.trimf(urgency.universe, [40, 60, 80])
urgency['extremely_urgent'] = fuzz.trimf(urgency.universe, [60, 100, 100])

# Define fuzzy rules

# temp(low) + headache(high) + age(young) -> urgent
# temp(low) + headache(high) + age(middle age) -> urgent
# temp(low) + headache(high) + age(old) ->  urgent
rule1 = ctrl.Rule(temperature['low'] & headache['high'], urgency['urgent'])

# temp(low) + headache(moderate) + age(young) -> less urgent
# temp(low) + headache(moderate) + age(middle age) -> less urgent
# temp(low) + headache(moderate) + age(old) -> less urgent
rule2 = ctrl.Rule(temperature['low'] & headache['moderate'], urgency['less_urgent'])

# temp(low) + headache(low) + age(young) -> not urgent
# temp(low) + headache(low) + age(middle age) -> not urgent
# temp(low) + headache(low) + age(old) -> not urgent
# temp(normal) + headache(low) + age(young) -> not urgent
# temp(normal) + headache(low) + age(middle age) -> not urgent
# temp(normal) + headache(low) + age(old) -> not urgent
rule3 = ctrl.Rule((temperature['low'] | temperature['normal']) & headache['low'], urgency['not_urgent'])

# temp(normal) + headache(moderate) + age(young) -> not urgent
rule4 = ctrl.Rule(temperature['normal'] & headache['moderate'] & age['young'], urgency['not_urgent'])

# temp(normal) + headache(high) + age(young) -> less urgent
rule5 = ctrl.Rule(temperature['normal'] & headache['high'] & age['young'], urgency['less_urgent'])

# temp(high) + headache(low) + age(young) -> less urgent
# temp(high) + headache(low) + age(middle age) -> less urgent
rule6 = ctrl.Rule(temperature['high'] & headache['low'] & (age['young'] | age['middle_aged']), urgency['less_urgent'])

# temp(high) + headache(moderate) + age(young) -> urgent
# temp(high) + headache(high) + age(young) -> urgent
rule7=ctrl.Rule(temperature['high'] & (headache['moderate'] | headache['high']) & age['young'], urgency['urgent'])

# temp(normal) + headache(moderate) + age(middle age) -> less urgent
# temp(normal) + headache(moderate) + age(old) -> less urgent
rule8 = ctrl.Rule(temperature['normal'] & headache['moderate'] & (age['middle_aged'] | age['old']), urgency['less_urgent'])

# temp(normal) + headache(high) + age(middle age) -> urgent
# temp(normal) + headache(high) + age(old) -> urgent
rule9 = ctrl.Rule(temperature['normal'] & headache['high'] & (age['middle_aged'] | age['middle_aged']), urgency['urgent'])

# temp(high) + headache(moderate) + age(middle age) -> urgent
rule10 = ctrl.Rule(temperature['high'] & headache['moderate'] & age['middle_aged'], urgency['urgent'])

# temp(high) + headache(high) + age(middle age) -> extremely urgent
rule11=ctrl.Rule(temperature['high']&headache['high']&age['middle_aged'],urgency['extremely_urgent'])

# temp(high) + headache(low) + age(old) -> urgent
rule12 = ctrl.Rule(temperature['high'] & headache['low'] & age['old'], urgency['urgent'])

# temp(high) + headache(high) + age(old) -> extremely urgent
# temp(high) + headache(moderate) + age(old) -> extremely urgent
rule13 = ctrl.Rule(temperature['high'] &(headache['high']| headache['moderate']) & age['old'], urgency['extremely_urgent'])

# Create a control system
urgency_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13])

# Create a simulation for the control system
urgency_sim = ctrl.ControlSystemSimulation(urgency_ctrl)

def visualize():
    plt.close('all')
    # Visualize the plots
    temperature.view()
    headache.view()
    age.view()
    urgency.view(sim=urgency_sim)

    # Show the plots
    plt.show(block = False)

# User input function
def user_input():
    while True:
        # Get User Input
        temperature = float(input("Temperature: "))
        headache = int(input("Headache: "))
        age = int(input("Age: "))

        # Feed the user input to the simulation
        urgency_sim.input['Temperature'] = temperature
        urgency_sim.input['Headache'] = headache
        urgency_sim.input['Age'] = age

        # Perform the computation
        urgency_sim.compute()   

        # Get the output value for urgency
        urgency_value = urgency_sim.output['Urgency']
        print("Urgency:", urgency_value)

        # Visualize
        visualize()

        if input("Press Enter to continue. X to exit") != "":
            break

if __name__ == "__main__":
    user_input()
