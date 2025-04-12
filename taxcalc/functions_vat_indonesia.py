
"""
pitaxcalc-demo functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit

@iterate_jit(nopython=True)
def cal_CONS_Food_Crops_behavior(CONS_Food_Crops, rate_Food_Crops, rate_Food_Crops_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Food_Crops_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Food_Crops<=0:
        elasticity=0
    elif CONS_Food_Crops<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Food_Crops<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Food_Crops
    rate_curr_law=rate_Food_Crops_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Food_Crops_behavior = CONS_Food_Crops*(1+frac_change_of_consumption)
    return CONS_Food_Crops_behavior

@iterate_jit(nopython=True)
def cal_vat_Food_Crops(CONS_Food_Crops_behavior, rate_Food_Crops, vat_Food_Crops):
    """
    """
    vat_Food_Crops = rate_Food_Crops * CONS_Food_Crops_behavior
    return vat_Food_Crops

@iterate_jit(nopython=True)
def cal_CONS_Processed_Food_behavior(CONS_Processed_Food, rate_Processed_Food, rate_Processed_Food_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Processed_Food_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Processed_Food<=0:
        elasticity=0
    elif CONS_Processed_Food<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Processed_Food<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Processed_Food
    rate_curr_law=rate_Processed_Food_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Processed_Food_behavior = CONS_Processed_Food*(1+frac_change_of_consumption)
    return CONS_Processed_Food_behavior

@iterate_jit(nopython=True)
def cal_vat_Processed_Food(CONS_Processed_Food_behavior, rate_Processed_Food, vat_Processed_Food):
    """
    """
    vat_Processed_Food = rate_Processed_Food * CONS_Processed_Food_behavior
    return vat_Processed_Food

@iterate_jit(nopython=True)
def cal_CONS_Fruits_Vegetables_Spices_behavior(CONS_Fruits_Vegetables_Spices, rate_Fruits_Vegetables_Spices, 
                                               rate_Fruits_Vegetables_Spices_curr_law, elasticity_consumption_threshold, 
                                               elasticity_consumption_value, CONS_Fruits_Vegetables_Spices_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Fruits_Vegetables_Spices<=0:
        elasticity=0
    elif CONS_Fruits_Vegetables_Spices<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Fruits_Vegetables_Spices<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Fruits_Vegetables_Spices
    rate_curr_law=rate_Fruits_Vegetables_Spices_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Fruits_Vegetables_Spices_behavior = CONS_Fruits_Vegetables_Spices*(1+frac_change_of_consumption)
    return CONS_Fruits_Vegetables_Spices_behavior

@iterate_jit(nopython=True)
def cal_vat_Fruits_Vegetables_Spices(CONS_Fruits_Vegetables_Spices_behavior, rate_Fruits_Vegetables_Spices, vat_Fruits_Vegetables_Spices):
    """
    """
    vat_Fruits_Vegetables_Spices = rate_Fruits_Vegetables_Spices * CONS_Fruits_Vegetables_Spices_behavior
    return vat_Fruits_Vegetables_Spices

@iterate_jit(nopython=True)
def cal_CONS_Fish_behavior(CONS_Fish, rate_Fish, rate_Fish_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Fish_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Fish<=0:
        elasticity=0
    elif CONS_Fish<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Fish<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Fish
    rate_curr_law=rate_Fish_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Fish_behavior = CONS_Fish*(1+frac_change_of_consumption)
    return CONS_Fish_behavior

@iterate_jit(nopython=True)
def cal_vat_Fish(CONS_Fish_behavior, rate_Fish, vat_Fish):
    """
    """
    vat_Fish = rate_Fish * CONS_Fish_behavior
    return vat_Fish

@iterate_jit(nopython=True)
def cal_CONS_Meat_behavior(CONS_Meat, rate_Meat, rate_Meat_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Meat_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Meat<=0:
        elasticity=0
    elif CONS_Meat<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Meat<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Meat
    rate_curr_law=rate_Meat_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Meat_behavior = CONS_Meat*(1+frac_change_of_consumption)
    return CONS_Meat_behavior

@iterate_jit(nopython=True)
def cal_vat_Meat(CONS_Meat_behavior, rate_Meat, vat_Meat):
    """
    """
    vat_Meat = rate_Meat * CONS_Meat_behavior
    return vat_Meat

@iterate_jit(nopython=True)
def cal_CONS_Poultry_behavior(CONS_Poultry, rate_Poultry, rate_Poultry_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Poultry_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Poultry<=0:
        elasticity=0
    elif CONS_Poultry<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Poultry<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Poultry
    rate_curr_law=rate_Poultry_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Poultry_behavior = CONS_Poultry*(1+frac_change_of_consumption)
    return CONS_Poultry_behavior

@iterate_jit(nopython=True)
def cal_vat_Poultry(CONS_Poultry_behavior, rate_Poultry, vat_Poultry):
    """
    """
    vat_Poultry = rate_Poultry * CONS_Poultry_behavior
    return vat_Poultry

@iterate_jit(nopython=True)
def cal_CONS_Dairy_behavior(CONS_Dairy, rate_Dairy, rate_Dairy_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Dairy_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Dairy<=0:
        elasticity=0
    elif CONS_Dairy<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Dairy<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Dairy
    rate_curr_law=rate_Dairy_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Dairy_behavior = CONS_Dairy*(1+frac_change_of_consumption)
    return CONS_Dairy_behavior

@iterate_jit(nopython=True)
def cal_vat_Dairy(CONS_Dairy_behavior, rate_Dairy, vat_Dairy):
    """
    """
    vat_Dairy = rate_Dairy * CONS_Dairy_behavior
    return vat_Dairy

@iterate_jit(nopython=True)
def cal_CONS_Beverages_behavior(CONS_Beverages, rate_Beverages, rate_Beverages_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Beverages_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Beverages<=0:
        elasticity=0
    elif CONS_Beverages<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Beverages<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Beverages
    rate_curr_law=rate_Beverages_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Beverages_behavior = CONS_Beverages*(1+frac_change_of_consumption)
    return CONS_Beverages_behavior

@iterate_jit(nopython=True)
def cal_vat_Beverages(CONS_Beverages_behavior, rate_Beverages, vat_Beverages):
    """
    """
    vat_Beverages = rate_Beverages * CONS_Beverages_behavior
    return vat_Beverages

@iterate_jit(nopython=True)
def cal_CONS_Alcohol_behavior(CONS_Alcohol, rate_Alcohol, rate_Alcohol_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Alcohol_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Alcohol<=0:
        elasticity=0
    elif CONS_Alcohol<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Alcohol<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Alcohol
    rate_curr_law=rate_Alcohol_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Alcohol_behavior = CONS_Alcohol*(1+frac_change_of_consumption)
    return CONS_Alcohol_behavior

@iterate_jit(nopython=True)
def cal_vat_Alcohol(CONS_Alcohol_behavior, rate_Alcohol, vat_Alcohol):
    """
    """
    vat_Alcohol = rate_Alcohol * CONS_Alcohol_behavior
    return vat_Alcohol

@iterate_jit(nopython=True)
def cal_CONS_Tobacco_behavior(CONS_Tobacco, rate_Tobacco, rate_Tobacco_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Tobacco_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Tobacco<=0:
        elasticity=0
    elif CONS_Tobacco<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Tobacco<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Tobacco
    rate_curr_law=rate_Tobacco_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Tobacco_behavior = CONS_Tobacco*(1+frac_change_of_consumption)
    return CONS_Tobacco_behavior

@iterate_jit(nopython=True)
def cal_vat_Tobacco(CONS_Tobacco_behavior, rate_Tobacco, vat_Tobacco):
    """
    """
    vat_Tobacco = rate_Tobacco * CONS_Tobacco_behavior
    return vat_Tobacco

@iterate_jit(nopython=True)
def cal_CONS_Other_Non_Consumption_behavior(CONS_Other_Non_Consumption, rate_Other_Non_Consumption, rate_Other_Non_Consumption_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Other_Non_Consumption_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Other_Non_Consumption<=0:
        elasticity=0
    elif CONS_Other_Non_Consumption<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Other_Non_Consumption<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Other_Non_Consumption
    rate_curr_law=rate_Other_Non_Consumption_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Other_Non_Consumption_behavior = CONS_Other_Non_Consumption*(1+frac_change_of_consumption)
    return CONS_Other_Non_Consumption_behavior

@iterate_jit(nopython=True)
def cal_vat_Other_Non_Consumption(CONS_Other_Non_Consumption_behavior, rate_Other_Non_Consumption, vat_Other_Non_Consumption):
    """
    """
    vat_Other_Non_Consumption = rate_Other_Non_Consumption * CONS_Other_Non_Consumption_behavior
    return vat_Other_Non_Consumption

@iterate_jit(nopython=True)
def cal_CONS_Rent_behavior(CONS_Rent, rate_Rent, rate_Rent_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Rent_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Rent<=0:
        elasticity=0
    elif CONS_Rent<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Rent<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Rent
    rate_curr_law=rate_Rent_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Rent_behavior = CONS_Rent*(1+frac_change_of_consumption) 
    return CONS_Rent_behavior

@iterate_jit(nopython=True)
def cal_vat_Rent(CONS_Rent_behavior, rate_Rent, vat_Rent):
    """
    """
    vat_Rent = rate_Rent * CONS_Rent_behavior
    return vat_Rent

@iterate_jit(nopython=True)
def cal_CONS_Electricity_behavior(CONS_Electricity, rate_Electricity, rate_Electricity_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Electricity_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Electricity<=0:
        elasticity=0
    elif CONS_Electricity<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Electricity<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Electricity
    rate_curr_law=rate_Electricity_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Electricity_behavior = CONS_Electricity*(1+frac_change_of_consumption)
    return CONS_Electricity_behavior

@iterate_jit(nopython=True)
def cal_vat_Electricity(CONS_Electricity_behavior, rate_Electricity, vat_Electricity):
    """
    """
    vat_Electricity = rate_Electricity * CONS_Electricity_behavior
    return vat_Electricity

@iterate_jit(nopython=True)
def cal_CONS_Water_behavior(CONS_Water, rate_Water, rate_Water_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Water_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Water<=0:
        elasticity=0
    elif CONS_Water<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Water<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Water
    rate_curr_law=rate_Water_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Water_behavior = CONS_Water*(1+frac_change_of_consumption)
    return CONS_Water_behavior

@iterate_jit(nopython=True)
def cal_vat_Water(CONS_Water_behavior, rate_Water, vat_Water):
    """
    """
    vat_Water = rate_Water * CONS_Water_behavior
    return vat_Water

@iterate_jit(nopython=True)
def cal_CONS_Fuel_behavior(CONS_Fuel, rate_Fuel, rate_Fuel_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Fuel_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Fuel<=0:
        elasticity=0
    elif CONS_Fuel<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Fuel<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Fuel
    rate_curr_law=rate_Fuel_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Fuel_behavior = CONS_Fuel*(1+frac_change_of_consumption)
    return CONS_Fuel_behavior

@iterate_jit(nopython=True)
def cal_vat_Fuel(CONS_Fuel_behavior, rate_Fuel, vat_Fuel):
    """
    """
    vat_Fuel = rate_Fuel * CONS_Fuel_behavior
    return vat_Fuel

@iterate_jit(nopython=True)
def cal_CONS_Other_Services_behavior(CONS_Other_Services, rate_Other_Services, rate_Other_Services_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Other_Services_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Other_Services<=0:
        elasticity=0
    elif CONS_Other_Services<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Other_Services<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Other_Services
    rate_curr_law=rate_Other_Services_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Other_Services_behavior = CONS_Other_Services*(1+frac_change_of_consumption)
    return CONS_Other_Services_behavior

@iterate_jit(nopython=True)
def cal_vat_Other_Services(CONS_Other_Services_behavior, rate_Other_Services, vat_Other_Services):
    """
    """
    vat_Other_Services = rate_Other_Services * CONS_Other_Services_behavior
    return vat_Other_Services

@iterate_jit(nopython=True)
def cal_CONS_Telecom_behavior(CONS_Telecom, rate_Telecom, rate_Telecom_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Telecom_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Telecom<=0:
        elasticity=0
    elif CONS_Telecom<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Telecom<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Telecom
    rate_curr_law=rate_Telecom_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Telecom_behavior = CONS_Telecom*(1+frac_change_of_consumption)
    return CONS_Telecom_behavior

@iterate_jit(nopython=True)
def cal_vat_Telecom(CONS_Telecom_behavior, rate_Telecom, vat_Telecom):
    """
    """
    vat_Telecom = rate_Telecom * CONS_Telecom_behavior
    return vat_Telecom

@iterate_jit(nopython=True)
def cal_CONS_Soap_Cosmetics_behavior(CONS_Soap_Cosmetics, rate_Soap_Cosmetics, rate_Soap_Cosmetics_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Soap_Cosmetics_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Soap_Cosmetics<=0:
        elasticity=0
    elif CONS_Soap_Cosmetics<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Soap_Cosmetics<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Soap_Cosmetics
    rate_curr_law=rate_Soap_Cosmetics_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Soap_Cosmetics_behavior = CONS_Soap_Cosmetics*(1+frac_change_of_consumption)
    return CONS_Soap_Cosmetics_behavior

@iterate_jit(nopython=True)
def cal_vat_Soap_Cosmetics(CONS_Soap_Cosmetics_behavior, rate_Soap_Cosmetics, vat_Soap_Cosmetics):
    """
    """
    vat_Soap_Cosmetics = rate_Soap_Cosmetics * CONS_Soap_Cosmetics_behavior
    return vat_Soap_Cosmetics

@iterate_jit(nopython=True)
def cal_CONS_Other_Home_Consumption_behavior(CONS_Other_Home_Consumption, rate_Other_Home_Consumption, rate_Other_Home_Consumption_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Other_Home_Consumption_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Other_Home_Consumption<=0:
        elasticity=0
    elif CONS_Other_Home_Consumption<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Other_Home_Consumption<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Other_Home_Consumption
    rate_curr_law=rate_Other_Home_Consumption_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Other_Home_Consumption_behavior = CONS_Other_Home_Consumption*(1+frac_change_of_consumption)
    return CONS_Other_Home_Consumption_behavior

@iterate_jit(nopython=True)
def cal_vat_Other_Home_Consumption(CONS_Other_Home_Consumption_behavior, rate_Other_Home_Consumption, vat_Other_Home_Consumption):
    """
    """
    vat_Other_Home_Consumption = rate_Other_Home_Consumption * CONS_Other_Home_Consumption_behavior
    return vat_Other_Home_Consumption

@iterate_jit(nopython=True)
def cal_CONS_Books_Newspapers_behavior(CONS_Books_Newspapers, rate_Books_Newspapers, rate_Books_Newspapers_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Books_Newspapers_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Books_Newspapers<=0:
        elasticity=0
    elif CONS_Books_Newspapers<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Books_Newspapers<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Books_Newspapers
    rate_curr_law=rate_Books_Newspapers_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Books_Newspapers_behavior = CONS_Books_Newspapers*(1+frac_change_of_consumption)
    return CONS_Books_Newspapers_behavior

@iterate_jit(nopython=True)
def cal_vat_Books_Newspapers(CONS_Books_Newspapers_behavior, rate_Books_Newspapers, vat_Books_Newspapers):
    """
    """
    vat_Books_Newspapers = rate_Books_Newspapers * CONS_Books_Newspapers_behavior
    return vat_Books_Newspapers

@iterate_jit(nopython=True)
def cal_CONS_Health_behavior(CONS_Health, rate_Health, rate_Health_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Health_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Health<=0:
        elasticity=0
    elif CONS_Health<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Health<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Health
    rate_curr_law=rate_Health_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Health_behavior = CONS_Health*(1+frac_change_of_consumption)
    return CONS_Health_behavior

@iterate_jit(nopython=True)
def cal_vat_Health(CONS_Health_behavior, rate_Health, vat_Health):
    """
    """
    vat_Health = rate_Health * CONS_Health_behavior
    return vat_Health

@iterate_jit(nopython=True)
def cal_CONS_Education_behavior(CONS_Education, rate_Education, rate_Education_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Education_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Education<=0:
        elasticity=0
    elif CONS_Education<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Education<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Education
    rate_curr_law=rate_Education_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Education_behavior = CONS_Education*(1+frac_change_of_consumption)
    return CONS_Education_behavior

@iterate_jit(nopython=True)
def cal_vat_Education(CONS_Education_behavior, rate_Education, vat_Education):
    """
    """
    vat_Education = rate_Education * CONS_Education_behavior
    return vat_Education

@iterate_jit(nopython=True)
def cal_CONS_Transport_Services_behavior(CONS_Transport_Services, rate_Transport_Services, rate_Transport_Services_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Transport_Services_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Transport_Services<=0:
        elasticity=0
    elif CONS_Transport_Services<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Transport_Services<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Transport_Services
    rate_curr_law=rate_Transport_Services_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Transport_Services_behavior = CONS_Transport_Services*(1+frac_change_of_consumption)
    return CONS_Transport_Services_behavior

@iterate_jit(nopython=True)
def cal_vat_Transport_Services(CONS_Transport_Services_behavior, rate_Transport_Services, vat_Transport_Services):
    """
    """
    vat_Transport_Services = rate_Transport_Services * CONS_Transport_Services_behavior
    return vat_Transport_Services

@iterate_jit(nopython=True)
def cal_CONS_Air_Transport_behavior(CONS_Air_Transport, rate_Air_Transport, rate_Air_Transport_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Air_Transport_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Air_Transport<=0:
        elasticity=0
    elif CONS_Air_Transport<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Air_Transport<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Air_Transport
    rate_curr_law=rate_Air_Transport_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Air_Transport_behavior = CONS_Air_Transport*(1+frac_change_of_consumption)
    return CONS_Air_Transport_behavior

@iterate_jit(nopython=True)
def cal_vat_Air_Transport(CONS_Air_Transport_behavior, rate_Air_Transport, vat_Air_Transport):
    """
    """
    vat_Air_Transport = rate_Air_Transport * CONS_Air_Transport_behavior
    return vat_Air_Transport

@iterate_jit(nopython=True)
def cal_CONS_Accomodation_behavior(CONS_Accomodation, rate_Accomodation, rate_Accomodation_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Accomodation_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Accomodation<=0:
        elasticity=0
    elif CONS_Accomodation<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Accomodation<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Accomodation
    rate_curr_law=rate_Accomodation_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Accomodation_behavior = CONS_Accomodation*(1+frac_change_of_consumption)
    return CONS_Accomodation_behavior

@iterate_jit(nopython=True)
def cal_vat_Accomodation(CONS_Accomodation_behavior, rate_Accomodation, vat_Accomodation):
    """
    """
    vat_Accomodation = rate_Accomodation * CONS_Accomodation_behavior
    return vat_Accomodation

@iterate_jit(nopython=True)
def cal_CONS_Entertainment_behavior(CONS_Entertainment, rate_Entertainment, rate_Entertainment_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Entertainment_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Entertainment<=0:
        elasticity=0
    elif CONS_Entertainment<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Entertainment<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Entertainment
    rate_curr_law=rate_Entertainment_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Entertainment_behavior = CONS_Entertainment*(1+frac_change_of_consumption)
    return CONS_Entertainment_behavior

@iterate_jit(nopython=True)
def cal_vat_Entertainment(CONS_Entertainment_behavior, rate_Entertainment, vat_Entertainment):
    """
    """
    vat_Entertainment = rate_Entertainment * CONS_Entertainment_behavior
    return vat_Entertainment

@iterate_jit(nopython=True)
def cal_CONS_Finance_behavior(CONS_Finance, rate_Finance, rate_Finance_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Finance_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Finance<=0:
        elasticity=0
    elif CONS_Finance<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Finance<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Finance
    rate_curr_law=rate_Finance_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Finance_behavior = CONS_Finance*(1+frac_change_of_consumption)
    return CONS_Finance_behavior

@iterate_jit(nopython=True)
def cal_vat_Finance(CONS_Finance_behavior, rate_Finance, vat_Finance):
    """
    """
    vat_Finance = rate_Finance * CONS_Finance_behavior
    return vat_Finance

@iterate_jit(nopython=True)
def cal_CONS_Clothing_Footwear_behavior(CONS_Clothing_Footwear, rate_Clothing_Footwear, rate_Clothing_Footwear_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Clothing_Footwear_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Clothing_Footwear<=0:
        elasticity=0
    elif CONS_Clothing_Footwear<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Clothing_Footwear<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Clothing_Footwear
    rate_curr_law=rate_Clothing_Footwear_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Clothing_Footwear_behavior = CONS_Clothing_Footwear*(1+frac_change_of_consumption)
    return CONS_Clothing_Footwear_behavior

@iterate_jit(nopython=True)
def cal_vat_Clothing_Footwear(CONS_Clothing_Footwear_behavior, rate_Clothing_Footwear, vat_Clothing_Footwear):
    """
    """
    vat_Clothing_Footwear = rate_Clothing_Footwear * CONS_Clothing_Footwear_behavior
    return vat_Clothing_Footwear

@iterate_jit(nopython=True)
def cal_CONS_Furniture_behavior(CONS_Furniture, rate_Furniture, rate_Furniture_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Furniture_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Furniture<=0:
        elasticity=0
    elif CONS_Furniture<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Furniture<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Furniture
    rate_curr_law=rate_Furniture_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Furniture_behavior = CONS_Furniture*(1+frac_change_of_consumption)
    return CONS_Furniture_behavior

@iterate_jit(nopython=True)
def cal_vat_Furniture(CONS_Furniture_behavior, rate_Furniture, vat_Furniture):
    """
    """
    vat_Furniture = rate_Furniture * CONS_Furniture_behavior
    return vat_Furniture

@iterate_jit(nopython=True)
def cal_CONS_Durable_Goods_behavior(CONS_Durable_Goods, rate_Durable_Goods, rate_Durable_Goods_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Durable_Goods_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Durable_Goods<=0:
        elasticity=0
    elif CONS_Durable_Goods<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Durable_Goods<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Durable_Goods
    rate_curr_law=rate_Durable_Goods_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Durable_Goods_behavior = CONS_Durable_Goods*(1+frac_change_of_consumption)
    return CONS_Durable_Goods_behavior

@iterate_jit(nopython=True)
def cal_vat_Durable_Goods(CONS_Durable_Goods_behavior, rate_Durable_Goods, vat_Durable_Goods):
    """
    """
    vat_Durable_Goods = rate_Durable_Goods * CONS_Durable_Goods_behavior
    return vat_Durable_Goods

@iterate_jit(nopython=True)
def cal_CONS_Vehicle_Purchase_behavior(CONS_Vehicle_Purchase, rate_Vehicle_Purchase, rate_Vehicle_Purchase_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Vehicle_Purchase_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Vehicle_Purchase<=0:
        elasticity=0
    elif CONS_Vehicle_Purchase<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Vehicle_Purchase<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Vehicle_Purchase
    rate_curr_law=rate_Vehicle_Purchase_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Vehicle_Purchase_behavior = CONS_Vehicle_Purchase*(1+frac_change_of_consumption)
    return CONS_Vehicle_Purchase_behavior

@iterate_jit(nopython=True)
def cal_vat_Vehicle_Purchase(CONS_Vehicle_Purchase_behavior, rate_Vehicle_Purchase, vat_Vehicle_Purchase):
    """
    """
    vat_Vehicle_Purchase = rate_Vehicle_Purchase * CONS_Vehicle_Purchase_behavior
    return vat_Vehicle_Purchase

@iterate_jit(nopython=True)
def cal_CONS_Other_Consumption_behavior(CONS_Other_Consumption, rate_Other_Consumption, rate_Other_Consumption_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Other_Consumption_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Other_Consumption<=0:
        elasticity=0
    elif CONS_Other_Consumption<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Other_Consumption<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Other_Consumption
    rate_curr_law=rate_Other_Consumption_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Other_Consumption_behavior = CONS_Other_Consumption*(1+frac_change_of_consumption)
    return CONS_Other_Consumption_behavior

@iterate_jit(nopython=True)
def cal_vat_Other_Consumption(CONS_Other_Consumption_behavior, rate_Other_Consumption, vat_Other_Consumption):
    """
    """
    vat_Other_Consumption = rate_Other_Consumption * CONS_Other_Consumption_behavior
    return vat_Other_Consumption

@iterate_jit(nopython=True)
def cal_CONS_Religious_Consumption_behavior(CONS_Religious_Consumption, rate_Religious_Consumption, rate_Religious_Consumption_curr_law, elasticity_consumption_threshold, elasticity_consumption_value, CONS_Religious_Consumption_behavior):
    """
    Compute consumption after adjusting for behavior.
    """
    elasticity_consumption_threshold0 = elasticity_consumption_threshold[0]
    elasticity_consumption_threshold1 = elasticity_consumption_threshold[1]
    #elasticity_consumption_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_consumption_value0=elasticity_consumption_value[0]
    elasticity_consumption_value1=elasticity_consumption_value[1]
    elasticity_consumption_value2=elasticity_consumption_value[2]
    if CONS_Religious_Consumption<=0:
        elasticity=0
    elif CONS_Religious_Consumption<elasticity_consumption_threshold0:
        elasticity=elasticity_consumption_value0
    elif CONS_Religious_Consumption<elasticity_consumption_threshold1:
        elasticity=elasticity_consumption_value1
    else:
        elasticity=elasticity_consumption_value2
    rate=rate_Religious_Consumption
    rate_curr_law=rate_Religious_Consumption_curr_law
# Compute the fractional change of VAT rate safely
    if rate == 0 and rate_curr_law == 0:
        # If both rates are zero, we set the fraction change to 0 (i.e. no effect)
        frac_change_of_vat_rate = 0
    elif rate_curr_law == 0:
        # If current law rate is zero but the other rate is non-zero, this would normally cause a division by zero.
        # You can choose to raise an error, or decide on another fallback behavior.
        frac_change_of_vat_rate = 0
    else:
        frac_change_of_vat_rate = (rate - rate_curr_law) / rate_curr_law
    frac_change_of_consumption = elasticity*frac_change_of_vat_rate
    CONS_Religious_Consumption_behavior = CONS_Religious_Consumption*(1+frac_change_of_consumption)
    return CONS_Religious_Consumption_behavior

@iterate_jit(nopython=True)
def cal_vat_Religious_Consumption(CONS_Religious_Consumption_behavior, rate_Religious_Consumption, vat_Religious_Consumption):
    """
    """
    vat_Religious_Consumption = rate_Religious_Consumption * CONS_Religious_Consumption_behavior
    return vat_Religious_Consumption

@iterate_jit(nopython=True)
def cal_vat(vat_Food_Crops, vat_Processed_Food, vat_Fruits_Vegetables_Spices, vat_Fish, vat_Meat, vat_Poultry, vat_Dairy, vat_Beverages,
            vat_Alcohol, vat_Tobacco, vat_Other_Non_Consumption, vat_Rent, vat_Electricity, vat_Water, vat_Fuel, vat_Other_Services,
            vat_Telecom, vat_Soap_Cosmetics, vat_Other_Home_Consumption, vat_Books_Newspapers, vat_Health, vat_Education, 
            vat_Transport_Services, vat_Air_Transport, vat_Accomodation, vat_Entertainment, vat_Finance, vat_Clothing_Footwear, 
            vat_Furniture, vat_Durable_Goods, vat_Vehicle_Purchase, vat_Other_Consumption, vat_Religious_Consumption, vatax):
    # Sum the VAT values for the following products:
    # vat_Food_Crops, vat_Processed_Food, vat_Fruits_Vegetables_Spices, vat_Fish, vat_Meat, vat_Poultry, vat_Dairy, vat_Beverages, vat_Alcohol, vat_Tobacco, vat_Other_Non_Consumption, vat_Rent, vat_Electricity, vat_Water, vat_Fuel, vat_Other_Services, vat_Telecom, vat_Soap_Cosmetics, vat_Other_Home_Consumption, vat_Books_Newspapers, vat_Health, vat_Education, vat_Transport_Services, vat_Air_Transport, vat_Accomodation, vat_Entertainment, vat_Finance, vat_Clothing_Footwear, vat_Furniture, vat_Durable_Goods, vat_Vehicle_Purchase, vat_Other_Consumption, vat_Religious_Consumption
    vat = vat_Food_Crops + vat_Processed_Food + vat_Fruits_Vegetables_Spices + vat_Fish + vat_Meat + vat_Poultry + vat_Dairy + vat_Beverages + vat_Alcohol + vat_Tobacco + vat_Other_Non_Consumption + vat_Rent + vat_Electricity + vat_Water + vat_Fuel + vat_Other_Services + vat_Telecom + vat_Soap_Cosmetics + vat_Other_Home_Consumption + vat_Books_Newspapers + vat_Health + vat_Education + vat_Transport_Services + vat_Air_Transport + vat_Accomodation + vat_Entertainment + vat_Finance + vat_Clothing_Footwear + vat_Furniture + vat_Durable_Goods + vat_Vehicle_Purchase + vat_Other_Consumption + vat_Religious_Consumption
    vatax = vat
    return vatax
