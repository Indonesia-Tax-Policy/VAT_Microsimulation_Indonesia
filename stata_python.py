# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 18:51:40 2020

@author: wb305167
"""

# insert into the file
#import sys
#sys.path.insert(0, 'C:/Users/wb305167/OneDrive - WBG/python_latest/Tax-Revenue-Analysis')
#from stata_python import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def castToList(x): #casts x to a list
    if isinstance(x, list):
        return x
    elif isinstance(x, str):
        return [x]
    try:
        return list(x)
    except TypeError:
        return [x]
    
# Creates a new dataframe with a list named data and with the field name
# field_name. the rows of the field field_name will be populated by the values
# in the list named data
# usage 
# df = create_dataframe(Country_Codes, 'Country_Code')
#
def create_dataframe(data, field_name):
    df = pd.DataFrame(data, columns = [field_name])   
    return(df)

def weighted_mean(df,field_name,weight_col,by_col):
    if type(field_name) is str:
        field_name = [field_name]       
    for col in field_name:
        df[col+'_data_times_weight'] = df[col]*df[weight_col]
        df[col+'_weight_where_notnull'] = df[weight_col]*pd.notnull(df[col])
    g = df.groupby(by_col)
    result = pd.DataFrame()
    for col in field_name:
        result[col] = g[col+'_data_times_weight'].sum() / g[col+'_weight_where_notnull'].sum()
        del df[col+'_data_times_weight'], df[col+'_weight_where_notnull']
    return result

def weighted_total(df,field_name,weight_col,by_col=None):
    if type(field_name) is str:
        field_name = [field_name]       
    for col in field_name:
        df[col+'_data_times_weight'] = df[col]*df[weight_col]
        df[col+'_weight_where_notnull'] = df[weight_col]*pd.notnull(df[col])
    #result = pd.DataFrame()
    # for col in field_name:
    #     result[col] = df[col+'_data_times_weight'].sum() 
    #     del df[col+'_data_times_weight'], df[col+'_weight_where_notnull']
    return df[col+'_data_times_weight'].sum()

# Function similar to egen in STATA
# usage egen(df, , 'mean', 'rev', 'Region_Code', 'avg_rev')
# df = egen(df, , 'mean', 'GGR_NGDP', ['Region_Code', 'year'],'mean_GGR_NGDP')
# for grouping by a combination of fields use list notation ['Region_Code, 'year'] 
# if we want the mean satisfying a certain condition, we use the 
# field name value, field value and field condition
# example df = egen(df, 'mean',  'rev', 'Region_Code', 'avg_rev', 'year', '<', 2019)
# calculates the mean only satisfying the condition year<2019

# value_of is to place a particular record value in each record satisfying the condition
# in the example below we take the value of 'rev' in year 2020 and fill in 
# the 'rev' for all the 'year' of the 'Country_Code' for further analysis
# df = egen(df, 'value_of', 'rev', 'Country_Code', 'rev_2020',  'year', 2020)
# df = egen(df, 'value_of', 'GGR_NGDP', 'Country_Code', 'GGR_NGDP_2020', 'year', 2020)
def egen(df, func, field_name, by, new_field_name=None, field_name_value=None, field_condition=None, field_value=None, weight_col=None):
    def dataframe_partition(df, field_name_value=None, field_condition=None, field_value=None):
        import operator
        ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq,
           '!=': operator.ne}
        return df[ops[field_condition](df[field_name_value], field_value)]      
    
    if func=='value_of':
        if (field_name_value is None or field_value is None):
            print('error')
        else:
            if by is not None:
                df2=df[df[field_name_value]==field_value][[by, field_name]]
            else:
                df2=df[df[field_name_value]==field_value][[field_name]]
    elif func=='mean':
        if field_condition is not None:
            df1=dataframe_partition(df, field_name_value, field_condition, field_value)
        else:
            df1 = df
        if by is not None:
            df2 = df1.groupby(by=by)[field_name].mean()
            df2 = df2.reset_index()
        else:
            df2 = pd.DataFrame([castToList(df1[field_name].mean(axis=0))], columns = castToList(field_name),
                   index = list(df1.index))
    elif func=='weighted_mean':
        if field_condition is not None:
            df1=dataframe_partition(df, field_name_value, field_condition, field_value)
        else:
            df1 = df
        if by is not None:
            if weight_col is not None:
                df2 = weighted_mean(df1,field_name,weight_col, by)
                df2 = df2.reset_index()
            else:
                df2 = df1.groupby(by=by)[field_name].mean()
                df2 = df2.reset_index()
                print('weight is not given so performing simple mean')
        else:
            df2 = pd.DataFrame([castToList(df1[field_name].mean(axis=0))], columns = castToList(field_name),
                   index = list(df1.index))    
    elif func=='sum':
        if field_condition is not None:
            df1=dataframe_partition(df, field_name_value, field_condition, field_value)
        else:
            df1 = df
        if by is not None:            
            df2 = df1.groupby(by=by)[field_name].sum()
            df2 = df2.reset_index()
        else:
            df2 = pd.DataFrame([castToList(df1[field_name].sum(axis=0))], columns = castToList(field_name),
                   index = df1.index)           
    elif func=='min':
        if field_condition is not None:
            df1=dataframe_partition(df, field_name_value, field_condition, field_value)
        else:
            df1 = df
        if by is not None:        
            df2 = df1.groupby(by=by)[field_name].min()
            df2 = df2.reset_index()
        else:
            df2 = pd.DataFrame([castToList(df1[field_name].min(axis=0))], columns = castToList(field_name),
                   index = df1.index)             
    elif func=='max':
        if field_condition is not None:
            df1=dataframe_partition(df, field_name_value, field_condition, field_value)
        else:
            df1 = df
        if by is not None: 
            df2 = df1.groupby(by=by)[field_name].max()
            df2 = df2.reset_index()
        else:
            df2 = pd.DataFrame([castToList(df1[field_name].max(axis=0))], columns = castToList(field_name),
                   index = df1.index)             
    elif func=='std':
        if field_condition is not None:
            df1=dataframe_partition(df, field_name_value, field_condition, field_value)
        else:
            df1 = df
        if by is not None: 
            df2 = df1.groupby(by=by)[field_name].std()
            df2 = df2.reset_index()
        else:
            df2 = pd.DataFrame([castToList(df1[field_name].std(axis=0))], columns = castToList(field_name),
                   index = df1.index) 
    elif func=='count':
        if field_condition is not None:
            df1=dataframe_partition(df, field_name_value, field_condition, field_value)
        else:
            df1 = df
        if by is not None:            
            df2 = df1.groupby(by=by)[field_name].count()
            df2 = df2.astype(int)
            df2 = df2.reset_index()
            #print(df2)
        else:
            df2 = pd.DataFrame([castToList(df1[field_name].count())], columns = castToList(field_name),
                   index = df1.index)
            df2 = df2.astype(int)
    if new_field_name is not None:
        if type(field_name) is str:
            if type(new_field_name) is str:
                df2=df2.rename(columns={field_name:new_field_name})
            else:
                df2=df2.rename(columns={field_name:func.capitalize()+' '+ field_name})
                #print("error: New field name is list while original is string")
        else:
            if len(new_field_name)==len(field_name):
                for i in range(len(field_name)):
                    df2=df2.rename(columns={field_name[i]:new_field_name[i]})
            else:               
                for i in range(len(field_name)):
                    df2=df2.rename(columns={field_name[i]:func.capitalize()+' '+ field_name[i]})            
    else:
        if type(field_name) is str:
            df2=df2.rename(columns={field_name:func.capitalize()+' '+ field_name})
        else:               
            for i in range(len(field_name)):
                df2=df2.rename(columns={field_name[i]:func.capitalize()+' '+ field_name[i]})
    #print('df before \n ', df)
    if by is not None:
        df = pd.merge(df, df2, on=by, how='inner')
    else:
        df = pd.concat([df, df2], axis=1, sort=False)

    #print('df after \n ', df)
    #print('df2 \n', df2)
    #print('\n')
    return(df)

# Function uses egen first and then tabulates it
# usage 
# df = tabulate(df, 'mean', 'rev', 'Region_Code')
# df = tabulate(df, 'mean', 'GGR_NGDP', ['Region_Code', 'year'])
# field name can be a list ['rev', 'tax revenue']
# for grouping by a combination of fields use list notation ['Region_Code, 'year'] 
# if we want the mean satisfying a certain condition, we use the 
# field name value, field value and field condition
# example df = tabulate(df, 'mean', 'rev', 'Region_Code', 'year', '<', 2019)
# tabulates the mean only satisfying the condition year<2019
# title is helpful when using giving more meaning to the column,
# df = tabulate(df, 'mean', 'rev', 'Region_Code', title='Region') 
# column would look like 'Mean rev Region'
def tabulate(df, func, field_name, by=None, field_name_value=None, field_condition=None, field_value=None, title=None, weight_col=None):
    def get_title():
        if title is None:
            return ''
        else:
            return ' '+title
    new_field_name = []
    if type(field_name) is str:
        new_field_name = new_field_name+ [func.capitalize()+' '+ field_name]
    else:
        for i in range(len(field_name)):
            new_field_name = new_field_name+ [func.capitalize()+' '+ 
                                              field_name[i]]
    df1 = egen(df, func, field_name, by, new_field_name, field_name_value, field_condition, field_value, weight_col=weight_col)    
    #print('df1 after \n ', df1)
    #print('df1 columns \n ', df1.columns)
    if by is not None:
        df1 = df1.groupby(by)[new_field_name].mean()
        #print('df1 after grouping \n ', df1)        
        # Now attach the overall mean or sum etc
        df2 = egen(df, func, field_name, by=None, new_field_name=None, field_name_value=None, field_condition=None, field_value=None, weight_col=weight_col) 
        #print('df2 after \n ', df2)
        df3 = pd.DataFrame([castToList(df2[new_field_name].mean(axis=0))], columns = castToList(new_field_name),
                           index = list(df2.index)).iloc[:1]
        df3 = df3.rename(index={df3.index[0]: 'OVERALL '+func.upper()})        
        df1 = pd.concat([df1, df3], axis=0, sort=False)    
    else:
        df2 = egen(df, func, field_name, by=None, new_field_name=None, field_name_value=None, field_condition=None, field_value=None, weight_col=weight_col) 
        #print('df2 after \n ', df2)
        df3 = pd.DataFrame([castToList(df2[new_field_name].mean(axis=0))], columns = castToList(new_field_name),
                           index = list(df2.index)).iloc[:1]
        df1 = df3.rename(index={df3.index[0]: 'OVERALL '+func.upper()})
    if func=='count':
        df1 = df1.astype(int)
    
    if title is not None:
        new_field_name = [i + ' '+title for i in new_field_name]
        df1.columns = new_field_name
    #print(new_field_name)
    #df1.columns = new_field_name
    #df1 = df1.set_index()   
    #df1 = df1[field_name].mean(axis=0)
    #df1 = pd.concat([df1, pd.DataFrame([[np.nan] * df1.shape[1]], columns=df1.columns)], ignore_index=True)
    #df1 = egen(df, func, field_name,  by, new_field_name, field_name_value, field_condition, field_value)    
    df1 = df1.reset_index()
    df1 = df1.rename(columns={'index':by})
    return(df1)


# Creates a new field with the default values if provided else 
# blanks will be filled
# usage 
# df = gen(df, 'Revenue Shock')
# df = gen(df, 'Revenue Shock', 1.0)
#
def gen(df, field_name, data=None, default_value=None):
    if field_name in df.columns.values:
        print('Field : ', field_name, ' already exists')
    else:
        if (default_value is None) and (data is None):        
            field_name_values = ['']*len(df)
        elif (default_value is not None) and (data is None):       
            field_name_values = [default_value]*len(df)
        elif (default_value is None) and (data is not None):
            field_name_values = data
        df[field_name] = field_name_values
    return(df)

# replaces the values of the column replace_field_name with replace_value
# in those rows whereever the condition condition_field_name == condition_field_name_value
# is satisfied
# usage 
# df = replace(df, 'Total_Non_Tax_Revenue', 1.0, 'Country_Code', 'ASM')
# df = replace(df, 'Tax_Revenue_incl_SC', 'Tax_Revenue', 'Country_Code', 'ASM')

def replace(df, replace_field_name, replace_value, condition_field_name,
            condition_field_name_value):
    if replace_value in df.columns:        
        df[replace_field_name] = np.where(df[condition_field_name]==condition_field_name_value, df[replace_value], df[replace_field_name])        
    else:
        df[replace_field_name] = np.where(df[condition_field_name]==condition_field_name_value, replace_value, df[replace_field_name])      
    return(df)

# returns a list of records from a dataframe satisfying certain conditions
# up to three conditions could be used to select
# usage
# list_if(revenue_df, ['year', 'govt_expenditure', 'Total_Revenue_excl_SC'], 'Country_Code', '=', 'IND', 'year', '>=', 2000)
#
def list_if(df, field_name,
            condition_field_name1=None, condition_operator1=None, condition_field_value1=None,
            condition_field_name2=None, condition_operator2=None, condition_field_value2=None,
            condition_field_name3=None, condition_operator3=None, condition_field_value3=None):

    condition_field_name_list = []
    condition_operator_list = []
    condition_field_value_list = []
    if ((condition_field_name1 is not None) and
        (condition_field_name2 is not None) and
        (condition_field_name3 is not None)):
            condition_field_name_list = [condition_field_name1,
                                         condition_field_name2,
                                         condition_field_name3]
            condition_operator_list = [condition_operator1,
                                       condition_operator2,
                                       condition_operator3]
            condition_field_value_list = [condition_field_value1,
                                          condition_field_value2,
                                          condition_field_value3]
    elif ((condition_field_name1 is not None) and
          (condition_field_name2 is not None)):
            condition_field_name_list = [condition_field_name1,
                                         condition_field_name2]
            condition_operator_list = [condition_operator1,
                                       condition_operator2]
            condition_field_value_list = [condition_field_value1,
                                          condition_field_value2]
    elif (condition_field_name1 is not None):
            condition_field_name_list = [condition_field_name1]
            condition_operator_list = [condition_operator1]      
            condition_field_value_list = [condition_field_value1]            
    #print('field_name: ', field_name)
    #print(condition_field_name_list)
    #print(condition_field_value_list)
    length_condition = len(condition_field_name_list)
    if (length_condition==0):
        return(df[field_name])
    else:
        for i in range(length_condition):
            print(condition_field_name_list[i])
            print(condition_field_value_list[i])
            if (condition_operator_list[i]=='='):
                df = df[df[condition_field_name_list[i]]==condition_field_value_list[i]]
            elif (condition_operator_list[i]=='>'):
                df = df[df[condition_field_name_list[i]]>condition_field_value_list[i]]
            elif (condition_operator_list[i]=='>='):
                df = df[df[condition_field_name_list[i]]>=condition_field_value_list[i]]
            elif (condition_operator_list[i]=='<'):
                df = df[df[condition_field_name_list[i]]<condition_field_value_list[i]]
            elif (condition_operator_list[i]=='<='):
                df = df[df[condition_field_name_list[i]]<=condition_field_value_list[i]]               
    #print(df)
    return (df[field_name])


def remove_outliers_value(df, field_name, lower=None, upper=None):
    if lower is not None:
        df = df[df[field_name]>=lower]
        
    if upper is not None:
        df = df[df[field_name]<=upper]
    
    return(df)

# usage
# if both values are given then the values as lower and upper
# if one value is given then lower and upper are removed to the extent of the value
# i.e. if one is given then 1 percentile and top 1 percentile are removed
# default is one percentile removed from top and bottom
# remove_outliers_centile(df, 'ROI', 1, 99)
# removes values below 1 percentile and above 99 percentile
# remove_outliers_centile(df, 'ROI', 5)
# removes values below 5 percentile and above 95 percentile
# remove_outliers_centile(df, 'ROI')
# removes values below 1 percentile and above 99 percentile
# If a list of fields are sent it removes the min of all the field values
# and max of all the field values
def remove_outliers_centile(df, field_name, lower=None, upper=None):
    def keep_df(df, field_name, field_condition, field_value):
        import operator
        ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq,
           '!=': operator.ne}
        for i in range(len(field_name)):
            df = df[(ops[field_condition](df[field_name[i]], field_value)) | (df[field_name[i]].isnull())]
        return df
            
    print('Centiles are:\n', df[field_name].quantile([0.01, .1, .2, .3, .4, .5, .6, .7, .8, .9, 0.99]))
    field_name = castToList(field_name)
    df_old = df
    if lower is not None:
        centile_value1 = min(df[field_name].quantile(lower/100).tolist())
        df = keep_df(df, field_name, '>', centile_value1)
        print('Removed the values below ' , centile_value1, ' for ', field_name[0])
        print(df_old[df_old[field_name[0]]<centile_value1])
    if upper is not None:
        centile_value2 = max(df[field_name].quantile(upper/100).tolist())
        df = keep_df(df, field_name, '<', centile_value2)
        print('Removed the values above ', centile_value2, ' for ', field_name[0])
        print(df_old[df_old[field_name[0]]>centile_value2])
    if lower is None and upper is None:
        centile_value1 = min(df[field_name].quantile(lower/100).tolist())
        centile_value2 = max(df[field_name].quantile(upper/100).tolist())
        df = keep_df(df, field_name, '>', centile_value1)
        df = keep_df(df, field_name, '<', centile_value2)
        print('Removed the values below ', centile_value1, ' for ', field_name[0])
        print(df_old[df_old[field_name[0]]<centile_value1])
        print('Removed the values above ', centile_value2, ' for ', field_name[0])
        print(df_old[df_old[field_name[0]]>centile_value2])
         
    return(df)

# unlike the pandas merge, this merge updates the common named fields (EXCEPT THE 
# FIELDS ON WHICH MERGED - see function stata_merge_update_field) from the 
# secondary dataframe to the master dataframe (when overwrite is set to True)
# or where the master dataframe is NaN (when overwrite_if_null is set to True) 
# and includes all the rows from both the secondary and master dataframe 
# when merge_type is set to "outer" , similarly "left" or "right" or "inner" 
# merge with DEFAULT being "outer" merge
# usage 
# df = stata_merge_update_all_fields_full(df1, df2, 'year', 'Country_Code', merge_type="outer",
#                  overwrite=True, indicator=True)
def stata_merge_update_all_fields_full(df1, df2, field1, field2=None, 
                                       merge_type=None, overwrite=None, overwrite_if_null=None,
                                       indicator=None):
    merge_fields = [field1]
    if field2 is not None:
        merge_fields = merge_fields + [field2]
    df1_columns = df1.columns
    df2_columns = df2.columns
    common_fields = list(set(df1_columns) & set(df2_columns))
    common_fields = [x for x in common_fields if x not in merge_fields]
    if merge_type is not None:
        #if ((merge_type=="left") or (merge_type=="right") or (merge_type=="inner")):
        df = pd.merge(df1, df2, how=merge_type, on=merge_fields, indicator=True)
    else:
        df = pd.merge(df1, df2, how="outer", on=merge_fields, indicator=True)
    common_fields_x = [x+'_x' for x in common_fields]
    common_fields_y = [x+'_y' for x in common_fields]  
    for i in range(len(common_fields_x)):
        if (overwrite_if_null is not None) and overwrite_if_null:
            df[common_fields_x[i]] = np.where(df[common_fields_x[i]].isnull(), df[common_fields_y[i]], df[common_fields_x[i]])          
        if (overwrite is not None) and overwrite:
            #overwrite only when the replacement is not null
            df[common_fields_x[i]] = np.where(df[common_fields_y[i]].notnull(), df[common_fields_y[i]], df[common_fields_x[i]]) 

    df.rename(columns=dict(zip(common_fields_x, common_fields)),inplace=True)
    if indicator is None:
        df = df.drop(['_merge'], axis=1, errors='ignore')
    else:
        if not indicator:
            df = df.drop(['_merge'], axis=1, errors='ignore')
    all_fields = list(df.columns)
    new_fields = [x for x in all_fields if x not in common_fields_y]
    df = df[new_fields]
    return(df)

# unlike the pandas merge, this merge updates the specified fields from the 
# secondary dataframe to the master dataframe
# usage 
# df2 =  stata_merge_update_field(df, country_map, 'Country', 
#                             update_master_field='Country',
#                             update_secondary_field='WB_Country',
#                             indicator=True)
def stata_merge_update_field(df1, df2, field1, field2=None, 
                             update_master_field=None,
                             update_secondary_field=None,
                             indicator=None):
    merge_fields = [field1]
    if field2 is not None:
        merge_fields = merge_fields + [field2]
    df1_columns = df1.columns
    df1 = df1.drop(['_merge'], axis=1, errors='ignore')
    df2_columns = df2.columns
    df2 = df2.drop(['_merge'], axis=1, errors='ignore')
    common_fields = list(set(df1_columns) & set(df2_columns))
    common_fields = [x for x in common_fields if x not in merge_fields]
    #print(common_fields)

    df = pd.merge(df1, df2, how="left", on=merge_fields, indicator=True)
    # if update_master_field or update_secondary_field is common in both dataframes
    # then merge will append an _x and _y respectively
    # so to check that
    if update_master_field in common_fields:
        update_master_field = update_master_field+'_x'    
    if update_secondary_field in common_fields:
        update_secondary_field = update_secondary_field+'_y'
    
    df[update_master_field] = np.where(df['_merge']=="both", df[update_secondary_field], df[update_master_field])
    
    if update_master_field in common_fields:
        df = df.rename(columns={update_master_field:update_master_field[:-2]})
    if indicator is None:
        df = df.drop(['_merge'], axis=1, errors='ignore')
    else:
        if not indicator:
            df = df.drop(['_merge'], axis=1, errors='ignore')
    return(df)

# unlike the pandas merge, this merge updates the common fields from the 
# secondary dataframe to the master dataframe
# the ultra merge also incorporates all records of both dataframes
# kinds of merge
# usage 
# df = stata_merge(df1, df2, 'year', 'Country_Code')
def stata_merge(df1, df2, field1, field2=None, indicator=None):
    merge_fields = [field1]
    if field2 is not None:
        merge_fields = merge_fields + [field2]
    df1_columns = df1.columns
    df2_columns = df2.columns
    common_fields = list(set(df1_columns) & set(df2_columns))
    common_fields = [x for x in common_fields if x not in merge_fields]
    df = pd.merge(df1, df2, how="outer", on=merge_fields, indicator=True)
    common_fields_x = [x+'_x' for x in common_fields]
    common_fields_y = [x+'_y' for x in common_fields]
    
    for i in range(len(common_fields_x)):
        df[common_fields_x[i]] = np.where(df['_merge']=="both", df[common_fields_y[i]], df[common_fields_x[i]])   
    
    df.rename(columns=dict(zip(common_fields_x, common_fields)),inplace=True)
    if indicator is None:
        if not indicator:
            common_fields_y = common_fields_y + ['_merge']
    all_fields = list(df.columns)
    new_fields = [x for x in all_fields if x not in common_fields_y]
    df = df[new_fields]
    return(df)

# visually lookup a file, if no filename is provided it will be called temp.csv
# alternatively a filename can be provided
def browse(df, filename=None):
    if filename is None:
        if isinstance(df, pd.DataFrame) or isinstance(df, pd.Series):
            df.to_csv('temp.csv')
        elif isinstance(df, np.ndarray):
            pd.DataFrame(df).to_csv('temp.csv')
        else:
            print('can browse dataframe or arrays')
            return
        import os
        os.startfile('temp.csv')
    else:
        if isinstance(df, pd.DataFrame):        
            df.to_csv(filename)
        elif isinstance(df, np.ndarray):
            pd.DataFrame(df).to_csv(filename)
        else:
            print('can browse dataframe or arrays')
            return            
        import os
        os.startfile(filename)      

#converts a wide WDI file to a long dataframe and also stores in csv format
#usage:
#filename = "GDP - Constant 2010 USD - March 2021.xls"
#parameter = 'GDP_constant_USD'
#df_gdp_constant_usd = convert_WDI_file(filename, parameter)
def convert_WDI_file(filename, parameter):
    
    df = pd.read_excel(filename, sheet_name='Data', skiprows=[0,1,2])
    #df = pd.read_excel(filename, sheet_name=sheetname, index_col=None, header=0)
    df = df.rename(columns={'Country Code':'Country_Code'})
    df.drop(['Country Name', 'Indicator Name', 'Indicator Code'], axis=1, inplace=True)
    
    df = df.set_index('Country_Code')
    df = df.stack(dropna=False)
    df = df.reset_index()
    df = df.rename(columns={'level_1':'year',0:parameter})
    df['year'] = df['year'].astype(int)
    if (filename.find('.xlsx') != -1):
        filename.replace('.xlsx', '')
    elif (filename.find('.xls') != -1):
        filename = filename.replace('.xls', '')
    else:
        filename.replace('.', '')
   
    df.to_csv(filename+'.csv', index=False)

    return(df)

#converts a wide file to a long dataframe
#retain only the category column (index_col) and years columns
#parameter is the new name of the column
#Usage - df_gsdp = convert_file_long(df, 'State', 'GSDP')
#also you can use the more versatile
# pd.wide_to_long(df_pop, stubnames='Population', i='State', j='year')
def convert_file_long(df, index_col, parameter):   
    df = df.set_index(index_col)
    df = df.stack()
    df = df.reset_index()
    df = df.rename(columns={'level_1':'year',0:parameter})
    df = df.set_index('year')
    return(df)

def centiles(df, ranking_col, centile_length):
    df = df[[ranking_col]]
    df['centile'] = pd.qcut(df[ranking_col], centile_length, labels=False)
    df.groupby(by=['centile']).sum()
    return df

def plot_density_chart(df, variable, category_var=None, title=None, xlabel=None, logx=None, vline=None, 
                       save_figure_name=None):
    '''
    Density Plot with option for logs of x axis and categories

    '''
    df1 = df.copy(deep=True)
    if logx is None:
        display_variable = 'disp_'+variable
        df1.loc[:,display_variable] = df1[variable]
        df1_sns = df1[[display_variable]]
        if vline is not None:
            adj_vline = vline            
    else:
        min_val1 = df1[variable].min()
        if (min_val1<0):
            raise ValueError("Cannot Calculate Logs of Negative Values")
        elif np.isclose(df1[variable],np.zeros(len(df1)), atol=0.0001).any():
            print("some values are close to zero so +1 is added")
            # add 1 so that any zero values are adjusted to 1           
            df1[variable] += 1
        display_variable = 'ln_'+variable
        df1.loc[:,display_variable] = np.log(df1[variable])
        df1_sns = df1[[display_variable]]
        if vline is not None:
            if (vline>0):
                adj_vline = np.log(vline)
            else:
                vline = None        
    if category_var is not None:
        df1_sns.loc[:, category_var] = df[category_var]
    sns.displot(df1_sns, kind='kde', x=display_variable, hue=category_var)
    if vline is not None:
        plt.axvline(adj_vline, color='b')
    if title is None:
        title = "Density Plot"
    plt.title(title)
    if xlabel is None:
        plt.xlabel(variable)
    else:
        plt.xlabel(xlabel)
    plt.ylabel('Density')
    plt.show()
    if save_figure_name is not None:
        plt.savefig(save_figure_name, bbox_inches="tight")

        
def plot_density_chart_mult(df1, df1_desc, df2, df2_desc, variable, title=None, xlabel=None, logx=None, vline=None):
    '''
    Plots a Kernel Density Function from multiple file inputs
    
    It is useful to compare distributions
    
    Parameters
    ----------
    df1 : Dataframe
    df1_desc : String
        DESCRIPTION. Label characterising df1 to show in the Chart
    df2 : Dataframe
    df2_desc : String
        DESCRIPTION. Label characterising df2 to show in the Chart
    variable : String
        Common variable of df1 and df1 on which the density plot is to be constructed
    title : String, optional
        DESCRIPTION. Title of the Chart. The default is None.
    xlabel : String, optional
        DESCRIPTION. X-axis title. The default is None.
    logx : String, optional
        DESCRIPTION. "Yes" if you want the X-axis in logs. The default is None.
    vline : Float, optional
        DESCRIPTION. Position in X-axis of vertical line. The default is None.

    Returns
    -------
    None.

    '''
    df1 = df1.copy(deep=True)
    df2 = df2.copy(deep=True)  
    if logx is None:
        display_variable = 'disp_'+variable
        df1.loc[:,display_variable] = df1[variable]
        df2.loc[:,display_variable] = df2[variable]
        df1_sns = df1[[display_variable]]
        df2_sns = df2[[display_variable]]
        if vline is not None:
            adj_vline = vline            
    else:
        min_val1 = df1[variable].min()
        if (min_val1<0):
            raise ValueError("Cannot Calculate Logs of Negative Values")
        elif np.isclose(df1[variable],np.zeros(len(df1)), atol=0.0001).any():
            # add 1 so that any zero values are adjusted to 1           
            df1[variable] += 1
        min_val2 = df2[variable].min()
        if (min_val2<0):
            raise ValueError("Cannot Calculate Logs of Negative Values")
        elif np.isclose(df2[variable],np.zeros(len(df2)), atol=0.0001).any():
            # add 1 so that any zero values are adjusted to 1           
            df2[variable] += 1
        display_variable = 'ln_'+variable
        df1.loc[:,display_variable] = np.log(df1[variable])
        df2.loc[:,display_variable] = np.log(df2[variable])
        df1_sns = df1[[display_variable]]
        df2_sns = df2[[display_variable]]
        if vline is not None:
            if (vline>0):
                adj_vline = np.log(vline)
            else:
                vline = None
        
    df1_sns.loc[:, 'source'] = df1_desc    
    df2_sns.loc[:, 'source'] = df2_desc
    df = pd.concat([df1_sns, df2_sns], axis=0) 
    sns.displot(df, kind='kde', x=display_variable, hue="source")
    if vline is not None:
        plt.axvline(adj_vline, color='b')
    if title is None:
        title = "Density Plot"
    plt.title(title)
    if xlabel is None:
        plt.xlabel(variable)
    else:
        plt.xlabel(xlabel)
    plt.ylabel('Density')
    plt.show()

def my_qcut(df, ranking_col, centile_length):
    len_df = len(df)
    df = df.sort_values(ranking_col)
    df = df.reset_index()
    df = df.reset_index()
    df = df.rename(columns={'level_0':'row_num'})
    df.drop(['index'], axis=1, inplace=True)
    bin_list=[]   
    row_bin = list((np.linspace(0, len_df, centile_length+1)))
    row_bin = [int(x) for x in row_bin]
    row_bin[-1] = len_df
    df['centile']=-1
    #print(row_bin)
    #print(len(row_bin))
    for i in range(len(row_bin)-1):
        #print(i, row_bin[i])
        bin_list = bin_list + [df.loc[row_bin[i], ranking_col]]
        df['centile'] = np.where(((df['row_num']>=row_bin[i])&
                                  (df['row_num']<row_bin[i+1])),i,df['centile'])
    bin_list = bin_list + [df.loc[row_bin[len(row_bin)-1]-1, ranking_col]]
    return df, bin_list, row_bin


def my_qcut_equal_length(df, ranking_col, centile_length):
    len_df = len(df)
    df = df.sort_values(ranking_col)
    df = df.reset_index()
    df = df.reset_index()
    df = df.rename(columns={'level_0':'row_num'})
    df.drop(['index'], axis=1, inplace=True, errors='ignore')
    min_val = df[ranking_col].iloc[0]
    max_val = df[ranking_col].iloc[-1:]
    bin_list=[]
    row_bin = list(np.linspace(0, max_val-min_val, centile_length+1))
    #row_bin = [int(x) for x in row_bin]
    #row_bin[-1] = len_df
    df['centile']=-1
    df_count = pd.DataFrame(-1, index=np.arange(centile_length), columns=['centile_count']) 

    #print(row_bin)
    #print(len(row_bin))
    df['centile'] = np.where(df[ranking_col]==min_val,0,df['centile'])
    for i in range(len(row_bin)-1):
        #print(i, row_bin[i])
        df['centile_pos'] = np.where(((df[ranking_col]>row_bin[i][0])&
                                  (df[ranking_col]<=row_bin[i+1][0])),i+1,df['centile'])

        df_count.loc[i, 'centile_count'] = len(df[(df[ranking_col]>row_bin[i][0])&
                                              (df[ranking_col]<=row_bin[i+1][0])])
        df_count.loc[i, 'centile'] = row_bin[i+1][0]
    #df.loc[df.index[-1], 'centile'] = centile_length
    return df, df_count

def my_qcut_weight(df, ranking_col, centile_length, weight=None):
    if weight is None:
        df['weight'] = 1
        weight='weight'
    df = df[df[weight] >0 ]
    df = df[df[ranking_col] >0 ]
    len_df = len(df)
    df = df.sort_values(ranking_col)
    df = df.reset_index()
    df = df.reset_index()
    df = df.rename(columns={'level_0':'row_num'})
    df.drop(['index'], axis=1, inplace=True)    
    df['rec_pos'] = df[weight].cumsum()
    bin_size = int(df[weight].sum()/centile_length)
    df = df.reset_index()
    df.drop(['index'], axis=1, inplace=True)
    bin_list=[]
    row_bin=[0]
    df['centile']=9
    for i in range(centile_length):
        row_bin=row_bin+[df.index[df['rec_pos']<=bin_size*(i+1)].max()]
        #print('row_bin: ', row_bin)
        #print(i)
        #print(df.loc[row_bin[i+1], ranking_col])
        bin_list = bin_list + [df.loc[row_bin[i+1], ranking_col]]
        df['centile'] = np.where((df['row_num']<row_bin[i+1])&(df['row_num']>=row_bin[i]),i,df['centile'])
    return df, bin_list, row_bin

# Centile Summary puts the centile as an index    
def centile_summary(df, ranking_col, summary_col, centile_field, centile_length, weight=None):
    df, bin_list, row_bin = my_qcut_weight(df, ranking_col, centile_length, weight)
    #df = df.rank(method='first')
    #result, bins = pd.qcut(df1[summary_col], centile_length, labels=False, retbins=True)
    #df, bins = my_qcut(df, summary_col, centile_length)
    # df0 = df[[ranking_col, 'centile']]
    # df0 = df0.groupby(by=['centile']).mean()
    # df0 = df0.rename(columns={ranking_col:'mean_'+ranking_col})
    df1 = df[[summary_col, centile_field]]
    df2 = df1.groupby(by=[centile_field]).sum()
    df2 = df2.rename(columns={summary_col:'sum_'+summary_col}) 
    df3 = df1.groupby(by=[centile_field]).count()
    df3 = df3.rename(columns={summary_col:'count_'+summary_col})
    df4 = df1.groupby(by=[centile_field]).mean()
    df4 = df4.rename(columns={summary_col:'mean_'+summary_col})
    df5 = df1.groupby(by=[centile_field]).median()
    df5 = df5.rename(columns={summary_col:'median_'+summary_col})    
    df6 = pd.concat([df2, df3, df4, df5], axis=1)
    #print('df6', df6)
    return (df6)

# Centile Summary1 puts the centile as a column   
def centile_summary1(df, ranking_col, summary_col, centile_field, centile_length, weight=None):
    df, bin_list, row_bin = my_qcut_weight(df, ranking_col, centile_length, weight)
    #df = df.rank(method='first')
    #result, bins = pd.qcut(df1[summary_col], centile_length, labels=False, retbins=True)
    #df, bins = my_qcut(df, summary_col, centile_length)
    # df0 = df[[ranking_col, 'centile']]
    # df0 = df0.groupby(by=['centile']).mean()
    # df0 = df0.rename(columns={ranking_col:'mean_'+ranking_col})
    df1 = df[[summary_col, centile_field]]
    df2 = df1.groupby(by=[centile_field]).sum().reset_index()
    df2 = df2.rename(columns={summary_col:'sum_'+summary_col}) 
    df3 = df1.groupby(by=[centile_field]).count().reset_index()
    df3 = df3.rename(columns={summary_col:'count_'+summary_col})
    df4 = df1.groupby(by=[centile_field]).mean().reset_index()
    df4 = df4.rename(columns={summary_col:'mean_'+summary_col})
    df5 = df1.groupby(by=[centile_field]).median().reset_index()
    df5 = df5.rename(columns={summary_col:'median_'+summary_col})    
    df6 = pd.concat([df2, df3[['count_'+summary_col]], df4[['mean_'+summary_col]], df5[['median_'+summary_col]]], axis=1)
    #print('df6', df6)
    return (df6)

def multi_merge(df, file_list, merge_field_list):
    for df1 in file_list:
        df = pd.merge(df, df1, how='left', on=merge_field_list)
    return(df)

def regress(df1, field_list):
    import statsmodels.api as sm
    df = df1[field_list] 
    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(axis=1)]

    X_vars = df[field_list[1:]] ## X_vars usually means our input variables (or independent variables)
    Y_vars = df[field_list[0]] ## Y_vars usually means our output/dependent variable
    X1 = sm.add_constant(X_vars) ## let's add an intercept (beta_0) to our model
    Y1 = Y_vars
    model = sm.OLS(Y1, X1).fit()
    print(model.summary())      
    return(model)

def survey_means(df, param, field_name, weight):
    df1 = df
    if param=='mean':
        sum_weight = df1[weight].sum()
        df1['wtd_'+param] = df1[field_name]*df1[weight]/sum_weight
        ret_val = df1['wtd_'+param].sum()
    
    return(ret_val)
        
def summary(df, field_name):
    # Count unique values
    value_counts = df[field_name].value_counts().reset_index()
   
    return(value_counts)        

def calc_gini(values): 
    n = len(values)
    cumulative_income = values.sum()
    gini_index = ((2 * np.sum((np.arange(1, n + 1) * values))) /
                  (n * cumulative_income)) - ((n + 1) / n)
    print(gini_index)
    return gini_index

# Send the income as a list or array and the title for the chart
def plot_lorenz_curve(income, title):
    """Plot the Lorenz Curve given an array of values and the Gini coefficient."""
    income = np.sort(income)
    income = np.append([0], income)  # Start at 0
    cum_income = np.cumsum(income) / np.sum(income)  # Normalize cumulative values
    cum_pop = np.linspace(0, 1, len(cum_income))  # Population percentage
    equality_line = np.ones(len(cum_income))
    gini_index = calc_gini(income)
    plt.figure(figsize=(8, 6))
    plt.plot(cum_pop, cum_income, label="")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")  # Perfect equality line
    print("cum_pop", cum_pop)
    plt.fill_between(cum_pop, cum_income, cum_pop, color="skyblue", alpha=0.5)

    plt.xlabel("Cumulative Population Share")
    plt.ylabel("Cumulative Income Share")
    plt.title(f"{title} ' Gini Goefficient: ' {gini_index:.4f}")
    plt.legend()
    plt.grid(False)
    plt.show()

# Values are not sorted in the kakwani
# Send the values of the pre-tax income and tax as a dataframe
# with the fields 'income', and 'tax'
# Send the corresponding values of the tax
def plot_kakwani_lorenz_curve(income, tax, title):
    """Plot the Lorenz Curve given an array of values and the Gini coefficient."""
    #income = np.sort(df['income'])
    income = np.append([0], income)  # Start at 0
    cum_income = np.cumsum(income) / np.sum(income)  # Normalize cumulative values
    cum_pop = np.linspace(0, 1, len(cum_income))  # Population percentage
    gini_income = calc_gini(income)
                           
    #tax = np.sort(df['tax'])
    #tax = df['tax']
    tax = np.append([0], tax)  # Start at 0
    cum_tax = np.cumsum(tax) / np.sum(tax)  # Normalize cumulative values
    #cum_pop_post = np.linspace(0, 1, len(cum_tax))  # Population percentage
    gini_tax = calc_gini(tax)

    plt.figure(figsize=(8, 6))
    plt.plot(cum_pop, cum_income, marker='o', markevery=200, label="Lorenz Curve Income")
    plt.plot(cum_pop, cum_tax, marker='s', markevery=200, label="Concentration Curve Current Tax")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")  # Perfect equality line
    plt.fill_between(cum_pop, cum_income, cum_tax, color="skyblue", alpha=0.5)
    
    plt.xlabel("Cumulative Population Share")
    plt.ylabel("Cumulative Income/Tax Share")
    plt.xlim(0, 1.0)
    plt.ylim(0, 1.0)
    # Add annotation
    plt.annotate(f"Kakwani Index:  {gini_tax-gini_income:.2f}", 
                 xy=(0.02, 0.8),
                 fontsize=10, color='black')
    
    plt.title(f"{title}")
    plt.legend()
    plt.grid(False)
    plt.show()

def plot_kakwani_lorenz_curve_reform(income, tax1, tax2, label1, label2, title, tax3 = None, label3 = None):
    """Plot the Lorenz Curve given an array of values and the Gini coefficient."""
    #income = np.sort(df['income'])
    income = np.append([0], income)  # Start at 0
    cum_income = np.cumsum(income) / np.sum(income)  # Normalize cumulative values
    cum_pop = np.linspace(0, 1, len(cum_income))  # Population percentage
    gini_income = calc_gini(income)
                           
    tax1 = np.append([0], tax1)  # Start at 0
    cum_tax1 = np.cumsum(tax1) / np.sum(tax1)  # Normalize cumulative values
    #cum_pop_post = np.linspace(0, 1, len(cum_tax))  # Population percentage
    gini_tax1 = calc_gini(tax1)

    tax2 = np.append([0], tax2)  # Start at 0
    cum_tax2 = np.cumsum(tax2) / np.sum(tax2)  # Normalize cumulative values
    gini_tax2 = calc_gini(tax2)

    if tax3 is not None:
        tax3 = np.append([0], tax3)  # Start at 0
        cum_tax3 = np.cumsum(tax3) / np.sum(tax3)  # Normalize cumulative values
        gini_tax3 = calc_gini(tax3)    
    
    plt.figure(figsize=(8, 6))
    plt.plot(cum_pop, cum_income, label="Lorenz Curve Income")
    plt.plot(cum_pop, cum_tax1, marker='o', markevery=300, label=label1)
    plt.plot(cum_pop, cum_tax2, marker='s', markevery=200, label=label2)
    if (tax3 is not None) and (label3 is not None):
        plt.plot(cum_pop, cum_tax3, marker='^', markevery=250, label=label3)       
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")  # Perfect equality line
    plt.fill_between(cum_pop, cum_tax1, cum_tax2, color="skyblue", alpha=0.5)
    
    plt.xlabel("Cumulative Population Share")
    plt.ylabel("Cumulative Income/Tax Share")
    plt.xlim(0, 1.0)
    plt.ylim(0, 1.0)
    # Add annotation
    plt.annotate(f"Kakwani Index Current Tax:  {gini_tax1-gini_income:.2f}", 
                 xy=(0.02, 0.7),
                 fontsize=10, color='black')
    plt.annotate(f"Kakwani Index Option 1:  {gini_tax2-gini_income:.2f}", 
                 xy=(0.02, 0.65),
                 fontsize=10, color='black')
    if tax3 is not None:
        plt.annotate(f"Kakwani Index Option 2:  {gini_tax3-gini_income:.2f}", 
                     xy=(0.02, 0.6),
                     fontsize=10, color='black')        
    
    plt.title(f"{title}")
    plt.legend()
    plt.grid(False)
    plt.show()

    
    