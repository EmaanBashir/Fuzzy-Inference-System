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
- **Trapezoidal functions** for temperature and age categories
- **Triangular functions** for urgency and headache levels

<p align="center">
  <img src="https://github.com/user-attachments/assets/4d2dabde-4361-4de2-8350-ddd9298520ac" height="200">
  <img src="https://github.com/user-attachments/assets/dcef644d-8237-4764-81f6-879481a64082" height="200">
  <img src="https://github.com/user-attachments/assets/68abca55-7d1b-45e2-ab10-e2ed9c059af0" height="200">
   <img src="https://github.com/user-attachments/assets/bcb1d82a-0613-46d1-83ac-07edac78531b" height="200">
</p>

---

## 🔄 Fuzzy Rules
The fuzzy system uses **27 rules** developed with input from a medical expert

```
1. IF temperature is low AND headache is low AND age is young THEN not-urgent.
2. IF temperature is low AND headache is moderate AND age is young THEN less-urgent.
3. IF temperature is low AND headache is high AND age is young THEN urgent.
4. IF temperature is normal AND headache is low AND age is young THEN not-urgent.
5. IF temperature is normal AND headache is moderate AND age is young THEN not-urgent.
6. IF temperature is normal AND headache is high AND age is young THEN less-urgent.
7. IF temperature is high AND headache is low AND age is young THEN less-urgent.
8. IF temperature is high AND headache is moderate AND age is young THEN urgent.
9. IF temperature is high AND headache is high AND age is young THEN urgent.
10. IF temperature is low AND headache is low AND age is middle-aged THEN not-urgent.
11. IF temperature is low AND headache is moderate AND age is middle-aged THEN less-urgent.
12. IF temperature is low AND headache is high AND age is middle-aged THEN urgent.
13. IF temperature is normal AND headache is low AND age is middle-aged THEN not-urgent.
14. IF temperature is normal AND headache is moderate AND age is middle-aged THEN less-urgent.
15. IF temperature is normal AND headache is high AND age is middle-aged THEN urgent.
16. IF temperature is high AND headache is low AND age is middle-aged THEN less-urgent.
17. IF temperature is high AND headache is moderate AND age is middle-aged THEN urgent.
18. IF temperature is high AND headache is high AND age is middle-aged THEN extremely-urgent.
19. IF temperature is low AND headache is low AND age is old THEN not-urgent.
20. IF temperature is low AND headache is moderate AND age is old THEN less-urgent.
21. IF temperature is low AND headache is high AND age is old THEN urgent.
22. IF temperature is normal AND headache is low AND age is old THEN not-urgent.
23. IF temperature is normal AND headache is moderate AND age is old THEN less-urgent.
24. IF temperature is normal AND headache is high AND age is old THEN urgent.
25. IF temperature is high AND headache is low AND age is old THEN urgent.
26. IF temperature is high AND headache is moderate AND age is old THEN extremely-urgent.
27. IF temperature is high AND headache is high AND age is old THEN extremely-urgent.
```
---
## 📏 Degree of Truth of an Antecedent
The degree of truth for each antecedent is determined based on the type of input:

### **Numeric Input:**
- The numeric input is converted into a **singleton fuzzy set**, represented as a spike.
- The degree of truth is obtained by computing the intersection of the input with the antecedent fuzzy set.
- Example:
  - For **age = 35**, the membership degrees could be:
    - Young: **0.2**
    - Middle-aged: **0.8**
    - Old: **0.0**

![image](https://github.com/user-attachments/assets/bacbcc54-0986-47fd-85b2-a51a6580a076)

### **Interval-Valued Input:**
- The interval is converted into a **non-singleton fuzzy set**, typically modeled by a **Gaussian function**, which improves robustness by handling the input vagueness.
- The **subsethood method** is used to compute the degree of truth, as it effectively handles uncertainty.
- Example:
  - For **temperature = 35-37**, the membership degrees might be:
    - Low: **0.26**
    - Normal: **0.85**
    - High: **0.0**

![image](https://github.com/user-attachments/assets/6437b96f-2eea-46a4-927e-d91165c515b9)

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

### Output Examples

**Example 1 (Numeric Input)**
![image](https://github.com/user-attachments/assets/d37c8833-7528-4742-97c0-39fcff9c3428)

**Example 2 (Interval Input)**
![image](https://github.com/user-attachments/assets/0377a45e-ee14-47ed-a13f-4fd7b47992a4)

---

## 📊 Results and Discussion
The system was evaluated on different cases:
- **Numeric input** provides a precise urgency level.
- **Interval-valued input** captures uncertainty and smoothens variations in urgency.

### **Sample Results**
![image](https://github.com/user-attachments/assets/05a85e03-f5b2-4d1d-9393-0f9bfa02f0f6)

---

## 📚 References
Pekaslan, D., Garibaldi, J. M., & Wagner, C. (2018). Exploring Subsethood to Determine Firing Strength in Non-Singleton Fuzzy Logic Systems. IEEE International Conference on Fuzzy Systems.

---

