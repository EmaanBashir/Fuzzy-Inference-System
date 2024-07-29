# Name: Emaan Bashir
# Student Id: 20594616

# Instructions
# You can directly run the code
# It will give two choices: 1. Numeric input
#                           2. Interval-value input
# For option 1 you need to enter the numeric values of temperature, headache and age in order to get the output urgency
# For option 2 you need to enter the start and end of interval for temperature, headache and age in order to get the output urgency
#
# Press Enter to continue or any other key + Enter to quit.

# Imports
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad

# Define the range for the variables
temperature_domain = [34, 44]
headache_domain = [0, 10]
age_domain = [0, 130]
urgency_domain = [0, 100]


### Membership functions for different linguistic variables

# function for variables having only one positive slope
def positive_slope(x, values):
    if x <= values[0]:
        return 0
    elif x >= values[1]:
        return 1
    else:
        return (x - values[0])/(values[1] - values[0])

# function for variables having only one negative slope
def negative_slope(x, values):
    if x <= values[0]:
        return 1
    elif x >= values[1]:
        return 0
    else:
        return (values[1] - x)/(values[1] - values[0])
    
# function for variables having a triangular shape with a positive and negative slope
def pos_neg_slope(x, values):
    if x <= values[0] or x >= values[3]:
        return 0
    elif x >= values[1] and x <= values[2]:
        return 1
    elif x < values[1]:
        return (x - values[0])/(values[1] - values[0])
    else:
        return (values[3] - x)/(values[3] - values[2])


### Define membership functions for all the variables involved

# Temperature
def temp_low(x):
    return negative_slope(x, [35, 36])

def temp_normal(x):
    return pos_neg_slope(x, [35, 36, 37, 38])

def temp_high(x):
    return positive_slope(x, [37, 41])

# Headache
def headache_low(x):
    return negative_slope(x, [0, 5])
    
def headache_moderate(x):
    return pos_neg_slope(x, [2, 5, 5, 8])
    
def headache_high(x):
    return positive_slope(x, [5, 10])
    
# Age
def young(x):
    return negative_slope(x, [15, 40])
    
def middle_aged(x):
    return pos_neg_slope(x, [14, 40, 40, 65])

def old(x):
    return positive_slope(x, [40, 70])

# Urgency
def not_urgent(x):
    return negative_slope(x, [0, 40])

def less_urgent(x):
    return pos_neg_slope(x, [20, 40, 40, 60])

def urgent(x):
    return pos_neg_slope(x, [40, 60, 60, 80])

def extremely_urgent(x):
    return positive_slope(x, [60, 100])
    
# Define the Gaussian function
def gaussian(x, a, mu, sd):
    return a * np.exp(-(x - mu)**2 / (2 * sd**2))

# Calculate crisp values for an interval based on the degree of overlap with the input membership functions
def crisp_values(interval, functions):
    membs = []
    a = 1 # Max height 
    mu = (interval[1] + interval[0])/2 # Mean
    sd = (interval[1] - interval[0])/3 # Standard Deviation
    
    # if the interval start and end is same
    if interval[0] == interval[1]:
        return [f(interval[0]) for f in functions]

    # Gaussian Function for the input interval
    def interval_gaussian(x):
        return gaussian(x, a, mu, sd)

    # Combined Total Interval Area
    total_area = quad(interval_gaussian, interval[0], interval[1])[0]

    # Calculate the membership based on the overlap between the function and the interval
    for f in functions:
        
        # Calculate the overlap at each point
        def min_func(x):
            return min(f(x), interval_gaussian(x))
        
        area = quad(min_func, interval[0], interval[1])[0]
        membs.append(area/total_area)

    return membs

# Calculate the output based on fuzzy logic rules
def output(x, temp, headache, age, is_interval = False):
    
    # In case of intervals, convert the intervals into crisp values
    if is_interval:
        temp_l, temp_n, temp_h = crisp_values(temp, [temp_low, temp_normal, temp_high])
        headache_l, headache_m, headache_h = crisp_values(headache, [headache_low, headache_moderate, headache_high])
        age_y, age_m, age_o = crisp_values(age, [young, middle_aged, old])

    # In case of numeric inputs, calculate the degrees of membership
    else:
        temp_l = temp_low(temp)
        temp_n = temp_normal(temp)
        temp_h = temp_high(temp)
        headache_l = headache_low(headache)
        headache_m = headache_moderate(headache)
        headache_h = headache_high(headache)
        age_y = young(age)
        age_m = middle_aged(age)
        age_o = old(age)

    # Fuzzy Logic Rules

    # temp(low) + headache(high) + age(young) -> urgent
    # temp(low) + headache(high) + age(middle age) -> urgent
    # temp(low) + headache(high) + age(old) ->  urgent
    rule1 = min(temp_l, headache_h, max(age_y, age_m, age_o), urgent(x))

    # temp(low) + headache(moderate) + age(young) -> less urgent
    # temp(low) + headache(moderate) + age(middle age) -> less urgent
    # temp(low) + headache(moderate) + age(old) -> less urgent
    rule2 = min(temp_l, headache_m, max(age_y, age_m, age_o), less_urgent(x))
    
    # temp(low) + headache(low) + age(young) -> not urgent
    # temp(low) + headache(low) + age(middle age) -> not urgent
    # temp(low) + headache(low) + age(old) -> not urgent
    # temp(normal) + headache(low) + age(young) -> not urgent
    # temp(normal) + headache(low) + age(middle age) -> not urgent
    # temp(normal) + headache(low) + age(old) -> not urgent
    rule3 = min(max(temp_l, temp_n), headache_l, max(age_y, age_m, age_o), not_urgent(x))

    # temp(normal) + headache(moderate) + age(young) -> not urgent
    rule4 = min(temp_n, headache_m, age_y, not_urgent(x))

    # temp(normal) + headache(high) + age(young) -> less urgent
    rule5 = min(temp_n, headache_h, age_y, less_urgent(x))

    # temp(high) + headache(low) + age(young) -> less urgent
    # temp(high) + headache(low) + age(middle age) -> less urgent
    rule6 = min(temp_h, headache_l, max(age_y, age_m), less_urgent(x))

    # temp(high) + headache(moderate) + age(young) -> urgent
    # temp(high) + headache(high) + age(young) -> urgent
    rule7 = min(temp_h, max(headache_m, headache_h), age_y, urgent(x))

    # temp(normal) + headache(moderate) + age(middle age) -> less urgent
    # temp(normal) + headache(moderate) + age(old) -> less urgent
    rule8 = min(temp_n, headache_m, max(age_m, age_o), less_urgent(x))

    # temp(normal) + headache(high) + age(middle age) -> urgent
    # temp(normal) + headache(high) + age(old) -> urgent
    rule9 = min(temp_n, headache_h, max(age_m, age_o), urgent(x))

    # temp(high) + headache(moderate) + age(middle age) -> urgent
    rule10 = min(temp_h, headache_m, age_m, urgent(x))

    # temp(high) + headache(high) + age(middle age) -> extremely urgent
    rule11 = min(temp_h, headache_h, age_m, extremely_urgent(x))

    # temp(high) + headache(low) + age(old) -> urgent
    rule12 = min(temp_h, headache_l, age_o, urgent(x))

    # temp(high) + headache(high) + age(old) -> extremely urgent
    # temp(high) + headache(moderate) + age(old) -> extremely urgent
    rule13 = min(temp_h, max(headache_h, headache_m), age_o, extremely_urgent(x))

    # Return the output urgency
    return max(rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13)
        
# Visualize the membership functions and the output
def visualize(temp, headache, age, is_interval = False):
    # Close the pervious graph before creating a new one
    plt.close('all')
    
    # Define the subplots
    fig, axes = plt.subplots(2, 3, figsize = (15, 7))

    # Define the x-axis of the plots
    temp_x = np.linspace(temperature_domain[0], temperature_domain[1], 1000)
    headache_x = np.linspace(headache_domain[0], headache_domain[1], 1000)
    age_x = np.linspace(age_domain[0], age_domain[1], 1000)
    urgency_x = np.linspace(urgency_domain[0], urgency_domain[1], 1000)

    ### Define the y-axis of the plots 
    # Temperature
    y_temp_low = [temp_low(i) for i in temp_x]
    y_temp_normal = [temp_normal(i) for i in temp_x]
    y_temp_high = [temp_high(i) for i in temp_x]
    
    # Headache
    y_headache_low = [headache_low(i) for i in headache_x]
    y_headache_moderate = [headache_moderate(i) for i in headache_x]
    y_headache_high = [headache_high(i) for i in headache_x]
    
    # Age
    y_young = [young(i) for i in age_x]
    y_middle_aged = [middle_aged(i) for i in age_x]
    y_old = [old(i) for i in age_x]
    
    # Urgency
    y_not_urgent = [not_urgent(i) for i in urgency_x]
    y_less_urgent = [less_urgent(i) for i in urgency_x]
    y_urgent = [urgent(i) for i in urgency_x]
    y_extremely_urgent = [extremely_urgent(i) for i in urgency_x]

    # Output
    y_urgency = [output(i, temp, headache, age, is_interval) for i in urgency_x]

    ### Plot the graphs
    # Temperature
    axes[0, 0].plot(temp_x, y_temp_low, label = 'Low', color = 'green')
    axes[0, 0].plot(temp_x, y_temp_normal, label = 'Normal', color = 'blue')
    axes[0, 0].plot(temp_x, y_temp_high, label = 'High', color = 'red')
    if is_interval: 
        # Indicate the start and end of the input interval
        axes[0, 0].axvline(temp[0], color='purple', linestyle='--')
        axes[0, 0].axvline(temp[1], color='purple', linestyle='--')
        # Draw a gaussian function for the interval
        gaussian_x = np.linspace(temp[0], temp[1], 1000)
        gaussian_y = [gaussian(i, a = 1, mu = (temp[1] + temp[0])/2, sd = (temp[1] - temp[0])/3) for i in gaussian_x]
        axes[0, 0].plot(gaussian_x, gaussian_y, label = 'Temperature Interval', color = 'black', linestyle = ':')
    else: # Indicate the user input
        axes[0, 0].axvline(temp, color='purple', linestyle='--', label = 'Temperature')
    axes[0, 0].set_title('Temperature')

    # Headache
    axes[0, 1].plot(headache_x, y_headache_low, label = 'Low', color = 'green')
    axes[0, 1].plot(headache_x, y_headache_moderate, label = 'Moderate', color = 'blue')
    axes[0, 1].plot(headache_x, y_headache_high, label = 'High', color = 'red')
    if is_interval: 
        # Indicate the start and end of the input interval
        axes[0, 1].axvline(headache[0], color='purple', linestyle='--')
        axes[0, 1].axvline(headache[1], color='purple', linestyle='--')
        # Draw a gaussian function for the interval
        gaussian_x = np.linspace(headache[0], headache[1], 1000)
        gaussian_y = [gaussian(i, a = 1, mu = (headache[1] + headache[0])/2, sd = (headache[1] - headache[0])/3) for i in gaussian_x]
        axes[0, 1].plot(gaussian_x, gaussian_y, label = 'Headache Interval', color = 'black', linestyle = ':')
    else: # Indicate the user input
        axes[0, 1].axvline(headache, color='purple', linestyle='--', label = 'Headache')
    axes[0, 1].set_title('Headache')

    # Age
    axes[0, 2].plot(age_x, y_young, label = 'Young', color = 'green')
    axes[0, 2].plot(age_x, y_middle_aged, label = 'Middle Aged', color = 'blue')
    axes[0, 2].plot(age_x, y_old, label = 'Old', color = 'red')
    if is_interval: 
        # Indicate the start and end of the input interval
        axes[0, 2].axvline(age[0], color='purple', linestyle='--')
        axes[0, 2].axvline(age[1], color='purple', linestyle='--')
        # Draw a gaussian function for the interval
        gaussian_x = np.linspace(age[0], age[1], 1000)
        gaussian_y = [gaussian(i, a = 1, mu = (age[1] + age[0])/2, sd = (age[1] - age[0])/3) for i in gaussian_x]
        axes[0, 2].plot(gaussian_x, gaussian_y, label = 'Age Interval', color = 'black', linestyle = ':')
    else: # Indicate the user input
        axes[0, 2].axvline(age, color='purple', linestyle='--', label = 'Age')
    axes[0, 2].set_title('Age')

    # Urgency
    axes[1, 0].plot(urgency_x, y_not_urgent, label = 'Not Urgent', color = 'purple')
    axes[1, 0].plot(urgency_x, y_less_urgent, label = 'Less Urgent', color = 'green')
    axes[1, 0].plot(urgency_x, y_urgent, label = 'Urgent', color = 'blue')
    axes[1, 0].plot(urgency_x, y_extremely_urgent, label = 'Extremely Urgent', color = 'red')
    axes[1, 0].set_title('Urgency')
    # Shade the output area
    axes[1, 0].fill_between(urgency_x, 0, y_urgency, color='blue', alpha=0.3)

    # Output Plot
    axes[1, 1].plot(urgency_x, y_urgency, color = 'blue')
    axes[1, 1].set_title('Urgency Output')

    # Calculate the centroid
    defuzzified = centroid_defuzzification(urgency_x, y_urgency)

    # Plot the centroid
    # axes[1, 0].axvline(defuzzified, color='black', linestyle='--', label = 'Centroid')
    axes[1, 1].axvline(defuzzified, color='purple', linestyle='--', label = 'Centroid')
    axes[1, 1].text(defuzzified, 0.1, f'{defuzzified:.2f}', color='purple', ha='right')

    # Display the defuzzified output
    print("\nDefuzzified Urgency:", defuzzified)

    #Remove the empty subplot
    axes[1, 2].axis('off')

    # Label axes and set limits
    labels = ['Temperature', 'Headache', 'Age', 'Urgency', 'Urgency Output']
    axes_list = axes.flat
    i = 0
    for label in labels:
        ax = axes_list[i]
        ax.set_ylim(0, 1)
        ax.set_xlabel(label)
        ax.set_ylabel('Membership')
        ax.grid(True)
        ax.legend()
        i+=1

    # Display the plots
    plt.tight_layout() 
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.show(block = False)

# Centroid defuzzification to obtain a crisp output value
def centroid_defuzzification(x, y):
    return sum([a * b for a, b in zip(x, y)]) / sum(y)

# Handle User Input
def user_input():

    while True:
        try:
            # Ask the user for the type of fuzzy system
            print("\nChoose the type of fuzzy system.\n1) Numeric input\n2) Interval-valued input")
            option = int(input("\nEnter option number (Any other number to exit): "))

            # Numeric Input
            if option == 1:

                is_interval = False
                temperature = float(input("\nTemperature: "))
                headache = float(input("Headache: "))
                age = float(input("Age: "))

            # Interval Input
            elif option == 2:
                
                is_interval = True

                print('\nTemperature')
                temp1 = float(input("Interval start: "))
                temp2 = float(input("Interval end: "))

                print('\nHeadache')
                headache1 = float(input("Interval start: "))
                headache2 = float(input("Interval end: "))

                print('\nAge')
                age1 = float(input("Interval start: "))
                age2 = float(input("Interval end: "))

                temperature = [temp1, temp2]
                headache = [headache1, headache2]
                age = [age1, age2]
                
            else:
                # Exit the loop if incorrect option is entered
                break

            # Visualize the Fuzzy System
            visualize(temperature, headache, age, is_interval)

            if input("\nPress Enter to continue. (Any key + Enter to exit)") != "":
                break

        except Exception as e:
            # Exception for Invalid inputs
            print('\nInvalid Input')
            print(e)

if __name__ == "__main__":
    user_input()



