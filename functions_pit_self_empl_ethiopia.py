"""
Functions that calculate personal income tax liability.
"""
# CODING-STYLE CHECKS:
# pycodestyle functions.py
# pylint --disable=locally-disabled functions.py

import math
import copy
import numpy as np
from taxcalc.decorators import iterate_jit


@iterate_jit(nopython=True)
def calc_Gross_Income(Sales, Other_Income, Gross_Income):
    """
    Compute accounting profit from business
    """
    Gross_Income = Sales + Other_Income
    return Gross_Income

@iterate_jit(nopython=True)
def calc_Gross_Profit(Gross_Income, Cost_of_Goods, Gross_Profit):
    """
    Compute accounting profit from business
    """
    Gross_Profit = Gross_Income - Cost_of_Goods
    return Gross_Profit

@iterate_jit(nopython=True)
def calc_Net_Income(Gross_Profit, Total_Expense, Net_Income):
    """
    Compute accounting profit from business
    """
    Net_Income = Gross_Profit - Total_Expense
    return Net_Income

@iterate_jit(nopython=True)
def Op_WDV_depr(Op_WDV_Bld, Op_WDV_Intang, Op_WDV_Mach, Op_WDV_Others, Op_WDV_Comp):
    """
    Return the opening WDV of each asset class.
    """
    Op_WDV_Bld, Op_WDV_Intang, Op_WDV_Mach, Op_WDV_Others, Op_WDV_Comp = (Op_WDV_Bld, 
    Op_WDV_Intang, Op_WDV_Mach, Op_WDV_Others, Op_WDV_Comp)
    return (Op_WDV_Bld, Op_WDV_Intang, Op_WDV_Mach, Op_WDV_Others, Op_WDV_Comp)

@iterate_jit(nopython=True)
def Tax_depr_Bld(Op_WDV_Bld, Add_Bld, Excl_Bld, rate_depr_bld, Tax_depr_Bld):
    """
    Compute tax depreciation of building asset class.
    """
    Tax_depr_Bld = max(rate_depr_bld*(Op_WDV_Bld + Add_Bld - Excl_Bld),0)
    return Tax_depr_Bld

@iterate_jit(nopython=True)
def Tax_depr_Intang(Op_WDV_Intang, Add_Intang, Excl_Intang, rate_depr_intang, Tax_depr_Intang):
    """
    Compute tax depreciation of intangibles asset class
    """
    Tax_depr_Intang = max(rate_depr_intang*(Op_WDV_Intang + Add_Intang - Excl_Intang),0)
    return Tax_depr_Intang

@iterate_jit(nopython=True)
def Tax_depr_Mach(Op_WDV_Mach, Add_Mach, Excl_Mach, rate_depr_mach, Tax_depr_Mach):
    """
    Compute tax depreciation of Machinary asset class
    """
    Tax_depr_Mach = max(rate_depr_mach*(Op_WDV_Mach + Add_Mach - Excl_Mach),0)
    return Tax_depr_Mach

@iterate_jit(nopython=True)
def Tax_depr_Others(Op_WDV_Others, Add_Others, Excl_Others, rate_depr_others, Tax_depr_Others):
    """
    Compute tax depreciation of Other asset class
    """
    Tax_depr_Others = max(rate_depr_others*(Op_WDV_Others + Add_Others - Excl_Others),0)
    return Tax_depr_Others

@iterate_jit(nopython=True)
def Tax_depr_Comp(Op_WDV_Comp, Add_Comp, Excl_Comp, rate_depr_comp, Tax_depr_Comp):
    """
    Compute tax depreciation of Computer asset class
    """
    Tax_depr_Comp = max(rate_depr_comp*(Op_WDV_Comp + Add_Comp - Excl_Comp),0)
    return Tax_depr_Comp

@iterate_jit(nopython=True)
def Tax_depreciation(Tax_depr_Bld, Tax_depr_Intang, Tax_depr_Mach, Tax_depr_Others, Tax_depr_Comp, Tax_depr):
    """
    Compute total depreciation of all asset classes.
    """
    Tax_depr = Tax_depr_Bld + Tax_depr_Intang + Tax_depr_Mach + Tax_depr_Others + Tax_depr_Comp
    return Tax_depr

@iterate_jit(nopython=True)
def Cl_WDV_depr(Op_WDV_Bld, Add_Bld, Excl_Bld, Tax_depr_Bld, 
                Op_WDV_Intang, Add_Intang, Excl_Intang, Tax_depr_Intang,
                Op_WDV_Mach, Add_Mach, Excl_Mach, Tax_depr_Mach,
                Op_WDV_Others, Add_Others, Excl_Others, Tax_depr_Others,
                Op_WDV_Comp, Add_Comp, Excl_Comp, Tax_depr_Comp,
                Cl_WDV_Bld, Cl_WDV_Intang, Cl_WDV_Mach, Cl_WDV_Others, Cl_WDV_Comp):
    """
    Compute Closing WDV of each block of asset.
    """
    Cl_WDV_Bld = max((Op_WDV_Bld + Add_Bld - Excl_Bld),0) - Tax_depr_Bld
    Cl_WDV_Intang = max((Op_WDV_Intang + Add_Intang - Excl_Intang),0) - Tax_depr_Intang
    Cl_WDV_Mach = max((Op_WDV_Mach + Add_Mach - Excl_Mach),0) - Tax_depr_Mach
    Cl_WDV_Others = max((Op_WDV_Others + Add_Others - Excl_Others),0) - Tax_depr_Others
    Cl_WDV_Comp= max((Op_WDV_Comp + Add_Comp - Excl_Comp),0) - Tax_depr_Comp
    return (Cl_WDV_Bld, Cl_WDV_Intang, Cl_WDV_Mach, Cl_WDV_Others, Cl_WDV_Comp)

@iterate_jit(nopython=True)
def calc_Total_Deductions(Tax_depr, Total_Deductions):
    """
    Compute net taxable profits afer allowing deductions.
    """
    Total_Deductions = Tax_depr-Tax_depr
    return Total_Deductions

@iterate_jit(nopython=True)
def calc_Carried_Forward_Losses(Loss_CF_Prev, Loss_CB_Adj, CF_losses):
    """
    Compute net taxable profits afer allowing deductions.
    """
    CF_losses = Loss_CF_Prev+Loss_CB_Adj
    return CF_losses

@iterate_jit(nopython=True)
def calc_Total_Taxable_Profit(Net_Income, Total_Taxable_Profit):
    """
    Compute total taxable profits afer adding back non-allowable deductions.
    """
    Total_Taxable_Profit = Net_Income
    return Total_Taxable_Profit

@iterate_jit(nopython=True)
def calc_Taxable_Business_Income(Total_Taxable_Profit, Total_Deductions, Taxable_Business_Income):
    """
    Compute net taxable profits afer allowing deductions.
    """
    Taxable_Business_Income = Total_Taxable_Profit - Total_Deductions
    return Taxable_Business_Income

@iterate_jit(nopython=True)
def calc_Tax_base_CF_losses(Taxable_Business_Income, Loss_CFLimit, CF_losses,
    Loss_lag1, Loss_lag2, Loss_lag3, Loss_lag4, Loss_lag5, Loss_lag6, Loss_lag7, Loss_lag8,
    newloss1, newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8, Used_loss_total, Tax_base):
    
    """
    Compute net tax base afer allowing donations and losses.
    """
    BF_loss = np.array([Loss_lag1, Loss_lag2, Loss_lag3, Loss_lag4, Loss_lag5, Loss_lag6, Loss_lag7, Loss_lag8])
    
    Gross_Tax_base = Taxable_Business_Income

    if BF_loss.sum() == 0:
        BF_loss[0] = CF_losses

    N = int(Loss_CFLimit)
    if N == 0:
        (newloss1, newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8) = np.zeros(8)
        Used_loss_total = 0
        Tax_base = Gross_Tax_base
        
    else:
        BF_loss = BF_loss[:N]
                
        if Gross_Tax_base < 0:
            CYL = abs(Gross_Tax_base)
            Used_loss = np.zeros(N)
        elif Gross_Tax_base >0:
            CYL = 0
            Cum_used_loss = 0
            Used_loss = np.zeros(N)
            for i in range(N, 0, -1):
                GTI = Gross_Tax_base - Cum_used_loss
                Used_loss[i-1] = min(BF_loss[i-1], GTI)
                Cum_used_loss += Used_loss[i-1]
        elif Gross_Tax_base == 0:
            CYL=0
            Used_loss = np.zeros(N)
    
        New_loss = BF_loss - Used_loss
        Tax_base = Gross_Tax_base - Used_loss.sum()
        newloss1 = CYL
        Used_loss_total = Used_loss.sum()
        (newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8) = np.append(New_loss[:-1], np.zeros(8-N))

    return (Tax_base, newloss1, newloss2, newloss3, newloss4, newloss5, newloss6, newloss7, newloss8, Used_loss_total)


@iterate_jit(nopython=True)
def calc_Net_tax_base(Tax_base, Net_tax_base):
    """
    Compute net tax base afer allowing deductions.
    """
    Net_tax_base = Tax_base
    return Net_tax_base

@iterate_jit(nopython=True)
def calc_Imputed_tax_base(Tax_Due, Tax_base_Imputed):
    """
    Compute net tax base afer allowing donations and losses.
    """
    Tax_base_Imputed = Tax_Due
    return Tax_base_Imputed

"Calculation for incorporating behavior - uses tax elasticity of total tax from labour income "
"Elasticity = % Change in income / % Change in tax rate "

@iterate_jit(nopython=True)
def calc_Net_tax_base_behavior(rate1, rate2, rate3, rate4, rate5, rate6, rate7,
                         tbrk1, tbrk2, tbrk3, tbrk4, tbrk5, tbrk6, tbrk7,
                         rate1_curr_law, rate2_curr_law, rate3_curr_law, 
                         rate4_curr_law, rate5_curr_law, rate6_curr_law, 
                         rate7_curr_law, tbrk1_curr_law, tbrk2_curr_law,
                         tbrk3_curr_law, tbrk4_curr_law, tbrk5_curr_law, 
                         tbrk6_curr_law, tbrk7_curr_law,
                         elasticity_pit_taxable_income_threshold,
                         elasticity_pit_taxable_income_value, Net_tax_base,
                         Net_tax_base_behavior):
    """
    Compute taxable total income after adjusting for behavior.
    """  
    elasticity_taxable_income_threshold0 = elasticity_pit_taxable_income_threshold[0]
    elasticity_taxable_income_threshold1 = elasticity_pit_taxable_income_threshold[1]
    #elasticity_taxable_income_threshold2 = elasticity_pit_taxable_income_threshold[2]
    elasticity_taxable_income_value0=elasticity_pit_taxable_income_value[0]
    elasticity_taxable_income_value1=elasticity_pit_taxable_income_value[1]
    elasticity_taxable_income_value2=elasticity_pit_taxable_income_value[2]
    if Net_tax_base<=0:
        elasticity=0
    elif Net_tax_base<elasticity_taxable_income_threshold0:
        elasticity=elasticity_taxable_income_value0
    elif Net_tax_base<elasticity_taxable_income_threshold1:
        elasticity=elasticity_taxable_income_value1
    else:
        elasticity=elasticity_taxable_income_value2

    if Net_tax_base<0:
        marg_rate=0
    elif Net_tax_base<=tbrk1:
        marg_rate=rate1
    elif Net_tax_base<=tbrk2:
        marg_rate=rate2
    elif Net_tax_base<=tbrk3:
        marg_rate=rate3
    elif Net_tax_base<=tbrk4:
        marg_rate=rate4
    elif Net_tax_base<=tbrk5:
        marg_rate=rate5
    elif Net_tax_base<=tbrk6:
        marg_rate=rate6        
    else:        
        marg_rate=rate7

    if Net_tax_base<0:
        marg_rate_curr_law=0
    elif Net_tax_base<=tbrk1_curr_law:
        marg_rate_curr_law=rate1_curr_law
    elif Net_tax_base<=tbrk2_curr_law:
        marg_rate_curr_law=rate2_curr_law
    elif Net_tax_base<=tbrk3_curr_law:
        marg_rate_curr_law=rate3_curr_law
    elif Net_tax_base<=tbrk4_curr_law:
        marg_rate_curr_law=rate4_curr_law
    elif Net_tax_base<=tbrk5_curr_law:
        marg_rate_curr_law=rate5_curr_law
    elif Net_tax_base<=tbrk6_curr_law:
        marg_rate_curr_law=rate6_curr_law       
    else:        
        marg_rate_curr_law=rate7_curr_law
    
    frac_change_net_of_pit_rate = ((1-marg_rate)-(1-marg_rate_curr_law))/(1-marg_rate_curr_law)
    frac_change_Net_tax_base = elasticity*(frac_change_net_of_pit_rate)  
    Net_tax_base_behavior = Net_tax_base*(1+frac_change_Net_tax_base)
    return Net_tax_base_behavior



DEBUG = False
DEBUG_IDX = 0

@iterate_jit(nopython=True)
def calc_mat_liability(mat_rate, Sales, MAT):
    """
    Compute tax liability given the corporate rate
    """
    # subtract TI_special_rates from TTI to get Aggregate_Income, which is
    # the portion of TTI that is taxed at normal rates
    MAT = mat_rate*max(Sales,0)
        
    return MAT

@iterate_jit(nopython=True)
def cal_pit_self_empl_before_credit(rate1, rate2, rate3, rate4, rate5, rate6, rate7,
              tbrk1, tbrk2, tbrk3, tbrk4, tbrk5, tbrk6, tbrk7,
              Net_tax_base_behavior, MAT, bracket1, bracket2, bracket3, 
              bracket4, bracket5, bracket6, bracket7, 
              pitax_before_tax_credit):
    """
    Compute PIT.
    """
    bracket1, bracket2, bracket3, bracket4, bracket5, bracket6, bracket7 = 0,0,0,0,0,0,0

    inc=Net_tax_base_behavior
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
           
    if MAT>pitax_before_tax_credit:
        pitax_before_tax_credit = MAT
    return pitax_before_tax_credit

@iterate_jit(nopython=True)
def cal_pit_self_empl(turnover_tax_rate, sales_threshold1, sales_threshold2, Sales, Total_Credit, pitax_before_tax_credit, citax):
    """
    Compute PIT after Tax Credits.
    """
    if (Sales<=sales_threshold1):
        citax = 0
    elif (Sales<=sales_threshold2):
        citax = turnover_tax_rate*Sales
    else:
        citax = pitax_before_tax_credit
    return citax