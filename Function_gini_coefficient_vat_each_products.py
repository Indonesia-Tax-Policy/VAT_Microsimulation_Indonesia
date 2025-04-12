# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 23:06:46 2025

@author: adeda
"""

import pandas as pd
import numpy as np

def gini(array):
    """
    Compute the Gini coefficient of a numpy array.
    
    Parameters:
        array (array-like): 1D array or list of non-negative numbers.
        
    Returns:
        float: Gini coefficient.
    """
    # Convert to numpy array of floats
    array = np.array(array, dtype=float)
    
    # If there are negative values, shift the data so that it is non-negative.
    if np.amin(array) < 0:
        array -= np.amin(array)
    
    # Add a small constant to avoid division by zero
    array += 1e-9
    
    # Sort the array in ascending order
    array = np.sort(array)
    
    n = array.shape[0]
    index = np.arange(1, n + 1)
    
    # Compute the Gini coefficient
    return (np.sum((2 * index - n - 1) * array)) / (n * np.sum(array))

# Read the CSV file
df = pd.read_csv("sampled_merged_susenas_Indo_utf8.csv", encoding="utf-8")

# Initialize a list to store the results
gini_results = []

# Loop through every column in the DataFrame
for col in df.columns:
    # Attempt to convert the column to numeric, non-convertible values become NaN
    numeric_data = pd.to_numeric(df[col], errors='coerce').dropna()
    
    # Only compute if there is numeric data in the column
    if not numeric_data.empty:
        try:
            gini_coef = gini(numeric_data)
            gini_results.append({'Column': col, 'Gini_Coefficient': gini_coef})
        except Exception as e:
            print(f"Error processing column {col}: {e}")

# Create a DataFrame from the results and display it
result_df = pd.DataFrame(gini_results)
print(result_df)

# Optionally, save the results to a new CSV file
result_df.to_csv("gini_coefficients_by_column.csv", index=False)
