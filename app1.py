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
vars['DEFAULTS_FILENAME'] = "current_law_policy_pit_training.json"
vars['GROWFACTORS_FILENAME'] = "growfactors_pit_training.csv" 
vars['pit_data_filename'] = "pit_data_training.csv"
vars['pit_weights_filename'] = "pit_weights_training.csv"
vars['pit_records_variables_filename'] = "records_variables_pit_training.json"
vars['pit_benchmark_filename'] = "tax_incentives_benchmark_pit_training.json"
vars['pit_elasticity_filename'] = "elasticity_pit_training.json"
vars['pit_functions_filename'] = "functions_pit_training.py"
vars['pit_function_names_filename'] = "function_names_pit_training.json"
vars['pit_distribution_json_filename'] = 'pit_distribution_training.json'

vars['vat_data_filename'] = "gst.csv"
vars['vat_weights_filename'] = "gst_weights.csv"
vars['vat_records_variables_filename'] = "gstrecords_variables.json"  

vars['cit_data_filename'] = "cit_cross.csv"
vars['cit_weights_filename'] = "cit_cross_wgts1.csv"
vars['cit_records_variables_filename'] = "corprecords_variables.json"

vars['gdp_filename'] = 'gdp_nominal_training.csv'
vars["start_year"] = 2022
vars["end_year"] = 2027
vars["SALARY_VARIABLE"] = "gross_i_w"
vars['elasticity_filename'] = "elasticity_pit_training.json"
vars['DIST_VARIABLES'] = ['weight', 'total_gross_income', 'pitax']
vars['DIST_TABLE_COLUMNS'] = ['weight', 'total_gross_income', 'pitax']        
vars['DIST_TABLE_LABELS'] = ['Returns',
                     'Gross Total Income',
                     'PITax']
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

f = open('taxcalc/'+vars['pit_distribution_json_filename'])
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
reform = Calculator.read_json_param_objects('app0_reform.json', None)
pol.implement_reform(reform['policy'])
calc2 = Calculator(policy=pol, records=recs, verbose=False)
calc2.calc_all()

# compare aggregate results from two calculators
weighted_tax1 = calc1.weighted_total_pit('pitax')
weighted_tax2 = calc2.weighted_total_pit('pitax')
total_weights = calc1.total_weight_pit()
print(f'Tax 1 {weighted_tax1 * 1e-9:,.2f}')
print(f'Tax 2 {weighted_tax2 * 1e-9:,.2f}')
print(f'Total weight {total_weights * 1e-6:,.2f}')

# dump out records
dump_vars = ['id_n', 'Year', 'income_wage_l', 'income_dividends_c',
             'income_interest_c', 'total_gross_income', 'pitax_w', 'pitax_c', 'pitax']
dumpdf = calc1.dataframe(dump_vars)
dumpdf['pitax1'] = calc1.array('pitax')
dumpdf['pitax2'] = calc2.array('pitax')
dumpdf['pitax_diff'] = dumpdf['pitax2'] - dumpdf['pitax1']
column_order = dumpdf.columns

dumpdf.to_csv('app1-dump.csv', columns=column_order,
              index=False, float_format='%.0f')
