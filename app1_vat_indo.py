"""
app1.py illustrates use of pitaxcalc-demo release 2.0.0 (India version).
USAGE: python app1.py > app1.res
CHECK: Use your favorite Windows diff utility to confirm that app1.res is
       the same as the app1.out file that is in the repository.
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from stata_python import *

# Initialize the variables

vars = {}

vars['pit'] = 1
vars['cit'] = 0
vars['vat'] = 0

tax_type = 'pit'
vars['DEFAULTS_FILENAME'] = "current_law_policy_vat_Indonesia_susenas_2018.json"
vars['GROWFACTORS_FILENAME'] = "growfactors_vat_indo_static.csv" 
vars['pit_data_filename'] = "sampled_merged_susenas_Indo_utf8.csv"
vars['pit_weights_filename'] = "weight_vat_indo_app.csv"
vars['pit_records_variables_filename'] = "records_variables_vat_indo_ade.json"
vars['pit_benchmark_filename'] = "tax_incentives_benchmark_pit_training.json"
vars['pit_elasticity_filename'] = "elasticity_pit_training.json"
vars['pit_functions_filename'] = "generated_vat_functions.py"
vars['pit_function_names_filename'] = "function_names_vat_indo_ade.json"
vars['pit_distribution_json_filename'] = "vat_distribution_indo.json"

vars['vat_data_filename'] = "gst.csv"
vars['vat_weights_filename'] = "gst_weights.csv"
vars['vat_records_variables_filename'] = "gstrecords_variables.json"  

vars['cit_data_filename'] = "cit_cross.csv"
vars['cit_weights_filename'] = "cit_cross_wgts1.csv"
vars['cit_records_variables_filename'] = "corprecords_variables.json"

vars['gdp_filename'] = 'gdp_nominal_training.csv'
vars["start_year"] = 2022
vars["end_year"] = 2027
vars["SALARY_VARIABLE"] = "CONS_total"
vars['elasticity_filename'] = "elasticity_pit_training.json"
vars['DIST_VARIABLES'] = ['weight', 'CONS_total', 'vat']
vars['DIST_TABLE_COLUMNS'] = ['weight', 'CONS_total', 'vat']        
vars['DIST_TABLE_LABELS'] = ['Population',
                     'Total Consumption',
                     'VAT']
vars['DECILE_ROW_NAMES'] = ['0-10n', '0-10z', '0-10p',
                    '10-20', '20-30', '30-40', '40-50',
                    '50-60', '60-70', '70-80', '80-90', '90-100',
                    'ALL',
                    '90-95', '95-99', 'Top 1%']
vars['STANDARD_ROW_NAMES'] = [ "<0", "=0", "0-0.5 m", "0.5-1m", "1-1.5m", "1.5-2m",
                      "2-3m", "3-4m", "4-5m", "5-10m", ">10m", "ALL"]
vars['STANDARD_INCOME_BINS'] = [-9e99, -1e-9, 1e-9, 5e5, 10e5, 15e5, 20e5, 30e5,
                        40e5, 50e5, 100e5, 9e99]
vars['income_measure'] = "total_gross_income"
vars['show_error_log'] = 0
vars['verbose'] = 0
vars['data_start_year'] = 2018

f = open('C:/Users/adeda/Microsimulation/Tax_Microsimulation/taxcalc/'+vars['pit_distribution_json_filename'])
distribution_vardict_dict = json.load(f)
f.close()
#print(distribution_vardict_dict)
           
with open('global_vars.json', 'w') as f:
    f.write(json.dumps(vars, indent=2))
f.close()

from taxcalc import *


# create Records object containing pit.csv and pit_weights.csv input data
recs = Records()

# create Policy object containing current-law policy
pol = Policy()

# specify Calculator object for current-law policy
calc1 = Calculator(policy=pol, records=recs, verbose=False)
calc1.calc_all()

# specify Calculator object for reform in JSON file
reform = Calculator.read_json_param_objects('app0_reform_vat_indo_uu_7.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, verbose=False)
calc2.calc_all()

# compare aggregate results from two calculators
weighted_tax1 = calc1.weighted_total_pit('vat')
weighted_tax2 = calc2.weighted_total_pit('vat')
total_weights = calc1.total_weight_pit()
print(f'Tax 1 {weighted_tax1 * 1e-9:,.2f}')
print(f'Tax 2 {weighted_tax2 * 1e-9:,.2f}')
print(f'Total weight {total_weights * 1e-6:,.2f}')

calc1.advance_to_year(2022)
calc2.advance_to_year(2022)
calc1.calc_all()
calc2.calc_all()

# compare aggregate results from two calculators
weighted_tax1 = calc1.weighted_total_pit('vat')
weighted_tax2 = calc2.weighted_total_pit('vat')
total_weights = calc1.total_weight_pit()
print(f'VAT Collection Pre Reform: {weighted_tax1 * 1e-9:,.2f}')
print(f'VAT Collection Post Reform: {weighted_tax2 * 1e-9:,.2f}')
print(f'Total population {total_weights * 1e-6:,.2f}')

# dump out records
dump_vars = ['id_n', 'Year', 'CONS_total', 'vat']
dumpdf = calc1.dataframe(dump_vars)
dumpdf['vat1'] = calc1.array('vat')
dumpdf['vat2'] = calc2.array('vat')
dumpdf['vat_diff'] = dumpdf['vat2'] - dumpdf['vat1']
column_order = dumpdf.columns

dumpdf.to_csv('app1-dump_vat_UU_7.csv', columns=column_order,
              index=False, float_format='%.0f')

def calc_gini(values, sort=None):
    n = len(values)
    #cumulative_income = np.cumsum(income)
    cumulative_values= values.sum()
    gini_index = ((2 * np.sum((np.arange(1, n + 1) * values))) / (n *
    cumulative_values)) - ((n + 1) / n)
    return gini_index

def plot_lorenz_curve_reform(values_pre, values_post, gini_pre, gini_post, label1, label2, title):
    """Plot the Lorenz Curve given an array of values and the Gini coefficient."""
    values_pre = np.sort(values_pre)
    values_pre = np.append([0], values_pre)  # Start at 0
    cum_values_pre = np.cumsum(values_pre) / np.sum(values_pre)  # Normalize cumulative values
    cum_pop_pre = np.linspace(0, 1, len(cum_values_pre))  # Population percentage

    values_post = np.sort(values_post)
    values_post = np.append([0], values_post)  # Start at 0
    cum_values_post = np.cumsum(values_post) / np.sum(values_post)  # Normalize cumulative values
    cum_pop_post = np.linspace(0, 1, len(cum_values_post))  # Population percentage
    
    plt.figure(figsize=(8, 6))
    plt.plot(cum_pop_pre, cum_values_pre, label=label1)
    plt.plot(cum_pop_post, cum_values_post, label=label2)
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")  # Perfect equality line
    plt.fill_between(cum_pop_pre, cum_values_pre, cum_values_post, color="skyblue", alpha=0.5)

    plt.xlabel("Cumulative Population Share")
    plt.ylabel("Cumulative Income Share")
    plt.title(f"{title} {gini_post-gini_pre:.4f}")
    plt.legend()
    plt.grid(True)
    plt.show()
    
dumpdf = dumpdf.sort_values(by=['CONS_total'])
# Extract relevant field
values_pre = dumpdf['CONS_total'].dropna().values  # Remove NaNs if any
gini_pre = calc_gini(values_pre)
print(f'Gini of Total Consumption Pre Reform : {gini_pre:.2f}')
title = 'Gini Pre Reform : '  

# Extract relevant field
values_post = dumpdf['vat1'].dropna().values  # Remove NaNs if any
gini_post = calc_gini(values_post)
print(f'Gini of VAT Pre Reform : {gini_post:.2f}')

print("Kakwani Index: %0.2f." % (gini_post - gini_pre))

title = 'Kakwani Index : ' 
# Plot Lorenz Curve
label1 = "Lorenz Curve of Total Consumption"
label2 =  "Lorenz Curve of VAT Pre Reform"
plot_lorenz_curve_reform(values_pre, values_post, gini_pre, gini_post, label1, label2, title)

# Extract relevant field
values_post = dumpdf['vat2'].dropna().values  # Remove NaNs if any
gini_post = calc_gini(values_post)
print(f'Gini of VAT Post Reform : {gini_post:.2f}')

print("Kakwani Index: %0.2f." % (gini_post - gini_pre))

title = 'Kakwani Index : ' 
# Plot Lorenz Curve
label1 = "Lorenz Curve of Total Consumption"
label2 =  "Lorenz Curve of VAT Post Reform"
plot_lorenz_curve_reform(values_pre, values_post, gini_pre, gini_post, label1, label2, title)
