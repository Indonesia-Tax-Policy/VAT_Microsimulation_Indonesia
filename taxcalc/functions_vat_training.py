"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import pandas as pd
import copy
import numpy as np
from taxcalc.decorators import iterate_jit

@iterate_jit(nopython=True)
# Calculate VAT for an item
def calculate_vat(kode_value, vat_rate):
    return kode_value * (vat_rate / (1 + vat_rate))


@iterate_jit(nopython=True)
# Main function
def main():
    # Load data
    record_data = vars['pit_records_variables_filename']
    policy_data = vars['DEFAULTS_FILENAME']
    data_df = vars['pit_data_filename']
    
    # Extract KODE items and their categories from record_variables_vat_indo.json
    kode_items = {key: value for key, value in record_data['read'].items() if key.startswith('KODE_')}
    
    # Debug: Print all KODE items
    print("KODE Items:", kode_items.keys())
    
    # Extract VAT rates from current_law_policy_indo.json
    vat_rates = {
        key.replace('_Rate_KODE_', ''): value['value'][0]
        for key, value in policy_data.items()
        if key.startswith('_Rate_KODE_')
    }
    
    # Debug: Print VAT rates
    print("VAT Rates:", vat_rates)
    
    # Prepare a mapping of KODE_item to category (handle both 'Category' and 'category')
    kode_to_category = {
        kode: details.get('Category', details.get('category', 'Uncategorized'))
        for kode, details in kode_items.items()
    }
    
    # Debug: Print KODE-to-category mapping
    print("KODE to Category Mapping:", kode_to_category)
    
    # Filter columns in the CSV that match KODE items
    relevant_columns = [col for col in data_df.columns if col in kode_items]
    
    # Debug: Print relevant columns found in the CSV
    print("Relevant Columns:", relevant_columns)
    
    # Convert relevant columns to numeric and handle non-numeric values
    for column in relevant_columns:
        data_df[column] = pd.to_numeric(data_df[column], errors='coerce')  # Convert to numeric
        data_df.fillna(0, inplace=True)  # Replace NaN with 0

    # Debug: Check column types after conversion
    print("Column Data Types:")
    print(data_df[relevant_columns].dtypes)

    # Initialize results storage for the four categories
    categories = ['food', 'non_food', 'education', 'health']
    category_results = {category: {'consumption': 0, 'vat_liability': 0} for category in categories}
    
    # Iterate over each person (row) in the dataset
    for _, row in data_df.iterrows():     
        # Process each relevant column (KODE_item)
        for column in relevant_columns:
            item_name = column.replace('KODE_', '')  # Extract item name from column name
            
            if item_name in vat_rates:
                vat_rate = vat_rates[item_name]
                category = kode_to_category.get(column, 'Uncategorized').lower()  # Convert category to lowercase

                if category not in categories:
                    print(f"Warning: Column '{column}' has an unknown category '{category}'. Skipping.")
                
            # Multiply consumption value by WERT
            weighted_consumption_value = row[column] * row['WERT']  # Multiply by WERT
            vat_liability_value = calculate_vat(weighted_consumption_value, vat_rate)  # Calculate VAT
            
            # Aggregate results into overall category results
            category_results[category]['consumption'] += weighted_consumption_value
            category_results[category]['vat_liability'] += vat_liability_value
    
    # Calculate overall totals
    total_consumption = sum(cat['consumption'] for cat in category_results.values())
    total_vat_liability = sum(cat['vat_liability'] for cat in category_results.values())
    
    return total_vat_liability