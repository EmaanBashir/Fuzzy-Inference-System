# Fuzzy Inference System for Medical Urgency Prediction

This project implements a **Fuzzy Inference System (FIS)** to predict the medical urgency of patients based on **temperature, age, and headache severity**. The system supports both **numeric and interval-based inputs**, allowing it to handle **uncertainty** when exact values are not known. This report details the fuzzy modeling process and discusses different input types, membership functions, and fuzzy rules used for decision-making.

---

## 📌 Table of Contents
- [Introduction](#introduction)
- [Model Design](#model-design)
- [Methodology](#methodology)
- [Linguistic Variables](#linguistic-variables)
- [Membership Functions](#membership-functions)
- [Fuzzy Rules](#fuzzy-rules)
- [Defuzzification](#defuzzification)
- [Technology Used](#technology-used)
- [Installation and Requirements](#installation-and-requirements)
- [Usage Instructions](#usage-instructions)
- [Project Structure](#project-structure)
- [Results and Discussion](#results-and-discussion)
- [References](#references)

---

## 📖 Introduction
The project applies **fuzzy logic** in healthcare to estimate patient urgency levels using linguistic variables. It supports:
- **Numeric Inputs:** Crisp values for temperature, age, and headache severity.
- **Interval-valued Inputs:** Fuzzy values for cases where exact inputs are uncertain.

The system calculates urgency based on **fuzzy rules**, applies **membership functions**, and uses **defuzzification** to obtain a crisp urgency score.

---

## 🏗 Model Design
Two types of models were designed:
1. **Numeric Input Model:** Uses singleton fuzzification to convert precise input values into fuzzy sets.
2. **Interval-Valued Model:** Uses non-singleton fuzzy sets to handle uncertainty when input values are imprecise.

---

## 🔬 Methodology
The fuzzy system follows these steps:
1. **Definition of linguistic variables**
2. **Design of membership functions**
3. **Formulation of fuzzy rules**
4. **Computation of firing strength for each rule**
5. **Defuzzification to obtain a crisp urgency score**

---

## 📝 Linguistic Variables
The system defines the following variables:

### **Inputs:**
- **Temperature:** Low, Normal, High (34°C - 44°C)
- **Headache:** Low, Moderate, High (0 - 10 scale)
- **Age:** Young, Middle-aged, Old (0 - 130 years)

### **Output:**
- **Urgency:** Not Urgent, Less Urgent, Urgent, Extremely Urgent (0 - 100 scale)

---

## 📊 Membership Functions
Membership functions define how input values are mapped to linguistic terms. The system uses:
- **Trapezoidal functions** for age categories (Young, Old)
- **Triangular functions** for urgency and headache levels
- **Gaussian functions** for interval-based input representation

---

## 🔄 Fuzzy Rules
The fuzzy system uses **27 rules** developed with input from a medical expert. Example rules:
- **IF** temperature is high **AND** headache is severe **AND** age is old **THEN** urgency is extremely urgent.
- **IF** temperature is normal **AND** headache is moderate **AND** age is young **THEN** urgency is not urgent.

---

## 🎯 Defuzzification
The system uses **Centroid Defuzzification** to calculate a crisp urgency value based on the fuzzy output.

---

## 🛠 Technology Used
- **Python**
- **NumPy** - Numerical computations
- **Matplotlib** - Data visualization
- **SciPy** - Gaussian function calculations

---

## 📌 Installation and Requirements
Ensure you have **Python 3.7+** installed. Install the required libraries using:
```bash
pip install numpy matplotlib scipy
```

---

## ▶️ Usage Instructions
1. **Run the script:**
   ```bash
   python Assignment.py
   ```
2. **Choose an input type:**
   - `1`: Numeric inputs (Enter exact values for temperature, headache, and age)
   - `2`: Interval inputs (Enter an interval range for each variable)
3. **View the output:**
   - The program will display the urgency level and membership functions graph.

---

## 📊 Results and Discussion
The system was evaluated on different cases:
- **Numeric input** provides a precise urgency level.
- **Interval-valued input** captures uncertainty and smoothens variations in urgency.
- **Gaussian function** improves robustness by handling input vagueness.

### **Sample Results**
| Temperature | Headache | Age | Urgency |
|------------|---------|-----|---------|
| 36         | 1       | 15  | 13.75   |
| 38.5       | 5.5     | 35  | 64.35   |
| 39.25      | 6.9     | 50  | 72.07   |
| 38.5-39    | 7.5-8.1 | 54-56 | 80.64 |

---

## 📚 References
Pekaslan, D., Garibaldi, J. M., & Wagner, C. (2018). Exploring Subsethood to Determine Firing Strength in Non-Singleton Fuzzy Logic Systems. IEEE International Conference on Fuzzy Systems.

---

