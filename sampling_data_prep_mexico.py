"""
This is a file that allows sampling of a large dataset.
"""
import sys
sys.path.insert(0, 'C:/Users/wb305167/OneDrive - WBG/python_latest/Tax-Revenue-Analysis')
from stata_python import *
import pandas as pd
import numpy as np

pit_df=pd.read_csv('pit_mexico_big.csv')
pit_df = pit_df.rename(columns={'id_n':'id_n1'})
pit_df['id_n']=pit_df.index
pit_df['weight'] = pit_df['factor']

pit_sample = pit_df.sample(n=100000, weights=pit_df['factor'], replace=True)
pit_sample['weight'] = 1.0
#plot_density_chart(pit_sample, 'tot_inc', logx=True)

plot_density_chart_mult(pit_df, 'Original Dataset', pit_sample, 'Sample Dataset', 'tot_inc', title=None, xlabel=None, logx=True, vline=None)

    
total_weight_sample = pit_sample['weight'].sum()
total_weight_population = pit_df['weight'].sum()
#comparing the statistic of the population and sample
varlist = ['tot_inc']
for var in varlist:
    pit_sample['weighted_'+var] = pit_sample[var]*pit_sample['weight']
    sample_sum = pit_sample['weighted_'+var].sum()
    pit_df['weighted_'+var] = pit_df[var]*pit_df['weight']
    population_sum = pit_df['weighted_'+var].sum()
    
    sample_mean = sample_sum/total_weight_sample
    population_mean = population_sum/total_weight_population
    print("           Sample Mean for ", var, " = ", sample_mean)
    print("       Population Mean for ", var, " = ", population_mean)
    print("Sampling Error for Mean(%) ", var, " = ", "{:.2%}".format((population_mean-sample_mean)/population_mean))    


df_weight = pit_sample[['weight']]

df_weight.columns = ['WT2022']
df_weight['WT2023'] = df_weight['WT2022']
df_weight['WT2024'] = df_weight['WT2022']
df_weight['WT2025'] = df_weight['WT2022']
df_weight['WT2026'] = df_weight['WT2022']
df_weight['WT2027'] = df_weight['WT2022']
df_weight['WT2028'] = df_weight['WT2022']
df_weight['WT2029'] = df_weight['WT2022']
df_weight['WT2030'] = df_weight['WT2022']
df_weight['WT2031'] = df_weight['WT2022']
df_weight['WT2032'] = df_weight['WT2022']

df_weight.to_csv('taxcalc/pit_mexico_sample_weights.csv')

pit_sample.to_csv('taxcalc/pit_mexico_sample.csv')

df_weight = pit_df[['weight']]

df_weight.columns = ['WT2022']
df_weight['WT2023'] = df_weight['WT2022']
df_weight['WT2024'] = df_weight['WT2022']
df_weight['WT2025'] = df_weight['WT2022']
df_weight['WT2026'] = df_weight['WT2022']
df_weight['WT2027'] = df_weight['WT2022']
df_weight['WT2028'] = df_weight['WT2022']
df_weight['WT2029'] = df_weight['WT2022']
df_weight['WT2030'] = df_weight['WT2022']
df_weight['WT2031'] = df_weight['WT2022']
df_weight['WT2032'] = df_weight['WT2022']

df_weight.to_csv('taxcalc/pit_mexico_big_weights.csv')

# Calibration to sample
#
# reweight using tax projections calibrated
tax_collection_2022_billion = 1332.00
# synthetic data has only 100,000 observations
tax_collection_app_billion = 1.04

multiplicative_factor = tax_collection_2022_billion/tax_collection_app_billion

pit_sample['weight'] = multiplicative_factor

df_weight = pit_sample[['weight']]

df_weight.columns = ['WT2022']
df_weight['WT2023'] = df_weight['WT2022']
df_weight['WT2024'] = df_weight['WT2022']
df_weight['WT2025'] = df_weight['WT2022']
df_weight['WT2026'] = df_weight['WT2022']
df_weight['WT2027'] = df_weight['WT2022']
df_weight['WT2028'] = df_weight['WT2022']
df_weight['WT2029'] = df_weight['WT2022']
df_weight['WT2030'] = df_weight['WT2022']
df_weight['WT2031'] = df_weight['WT2022']
df_weight['WT2032'] = df_weight['WT2022']

df_weight.to_csv('taxcalc/pit_mexico_sample_weights.csv')

pit_sample.to_csv('taxcalc/pit_mexico_sample.csv')

