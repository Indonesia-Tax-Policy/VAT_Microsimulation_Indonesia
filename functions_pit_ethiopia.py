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
def cal_gross_income(Employment_Income, Other_Income_Federal,     
                           gross_income):
    """
    Compute gross income.
    """
    gross_income = Employment_Income + Other_Income_Federal
    return gross_income

@iterate_jit(nopython=True)
def cal_employment_income(deduction_employment, Employment_Income, 
                          employment_income_taxable):
    """
    Compute total gross income.
    """
    employment_income_taxable = Employment_Income - deduction_employment
    return employment_income_taxable

@iterate_jit(nopython=True)
def cal_other_income(Other_Income_Federal):
    """
    Compute Other Income.
    """
    Other_Income_Federal = Other_Income_Federal
    return Other_Income_Federal

@iterate_jit(nopython=True)
def cal_taxable_income(tax_global_income_federal, standard_deduction,
                       employment_income_taxable, Other_Income_Federal, 
                       taxable_income):
    """
    Compute Taxable Income.
    """
    if (tax_global_income_federal>=0.9999):
        taxable_income = employment_income_taxable + Other_Income_Federal - standard_deduction
    else:
        taxable_income = employment_income_taxable - standard_deduction
    return taxable_income

@iterate_jit(nopython=True)
def cal_pit_before_credit(rate1, rate2, rate3, rate4, rate5, rate6, rate7,
              tbrk1, tbrk2, tbrk3, tbrk4, tbrk5, tbrk6, tbrk7,
              taxable_income, bracket1, bracket2, bracket3, 
              bracket4, bracket5, bracket6, bracket7, 
              pitax_before_tax_credit):
    """
    Compute PIT.
    """
    bracket1, bracket2, bracket3, bracket4, bracket5, bracket6, bracket7 = 0,0,0,0,0,0,0

    inc=taxable_income
    if (inc<tbrk1):
        bracket1 = (inc-0)*rate1
    elif (inc<tbrk2):
        bracket1 = (tbrk1-0)*rate1
        bracket2 = (inc-tbrk1)*rate2
    elif (inc<tbrk3):
        bracket1 = (tbrk1-0)*rate1
        bracket2 = (tbrk2-tbrk1)*rate2
        bracket3 = (inc-tbrk2)*rate3
    elif (inc<tbrk4):
        bracket1 = (tbrk1-0)*rate1
        bracket2 = (tbrk2-tbrk1)*rate2
        bracket3 = (tbrk3-tbrk2)*rate3    
        bracket4 = (inc-tbrk3)*rate4        
    elif (inc<tbrk5):
        bracket1 = (tbrk1-0)*rate1
        bracket2 = (tbrk2-tbrk1)*rate2
        bracket3 = (tbrk3-tbrk2)*rate3
        bracket4 = (tbrk4-tbrk3)*rate4 
        bracket5 = (inc-tbrk4)*rate5
    elif (inc<tbrk6):
        bracket1 = (tbrk1-0)*rate1
        bracket2 = (tbrk2-tbrk1)*rate2
        bracket3 = (tbrk3-tbrk2)*rate3
        bracket4 = (tbrk4-tbrk3)*rate4
        bracket5 = (tbrk5-tbrk4)*rate5
        bracket6 = (inc-tbrk5)*rate6        
    elif (inc<tbrk7):
        bracket1 = (tbrk1-0)*rate1
        bracket2 = (tbrk2-tbrk1)*rate2
        bracket3 = (tbrk3-tbrk2)*rate3
        bracket4 = (tbrk4-tbrk3)*rate4
        bracket5 = (tbrk5-tbrk4)*rate5
        bracket6 = (tbrk6-tbrk5)*rate6
        bracket7 = (inc-tbrk6)*rate7
    
    pitax_before_tax_credit =  bracket1+bracket2+bracket3+bracket4+bracket5+bracket6+bracket7
    
    return pitax_before_tax_credit

@iterate_jit(nopython=True)
def cal_pit(tax_credit, pitax_before_tax_credit, pitax):
    """
    Compute PIT after Tax Credits.
    """
    pitax = pitax_before_tax_credit - tax_credit
    return pitax