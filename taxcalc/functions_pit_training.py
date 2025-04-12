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
def cal_capital_income(income_dividends_c, income_interest_c,     
                           capital_income):
    """
    Compute total gross income.
    """
    capital_income = (income_dividends_c + income_interest_c)
    return capital_income

@iterate_jit(nopython=True)
def cal_total_gross_income(income_wage_l, income_dividends_c, income_interest_c,     
                           total_gross_income):
    """
    Compute total gross income.
    """
    total_gross_income = (income_wage_l + income_dividends_c + income_interest_c)
    return total_gross_income

@iterate_jit(nopython=True)
def cal_pit_c(capital_income_rate_a, capital_income, pitax_c):
    """
    Compute PIT for Capital Income.
    """
    pitax_c = capital_income_rate_a*capital_income
    return pitax_c

@iterate_jit(nopython=True)
def cal_pit_w(rate1, rate2, rate3, rate4, tbrk1, tbrk2, tbrk3, tbrk4, tbrk5, income_wage_l, pitax_w):
    """
    Compute PIT.
    """
    inc=income_wage_l
    if (inc<tbrk2):
        pitax_w=(inc-tbrk1)*rate1
    elif (inc<tbrk3):
        pitax_w=(tbrk2-tbrk1)*rate1 + (inc-tbrk2)*rate2
    elif (inc<tbrk4):
        pitax_w = (tbrk2-tbrk1)*rate1 + (tbrk3-tbrk2)*rate2 + (inc-tbrk3)*rate3
    elif (inc<tbrk5):
        pitax_w = (tbrk2-tbrk1)*rate1 + (tbrk3-tbrk2)*rate2 + (tbrk4-tbrk3)*rate3 + (inc-tbrk4)*rate4

    return pitax_w

@iterate_jit(nopython=True)
def cal_total_pit(pitax_w, pitax_c, pitax):
    """
    Compute Total PIT.
    """
    pitax = pitax_w + pitax_c
    return pitax