"""
This is a file that allows sampling of a large dataset.
"""

from stata_python import *
import pandas as pd
import numpy as np

field_names = pd.read_excel('susenas_2018_product_name_and_rate.xlsx', 'Sheet1')
vat_df0=pd.read_csv('taxcalc/merged_susenas_2018_no_sum.csv')

vat_df0 = vat_df0.rename(columns={'URUT':'id_n'})

vat_df = vat_df0.drop(['Year', 'weight', 'WEIND','CONS_total', 'WT2018'], axis = 1)
vat_long_df = pd.melt(vat_df, id_vars='id_n', var_name='KODE', value_name='CONS')
vat_long_df = pd.merge(vat_long_df, field_names[['KODE', 'Category4']], on='KODE', how='left' )
vat_merged_df = vat_long_df.groupby(['id_n', 'Category4'])[["CONS"]].sum()
vat_merged_df = vat_merged_df.reset_index()
vat_long1_df = pd.melt(vat_df, id_vars='id_n', var_name='KODE', value_name='CONS')
vat_long1_df = pd.merge(vat_long1_df, field_names[['KODE', 'Category5']], on='KODE', how='left' )
vat_merged1_df = vat_long1_df.groupby(['id_n', 'Category5'])[["CONS"]].sum()
vat_merged1_df = vat_merged1_df.reset_index()
vat_wide_df = vat_merged_df.pivot(index='id_n', columns='Category4', values='CONS')
vat_wide1_df = vat_merged1_df.pivot(index='id_n', columns='Category5', values='CONS')
vat_wide_df['CONS_total'] = vat_wide_df[vat_wide_df.columns[vat_wide_df.columns.str.startswith(('CONS'))]].sum(axis=1)
# First merge: merge vat_wide_df with vat_wide1_df
df_temp = pd.merge(vat_wide_df, vat_wide1_df, on='id_n', how='left')
# Second merge: merge the result with the weight column from vat_df0
vat_wide_df = pd.merge(df_temp, vat_df0[['id_n','weight']], on='id_n', how='left')

#vat_wide_df = pd.merge(vat_wide_df, vat_wide1_df, vat_df0[['id_n','weight']], on='id_n', how='left')
vat_wide_df['Year']=2018

sample_size = 20000
vat_sample = vat_wide_df.sample(n=sample_size, weights=vat_wide_df['weight'], replace=True)
total_households = vat_df0['weight'].sum()
factor = total_households/sample_size
vat_sample['weight'] = factor
#plot_density_chart(vat_sample, 'tot_inc', logx=True)

plot_density_chart_mult(vat_wide_df, 'Original Dataset', vat_sample, 'Sample Dataset', 'CONS_total', title=None, xlabel=None, logx=False, vline=None)

    
total_weight_sample = vat_sample['weight'].sum()
total_weight_population = vat_wide_df['weight'].sum()
#comparing the statistic of the population and sample
varlist = ['CONS_total']
for var in varlist:
    vat_sample['weighted_'+var] = vat_sample[var]*vat_sample['weight']
    sample_sum = vat_sample['weighted_'+var].sum()
    vat_wide_df['weighted_'+var] = vat_wide_df[var]*vat_wide_df['weight']
    population_sum = vat_wide_df['weighted_'+var].sum()
    
    sample_mean = sample_sum/total_weight_sample
    population_mean = population_sum/total_weight_population
    print("           Sample Mean for ", var, " = ", sample_mean)
    print("       Population Mean for ", var, " = ", population_mean)
    print("Sampling Error for Mean(%) ", var, " = ", "{:.2%}".format((population_mean-sample_mean)/population_mean))    


df_weight = vat_sample[['weight']]

df_weight.columns = ['WT2018']
df_weight['WT2019'] = df_weight['WT2018']
df_weight['WT2020'] = df_weight['WT2018']
df_weight['WT2021'] = df_weight['WT2018']
df_weight['WT2022'] = df_weight['WT2018']
df_weight['WT2023'] = df_weight['WT2018']
df_weight['WT2024'] = df_weight['WT2018']
df_weight['WT2025'] = df_weight['WT2018']
df_weight['WT2026'] = df_weight['WT2018']
df_weight['WT2027'] = df_weight['WT2018']
df_weight['WT2028'] = df_weight['WT2018']

df_weight.to_csv('taxcalc/vat_indo_sample_weights.csv')

vat_sample.to_csv('taxcalc/vat_indo_sample.csv')

# Creating weights of original dataset
df_weight = vat_wide_df[['weight']]

df_weight.columns = ['WT2018']
df_weight['WT2019'] = df_weight['WT2018']
df_weight['WT2020'] = df_weight['WT2018']
df_weight['WT2021'] = df_weight['WT2018']
df_weight['WT2022'] = df_weight['WT2018']
df_weight['WT2023'] = df_weight['WT2018']
df_weight['WT2024'] = df_weight['WT2018']
df_weight['WT2025'] = df_weight['WT2018']
df_weight['WT2026'] = df_weight['WT2018']
df_weight['WT2027'] = df_weight['WT2018']
df_weight['WT2028'] = df_weight['WT2018']

df_weight.to_csv('taxcalc/vat_indo_big_weights.csv')
vat_wide_df.to_csv('taxcalc/vat_indo_big.csv')

# Calibration to sample
#
# reweight using tax projections calibrated
tax_collection_2018_billion = 537.470392215416*1e3
# synthetic data has only 100,000 observations
tax_collection_app_billion = 173928.95

multiplicative_factor = tax_collection_2018_billion/tax_collection_app_billion

vat_sample = pd.read_csv('taxcalc/vat_indo_sample.csv')
vat_sample['weight'] = multiplicative_factor*vat_sample['weight']

df_weight = vat_sample[['weight']]

df_weight.columns = ['WT2018']
df_weight['WT2019'] = df_weight['WT2018']
df_weight['WT2020'] = df_weight['WT2018']
df_weight['WT2021'] = df_weight['WT2018']
df_weight['WT2022'] = df_weight['WT2018']
df_weight['WT2023'] = df_weight['WT2018']
df_weight['WT2024'] = df_weight['WT2018']
df_weight['WT2025'] = df_weight['WT2018']
df_weight['WT2026'] = df_weight['WT2018']
df_weight['WT2027'] = df_weight['WT2018']
df_weight['WT2028'] = df_weight['WT2018']

df_weight.to_csv('taxcalc/vat_indo_sample_weights.csv')

vat_sample.to_csv('taxcalc/vat_indo_sample.csv')

