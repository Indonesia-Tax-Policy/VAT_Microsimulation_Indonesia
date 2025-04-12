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

"Calculation for Social Security Contribution (SSC)"  
@iterate_jit(nopython=True)
def cal_ssc_w(ssc_rate, income_wage_l, ssc_w_calc):
    """
    Compute ssc for wages.
    """
    """ Note : First condition: Case when SSC is zero (e.g Exemption from SSC for TIDZ or no income from wages);
    Second condition:Case when gross income from wages is below minimum wages;
    Third condition: Case when gross income from wages is range between minium and maximum wages an
    Fourth condition:Case when gross income from wages is above maximum wages.
    note: income_wage_l = gross income for wages
    """
    ssc_w_calc = ssc_rate * income_wage_l
    return ssc_w_calc


"Calculation for tax base for wages"
@iterate_jit(nopython=True)
def cal_tax_base_w(income_wage_l, ssc_w_calc, personal_allowance_w):
    tax_base_w = income_wage_l - ssc_w_calc - personal_allowance_w
    tax_base_w = max(tax_base_w, 0.)
    return tax_base_w

"Calculation for PIT from wages only"
@iterate_jit(nopython=True)
def cal_pit_w(tax_base_w, rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3, pit_w):
    """
    Compute tax liability given the progressive tax rate schedule specified
    by the (marginal tax) rate* and (upper tax bracket) brk* parameters and
    given taxable income (taxinc)
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    taxinc = tax_base_w  
    
    pit_w = (rate1 * min(taxinc, tbrk1) +
                    rate2 * min(tbrk2 - tbrk1, max(0., taxinc - tbrk1)) +
                    rate3 * min(tbrk3 - tbrk2, max(0., taxinc - tbrk2)) +
                    rate4 * max(0., taxinc - tbrk3))        
    return (pit_w)

"Calculation for tax base from capital - income from interest and dividends against which no deduction is allowed"
@iterate_jit(nopython=True)
def cal_tax_base_c(income_dividends_c, income_interest_c, tti_c):
    tti_c = (income_dividends_c + income_interest_c)
    return (tti_c)

@iterate_jit(nopython=True)
def cal_total_gross_income(income_wage_l, income_dividends_c, income_interest_c,     
                           total_gross_income):
    """
    Compute total gross income.
    """
    total_gross_income = (income_wage_l + income_dividends_c + income_interest_c)
    return total_gross_income

"Calculation for PIT from capital"
@iterate_jit(nopython=True)
def cal_pit_c(capital_income_rate_a, tti_c, pit_c):
    pit_c = (tti_c*capital_income_rate_a)
    return pit_c


@iterate_jit(nopython=True)
def cal_total_pit(pit_w, pit_c, pitax):
    """
    Compute PIT.
    """
    pitax = pit_w + pit_c
    return pitax

