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

# Initialize the variables

vars = {}

vars['pit'] = 1
vars['cit'] = 0
vars['vat'] = 0

tax_type = 'pit'
vars['DEFAULTS_FILENAME'] = "current_law_policy_vat_Indonesia_susenas_2018.json"
vars['GROWFACTORS_FILENAME'] = "growfactors_vat_indo_static.csv" 
vars['pit_data_filename'] = "sampled_merged_susenas_Indo_utf8.csv"
vars['pit_weights_filename'] = "weight_vat_indo_utf8.csv"
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
reform = Calculator.read_json_param_objects('app0_reform_vat_indo_11_everything.json', None)
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
print(f'Tax 1 {weighted_tax1 * 1e-9:,.2f}')
print(f'Tax 2 {weighted_tax2 * 1e-9:,.2f}')
print(f'Total weight {total_weights * 1e-6:,.2f}')

# dump out records
dump_vars = ['id_n', 'Year', 'CONS_total', 'vat']
dumpdf = calc1.dataframe(dump_vars)
dumpdf['vat1'] = calc1.array('vat')
dumpdf = dumpdf.sort_values(by=['vat1'])
dumpdf['vat2'] = calc2.array('vat')
dumpdf['vat_diff'] = dumpdf['vat2'] - dumpdf['vat1']
column_order = dumpdf.columns

dumpdf.to_csv('app1-dump_vat.csv', columns=column_order,
              index=False, float_format='%.0f')


def calc_gini(values, weights):
    """
    Compute the *weighted* Gini of `values` using `weights`.
    Both `values` and `weights` should be 1D arrays of the same length.
    """
    # Sort by values
    idx = np.argsort(values)
    sorted_values = values[idx]
    sorted_weights = weights[idx]
    
    # Cumulative weight
    cum_weights = np.cumsum(sorted_weights)
    total_weight = cum_weights[-1]
    
    # Weighted cumulative sum of the values
    cum_values = np.cumsum(sorted_values * sorted_weights)
    total_value = cum_values[-1]
    
    # The Gini formula can be written in several ways; this is a common approach:
    gini = 1.0 - 2.0 * np.sum(
        (cum_values / total_value) * (sorted_weights / total_weight)
    )
    return gini


dumpdf["vat1"] = calc1.array("vat")
dumpdf["vat2"] = calc2.array("vat")
dumpdf["wts"]  = calc1.array("weight")  # or whichever is the correct weight

gini_pre = calc_gini(dumpdf["vat1"].values, dumpdf["wts"].values)
gini_post = calc_gini(dumpdf["vat2"].values, dumpdf["wts"].values)
print(gini_pre, gini_post)


def plot_weighted_lorenz_curve_reform(values_pre, weights_pre, 
                                      values_post, weights_post, 
                                      gini_pre, gini_post, title):
    """
    Plot the weighted Lorenz curves for pre and post reform.
    The Lorenz curve is computed using the cumulative distribution of weights.
    """
    # Pre-reform: sort by values and compute cumulative distribution
    sorted_idx_pre = np.argsort(values_pre)
    sorted_vals_pre = values_pre[sorted_idx_pre]
    sorted_wts_pre = weights_pre[sorted_idx_pre]
    cum_wts_pre = np.cumsum(sorted_wts_pre)
    total_wt_pre = cum_wts_pre[-1]
    cum_vals_pre = np.cumsum(sorted_vals_pre * sorted_wts_pre)
    total_val_pre = cum_vals_pre[-1]
    x_pre = np.concatenate(([0], cum_wts_pre / total_wt_pre))
    y_pre = np.concatenate(([0], cum_vals_pre / total_val_pre))
    
    # Post-reform: sort by values and compute cumulative distribution
    sorted_idx_post = np.argsort(values_post)
    sorted_vals_post = values_post[sorted_idx_post]
    sorted_wts_post = weights_post[sorted_idx_post]
    cum_wts_post = np.cumsum(sorted_wts_post)
    total_wt_post = cum_wts_post[-1]
    cum_vals_post = np.cumsum(sorted_vals_post * sorted_wts_post)
    total_val_post = cum_vals_post[-1]
    x_post = np.concatenate(([0], cum_wts_post / total_wt_post))
    y_post = np.concatenate(([0], cum_vals_post / total_val_post))
    
    plt.figure(figsize=(8, 6))
    plt.plot(x_pre, y_pre, label="Lorenz Curve Pre Reform")
    plt.plot(x_post, y_post, label="Lorenz Curve Post Reform")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")  # Line of perfect equality
    
    # To fill between curves, interpolate the post curve values on pre curve's x-axis
    y_post_interp = np.interp(x_pre, x_post, y_post)
    plt.fill_between(x_pre, y_pre, y_post_interp, color="skyblue", alpha=0.5)
    
    plt.xlabel("Cumulative Population Share")
    plt.ylabel("Cumulative Income Share")
    plt.title(f"{title} {gini_post - gini_pre:.4f}")
    plt.legend()
    plt.grid(True)
    plt.show()

# ---- Example usage below ----

# Assume dumpdf is your DataFrame and it contains columns:
# 'CONS_total' for total consumption,
# 'vat1' for pre-reform VAT,
# 'vat2' for post-reform VAT, and
# 'wts' for weights.

# Sort by consumption
dumpdf = dumpdf.sort_values(by=['CONS_total'])

# For Total Consumption (pre reform)
values_consumption = dumpdf['CONS_total'].dropna().values
weights_consumption = dumpdf.loc[dumpdf['CONS_total'].notna(), 'wts'].values
gini_consumption = calc_gini(values_consumption, weights_consumption)
print(f'Gini of Total Consumption Pre Reform : {gini_consumption:.2f}')

# For VAT Pre Reform
values_vat1 = dumpdf['vat1'].dropna().values
weights_vat1 = dumpdf.loc[dumpdf['vat1'].notna(), 'wts'].values
gini_vat1 = calc_gini(values_vat1, weights_vat1)
print(f'Gini of VAT Pre Reform : {gini_vat1:.2f}')
print("Kakwani Index (Pre Reform): %0.2f." % (gini_vat1 - gini_consumption))
title = 'Kakwani Index:'

# Plot weighted Lorenz curves for pre reform VAT
plot_weighted_lorenz_curve_reform(values_consumption, weights_consumption,
                                  values_vat1, weights_vat1,
                                  gini_consumption, gini_vat1, title)

# For VAT Post Reform
values_vat2 = dumpdf['vat2'].dropna().values
weights_vat2 = dumpdf.loc[dumpdf['vat2'].notna(), 'wts'].values
gini_vat2 = calc_gini(values_vat2, weights_vat2)
print(f'Gini of VAT Post Reform : {gini_vat2:.2f}')
print("Kakwani Index (Post Reform): %0.2f." % (gini_vat2 - gini_consumption))
title = 'Kakwani Index:'
# Plot Lorenz Curve
plot_lorenz_curve_reform(values_pre, values_post, gini_pre, gini_post, title)
