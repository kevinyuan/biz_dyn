import numpy as np
import statsmodels.api as sm
#import pylab as pl
import matplotlib.pyplot as pl
import sys

def f_trading_profit(sales, price, direct_cost, mkt_cost, tool_cost, trading_cost):
    trading_profit = sales * (price - direct_cost) - mkt_cost - trading_cost
    #print "trading_profit: ", trading_profit
    return trading_profit

def f_direct_cost(production, production_prev, total_tool_qty):
    if production_prev == 0:
        disruption_ratio = 0  # new factory
    else:
        production_change = float(production - production_prev) / float(production_prev)
        production_change = np.abs(production_change*100)
        if (production_change > 30):
            print "warning: production_change > 30% : ", production_change
            sys.exit(1)
        ## regression with 0,0; 10,2.5; 25,15
        disruption_ratio = 0.0233*production_change**2+0.0167*production_change
        disruption_ratio = np.round(disruption_ratio/100,4)
    direct_cost = 257.29 * ((production/1000)**0.0942) * (total_tool_qty**(-0.3425)) 
    direct_cost = np.round(direct_cost, 3)
    direct_cost_w_disrpt = direct_cost * (1+disruption_ratio)
    direct_cost_w_disrpt = np.round(direct_cost_w_disrpt, 3)
    #print "production_change: ", production_change  
    #print "disruption_ratio: ", disruption_ratio
    #print "direct_cost: ",  direct_cost
    #print "direct_cost_w_disrpt: ",  direct_cost_w_disrpt
    return (direct_cost, direct_cost_w_disrpt, production_change, disruption_ratio)

def f_mkt_cost(sales, price, gnp):
    mkt_cost = (sales + 2.578*107 + 1095.4160 * price - 2.652*105 * gnp) / 0.1533       
    #print "mkt_cost: ", mkt_cost
    return mkt_cost

def f_trading_cost(ship_cost, dealer_cost):
    trading_cost = ship_cost + dealer_cost 
    #print "trading_cost: ", trading_cost
    return trading_cost

def f_ship_cost(ship_qty):
    if (ship_qty >= 100000):
        ship_cost = ship_qty * 4
    else:
        ship_cost = ship_qty * 8
    #print "ship_cost: ", ship_cost
    return ship_cost

def f_ship_cost_chart():
    s = np.linspace(50000,200000,150001)
    ca = []
    for i in s:
        c = f_ship_cost(i)
        ca.append(c)
    pl.plot(s,ca)
    pl.show()

#f_ship_cost_chart()


def f_dealer_cost(sales, existing_dealer=0):
    dealer_qty = np.ceil(sales / 2500)
    if (dealer_qty < existing_dealer):
        dealer_qty = existing_dealer
    dealer_cost = dealer_qty * 30000
    #print "dealer_qty: ", dealer_qty
    #print "dealer_cost: ", dealer_cost
    return (dealer_cost, dealer_qty)

def f_dealer_cost_chart():
    s = np.linspace(50000,200000,150001)
    c,n = f_dealer_cost(s)
    pl.plot(s,c)
    pl.show()

#f_dealer_cost_chart
def f_tool_depr(tool_owned_qty):
    d = np.round((tool_owned_qty * 2.5/100),0)
    return d

def f_tool_cost(tool_price, tool_owned_qty, tool_buy_qty, tool_hire_qty):
    tool_hire_cost = 2000 * tool_hire_qty
    tool_buy_cost = tool_price * tool_buy_qty
    tool_depr_cost = f_tool_depr(tool_owned_qty) * tool_price 
    tool_cost = tool_hire_cost + tool_buy_cost + tool_depr_cost
    #print "tool_hire_cost :",  tool_hire_cost 
    #print "tool_buy_cost :",   tool_buy_cost  
    #print "tool_depr_cost :",  tool_depr_cost 
    #print "tool_cost :",  tool_cost 
    return tool_cost

def f_bank_interest(init_cash, current_expense, overdraft_facility):
    cost_of_od = overdraft_facility * 0.0025 

    cash_at_bank = init_cash - current_expense

    if (cash_at_bank >= 0):
        i_rec = cash_at_bank * 0.03
        i_od_4 = 0 
        i_od_6 = 0
    else:
        i_rec = 0
        if (cash_at_bank >= overdraft_facility): # within o/d
            i_od_4 = cash_at_bank * 0.04 
            i_od_6 = 0
        else:  # exceed o/d
            i_od_4 = overdraft_facility * 0.04
            i_od_6 = (cash_at_bank - overdraft_facility) * 0.06

    net_interest = i_rec + i_od_4 + i_od_6 + cost_of_od 
    # net_interest<0: pay interest to bank 
    # net_interest>0: receive interest from bank 
    return (net_interest, cash_at_bank, i_rec , i_od_4 , i_od_6 , cost_of_od )
    # net_interest<0: pay interest to bank 

def f_bond_interest(bond):
    i = bond * 0.02
    return i

def f_pretax_profit(trading_profit, bank_interest, bond_interest):
    pretax_profit  = trading_profit + bank_interest - bond_interest   
    #print "pretax_profit:",  pretax_profit  
    return pretax_profit  

def f_tax(pretax_profit, tax_allowance):
    if (pretax_profit < tax_allowance ):
        tax =  0 
    else:
        tax = pretax_profit * 50/100
    #print "tax: ", tax
    return tax

def f_net_profit(pretax_profit, tax):
    net_profit = earning_before_tax - tax
    #print "net_profit: ", net_profit
    return net_profit

#def f_optimal_tool_num_chart_1(production, production_prev, tool_price, tool_owned_qty):
#    cost_of_production_list = []
#    num_of_tool_list = []
#    tool_hire_qty = 0
#    total_tool_qty = tool_owned_qty 
#    while (total_tool_qty <= 2000):
#    #while (total_tool_qty <= 662):
#        total_tool_qty  = tool_owned_qty + tool_hire_qty
#        direct_cost = f_direct_cost(production, production_prev, total_tool_qty)
#        tool_cost = f_tool_cost(tool_price, tool_owned_qty, 0, tool_hire_qty)
#        cost_of_production = int(direct_cost*production+tool_cost)
#        tool_hire_qty += 10
#        num_of_tool_list.append(total_tool_qty)
#        #print "-------- num_of_tool: ", total_tool_qty, " ---------"
#        cost_of_production_list.append(cost_of_production)
#        #print "-------- cost_of_production: ", cost_of_production, " ---------"
#    pl.plot(num_of_tool_list, cost_of_production_list)
#    pl.show()
#    #print cost_of_production_list
#
##f_optimal_tool_num_chart_1(91000,70000,23000,662)
##f_optimal_tool_num_chart_1(118000,91000,23000,662)
##f_optimal_tool_num_chart_1(200000,154000,23000,662)

def f_optimize_tools(production, tool_price, calc_modes=0, tool_owned_qty_init=400, production_prev=0):

    tool_owned_qty = tool_owned_qty_init

    cost_delta_list = []
    num_of_tool_list = []

    tool_hire_qty = 0
    cost_of_production_new = 0

    total_tool_qty  = tool_owned_qty + tool_hire_qty

    while (total_tool_qty < 2000):

        if calc_modes == 0:   # compare vs non-hire and hire
            # cost with tool_owned_qty 
            tool_hire_qty = 0
            total_tool_qty  = tool_owned_qty + tool_hire_qty
            direct_cost,direct_cost_w_disrpt = f_direct_cost(production, production_prev, total_tool_qty)
            tool_cost = f_tool_cost(tool_price, tool_owned_qty, 0, tool_hire_qty)
            cost_of_production = int(direct_cost_w_disrpt*production+tool_cost)

            # cost with tool_owned_qty + tool_hire_qty
            tool_hire_qty = 1 
            total_tool_qty  = tool_owned_qty + tool_hire_qty
            direct_cost,direct_cost_w_disrpt = f_direct_cost(production, production_prev, total_tool_qty)
            tool_cost = f_tool_cost(tool_price, tool_owned_qty, 0, tool_hire_qty)
            cost_of_production_new = int(direct_cost_w_disrpt*production+tool_cost)

            # prepare for next loop
            tool_owned_qty += 1
            total_tool_qty = tool_owned_qty

        else:  # compare hire@t+1 and hire@t


            total_tool_qty  = tool_owned_qty + tool_hire_qty
            direct_cost,direct_cost_w_disrpt, production_change, disruption_ratio = f_direct_cost(production, production_prev, total_tool_qty)
            tool_cost = f_tool_cost(tool_price, tool_owned_qty, 0, tool_hire_qty)

            # record previus cost
            if tool_hire_qty == 0:
                cost_of_production = int(direct_cost_w_disrpt*production+tool_cost)
                cost_of_production_new = cost_of_production
            else:
                cost_of_production = cost_of_production_new 
                cost_of_production_new = int(direct_cost_w_disrpt*production+tool_cost)

            tool_hire_qty += 1

            if (tool_hire_qty > tool_owned_qty * 0.2):
               break

            total_tool_qty  = tool_owned_qty + tool_hire_qty

        # compare costs
        cost_delta = cost_of_production_new - cost_of_production

        if cost_delta <= 0:
            optimal_tool_num = total_tool_qty
            optimal_production_cost = cost_of_production_new

        num_of_tool_list.append(total_tool_qty)
        #print "-------- num_of_tool: ", total_tool_qty, " -> ", total_tool_qty, " ---------"

        cost_delta_list.append(cost_delta)
        #print "-------- cost_delta: ", cost_delta, " ---------"

    return (num_of_tool_list, cost_delta_list, optimal_tool_num, optimal_production_cost,direct_cost,direct_cost_w_disrpt, production_change, disruption_ratio)


# calc_modes: 
#    0. tool_owned_qty increase, check cost_delta with one hired tool
#    1. tool_owned_qty fixed, check cost_delta with increasing number of hired tools
def f_optimal_tool_num_chart(tool_price, calc_modes=0, tool_owned_qty_init=400, tool_owned_qty_inc=0, production_init=50000, production_inc=10000):

    pl.figure(figsize=(6,5),dpi=198)
    pl.close("all")
    f, p = pl.subplots(4,4) 
    f.subplots_adjust(hspace=0.6)
    f.subplots_adjust(wspace=0.3)
    #f.subplots_adjust(left=0.2, right=None)

    tool_owned_qty = tool_owned_qty_init
    production = production_init
    i = 0

    while (i <= 15):
    #while (production <= 60000):

        #cost_delta_list = []
        #num_of_tool_list = []
        #optimal_tool_num = 0

        num_of_tool_list, cost_delta_list, optimal_tool_num, optimal_production_cost, direct_cost, direct_cost_w_disrpt = f_optimize_tools(production, tool_price, calc_modes, tool_owned_qty)

        #print "production:", production
        x = i % 4
        y = i / 4
        #print " i: " , i, " x: ", x, " y: ", y

        title = "Production: " + str(production)
        optimal_unit_cost = np.round((optimal_production_cost / production), 3)
        lb = "optimal tool_num: " + str(optimal_tool_num) + " unit_cost: " + str(optimal_unit_cost)

        p[y, x].plot(num_of_tool_list, cost_delta_list, label=lb)
        p[y, x].xaxis.set_tick_params(labelsize=8)
        p[y, x].yaxis.set_tick_params(labelsize=8)
        p[y, x].hlines(0, num_of_tool_list[0], num_of_tool_list[len(num_of_tool_list)-1],"r")
        p[y, x].set_title(title, fontsize = 9)
        p[y, x].set_xlabel("Number of tools", fontsize = 8)
        p[y, x].set_ylabel("Cost", fontsize = 8)
        p[y, x].grid(True)
        p[y, x].legend(loc="best", fontsize = 7)

        tool_owned_qty+=tool_owned_qty_inc
        production+=production_inc
        i = i + 1

    if calc_modes == 0:
        fig_title = "calc_modes 0: tool_owned_qty increase, check cost_delta with one hired tool"
    else:
        fig_title = "calc_modes 1: tool_owned_qty fixed @ " + str(tool_owned_qty_init) + ", check cost_delta with increasing number of hired tools"
    pl.suptitle(fig_title)
    pl.show()

# Step 2: decide number of hired-tools for new production level
#f_optimal_tool_num_chart(23000)
#f_optimal_tool_num_chart(23000, 1, 645)
#f_optimal_tool_num_chart(23250, 1, 629, 0, 91000, 1000) #q4a2
#f_optimal_tool_num_chart(23250, 1, 488, 0, 100000, -5000) #q4a4
#f_optimal_tool_num_chart(23250, 1, 488, 10, 100000, 0) #q4a4, fix production, buy tool
#f_optimal_tool_num_chart(22500, 1, 613, 10, 92045, 0) #y7q1a2, fix production, buy tool
#f_optimal_tool_num_chart(22500, 1, 475, 10, 100720, 0) #y7q1a4, fix production, buy tool
#f_optimal_tool_num_chart(23500, 1, 598, 10, 102080, 0) #y7q2a2, fix production, buy tool
#f_optimal_tool_num_chart(23500, 1, 464, 10, 107700, 0) #y7q2a4, fix production, buy tool
#f_optimal_tool_num_chart(22250, 1, 583, 10, 102080, 0) #y7q3a2, fix production, buy tool
#f_optimal_tool_num_chart(22250, 1, 502, 10, 107700, 0) #y7q3a4, fix production, buy tool

def f_optimize_production(production_prev, tool_price, tool_owned_qty, price=80, open_inventory=0, existing_dealer=0, mkt_cost=0, init_cash=0, overdraft_facility=-13000000, bond=9900000):
    production_list = []
    cost_of_production_list = []
    trading_cost_list = []
    unit_trading_cost_list = []
    revenue_list = []
    net_trading_profit_list = []
    tool_num_list = []
    production_change = 1.001 
    total_tool_qty = tool_owned_qty 
    production_max_set = 0
    production_max = production_prev 
    MaxPreTaxProfit = 0

    inventory_cost = open_inventory * 40
    tool_depr_cost = f_tool_depr(tool_owned_qty) * tool_price 

    while (production_change <= 1.3):
        production = production_prev*production_change
        production_list.append(production)
        #print "-------- production: ", production, " ---------"

        num_of_tool_list, cost_delta_list, optimal_tool_num, optimal_production_cost, direct_cost, direct_cost_w_disrpt,production_change_x, disruption_ratio = f_optimize_tools(production, tool_price, 1, tool_owned_qty, production_prev)

        if (optimal_tool_num > tool_owned_qty * 1.2):
            #print "warning: @production ", production, ", (optimal_tool_num > tool_owned_qty * 1.2)", optimal_tool_num, tool_owned_qty
            if production_max_set == 0:
                production_max_set = 1
                production_max = production

        tool_num_list.append(optimal_tool_num) 

        cost_of_production_list.append(optimal_production_cost)
        unit_production_cost = np.ceil(float(optimal_production_cost/production)*100)/100

        #print "-------- cost_of_production: ", cost_of_production, " ---------"

        sales = production + open_inventory

        dealer_cost, dealer_qty = f_dealer_cost(sales, existing_dealer) # assume no shipment

        trading_cost = optimal_production_cost + inventory_cost + dealer_cost + mkt_cost # TODO + ship_cost
        trading_cost_list.append(trading_cost)
        #print "-------- trading_cost: ", trading_cost, " ---------"

        unit_trading_cost = np.ceil(float(trading_cost/sales)*100)/100
        unit_trading_cost_list.append(unit_trading_cost)
        #print "-------- unit_trading_cost: ", unit_trading_cost, " ---------"

        revenue = price * sales
        revenue_list.append(revenue)

        net_trading_profit = revenue - trading_cost # include depreciation
        net_trading_profit_list.append(net_trading_profit)

        current_expense = optimal_production_cost + dealer_cost + mkt_cost - tool_depr_cost # TODO + ship_cost

        bank_interest, cash_at_bank, i_rec, i_od_4 , i_od_6, cost_of_od = f_bank_interest(init_cash, current_expense, overdraft_facility)

        bond_interest = f_bond_interest(bond) 

        pretax_profit = f_pretax_profit(net_trading_profit, bank_interest, bond_interest)

        if (pretax_profit > MaxPreTaxProfit):
            MaxPreTaxProfit = pretax_profit
            MaxPreTaxProfit_production = production
            MaxPreTaxProfit_production_cost = optimal_production_cost
            MaxPreTaxProfit_tools = optimal_tool_num
            MaxPreTaxProfit_sales = sales
            MaxPreTaxProfit_revenue = revenue
            MaxPreTaxProfit_dealer_qty = dealer_qty
            MaxPreTaxProfit_dealer_cost = dealer_cost
            MaxPreTaxProfit_trading_cost = trading_cost
            MaxPreTaxProfit_unit_trading_cost = unit_trading_cost
            MaxPreTaxProfit_unit_production_cost = unit_production_cost
            MaxPreTaxProfit_direct_cost           = direct_cost
            MaxPreTaxProfit_direct_cost_w_disrpt  = direct_cost_w_disrpt 
            MaxPreTaxProfit_production_change_x = production_change_x
            MaxPreTaxProfit_disruption_ratio    = disruption_ratio
            MaxPreTaxProfit_net_trading_profit = net_trading_profit
            MaxPreTaxProfit_gross_trading_profit = net_trading_profit + tool_depr_cost
            MaxPreTaxProfit_current_expense  = current_expense 
            MaxPreTaxProfit_bank_interest    = bank_interest, cash_at_bank, i_rec, i_od_4 , i_od_6, cost_of_od
            MaxPreTaxProfit_bond_interest    = bond_interest

        production_change += 0.0001

    print "Strategy: maximize gross profit:"
    print "----------------"
    print "target production: ", MaxPreTaxProfit_production
    print "target sales: ", MaxPreTaxProfit_sales
    print "----------------"
    print "+revenue: ", MaxPreTaxProfit_revenue
    print "-trading_cost: ", MaxPreTaxProfit_trading_cost
    print "    total_production_cost(incl tools): ", MaxPreTaxProfit_production_cost
    print "    inventory_cost: ", inventory_cost
    print "    dealer_cost: ", MaxPreTaxProfit_dealer_cost
    print "    mkt_cost: ", mkt_cost
    print "=net_trading_profit: ", MaxPreTaxProfit_net_trading_profit 
    print "    -tool_depr_cost: ", tool_depr_cost
    print "    =gross_trading_profit: ", MaxPreTaxProfit_gross_trading_profit 
    print "-bank_interest_expense: ", MaxPreTaxProfit_bank_interest
    print "    current_expense: ", MaxPreTaxProfit_current_expense  
    print "-bond_interest: ", MaxPreTaxProfit_bond_interest
    print "=pretax_profit: ", MaxPreTaxProfit 
    print "----------------"
    print "dealer_qty: ", MaxPreTaxProfit_dealer_qty
    print "tools: ", MaxPreTaxProfit_tools
    print "unit direct_cost: ", MaxPreTaxProfit_direct_cost           
    print "unit direct_cost_w_disrpt: ", MaxPreTaxProfit_direct_cost_w_disrpt  
    print "unit_production_cost(incl tools): ", MaxPreTaxProfit_unit_production_cost
    print "production_change % : ", MaxPreTaxProfit_production_change_x
    print "disruption_ratio: ", MaxPreTaxProfit_disruption_ratio   
    print "unit_trading_cost: ", MaxPreTaxProfit_unit_trading_cost
    print "----------------"

    #return # bypass plot


    plt1 = pl.subplot(121)
    pl.plot(production_list, cost_of_production_list, label="Production cost")
    pl.plot(production_list, trading_cost_list, label="Trading cost")
    pl.plot(production_list, revenue_list, label="Revenue")
    pl.plot(production_list, net_trading_profit_list, label="Net trading profit")
    #pl.vlines(production_max, "r")
    pl.xlabel("Production",fontsize=14)
    pl.ylabel("Euros",fontsize=14)
    pl.grid(True)
    pl.legend(loc="best", fontsize = 10)
    #pl.setp(plt1.get_xticklabels(), visible=False)

#    plt2 = pl.subplot(512, sharex=plt1)
#    pl.plot(production_list, tool_num_list, "b", label="Optimal tool number")
#    pl.ylabel("Tool number",fontsize=14) #    pl.hlines(tool_owned_qty * 1.2, production_list[0], production_list[len(production_list)-1],"r")
#    pl.vlines(production_max, tool_num_list[0], tool_num_list[len(tool_num_list)-1],"r")
#    pl.grid(True)
#    pl.legend(loc="best", fontsize = 10)
#    pl.setp(plt2.get_xticklabels(), visible=False)

    plt2 = pl.subplot(122)
    pl.plot(production_list, unit_trading_cost_list, label="Unit trading cost")
    pl.xlabel("Production",fontsize=14)
    pl.ylabel("Unit trading cost",fontsize=14)
    pl.grid(True)
    pl.legend(loc="best", fontsize = 10)
    #pl.setp(plt3.get_xticklabels(), visible=False)

#    plt4 = pl.subplot(514, sharex=plt1)
#    pl.plot(production_list, revenue_list, label="Revenue")
#    pl.xlabel("Production",fontsize=14)
#    pl.ylabel("Revenue",fontsize=14)
#    pl.grid(True)
#    pl.legend(loc="best", fontsize = 10)
#    pl.setp(plt4.get_xticklabels(), visible=False)

#    plt4 = pl.subplot(425, sharex=plt1)
#    pl.plot(production_list, net_trading_profit_list, "g", label="Net trading profit")
#    #pl.vlines(production_max, "r")
#    pl.ylabel("Net trading profit",fontsize=14)
#    pl.grid(True)
#    pl.legend(loc="best", fontsize = 10)
##    #pl.setp(plt5.get_xticklabels(), visible=False)
 
    pl.show()
    #print cost_of_production_list

def f_production_plan():
    #f_optimize_production(70000,23000,662) # planner for Y6Q2
    #f_optimize_production(91000,23000,645) # planner for Y6Q3, TODO: chagne tools price
    #f_optimize_production(91000,23250,629) # planner for Y6Q4, Area2
    #f_optimize_production(100000,23250,488) # planner for Y6Q4, Area4
    #f_optimize_production(910000,22500,613) # planner for Y7Q1, Area2
    #f_optimize_production(100000,22500,475) # planner for Y7Q1, Area4
    #f_optimize_production(92045,23500,598) # planner for Y7Q2, Area2
    #f_optimize_production(100720,23500,464) # planner for Y7Q2, Area4

    #print "------ planner for Y7Q3, Area 2 ------"
    ##f_optimize_production(102080,22250,583,76.5,4906,40,400000,306819) 
    #print "------ planner for Y7Q3, Area 4 ------"
    ##f_optimize_production(107700,22250,502,76,0,42,400000,306819) 

    print "------ planner for Y7Q4, Area 2 ------"
    #f_optimize_production(107594,22750,668,75,0,45,400000,500000) 
    print "------ planner for Y7Q4, Area 4 ------"
    f_optimize_production(112500,22750,660,74.5,0,45,400000,500000) 

# Step 1: decide new production level
f_production_plan()

def f_mkt_regr(year):
    m = 0.4917*(year**3) - 2.6964*(year**2) + 5.1119*year - 1.46
    return m

def f_mkt_plan(year):
    m = f_mkt_regr(year)
    m_r = np.round(m, 3)
    #print "-----------------------------------------------"
    #print "\nmkting for year ", year, ": ", m_r, " million"
    magic_q1 = 3
    while (magic_q1<=6):
        q1 = np.round(f_mkt_regr(magic_q1), 2)
        q2 = np.round(f_mkt_regr(magic_q1+0.25), 2)
        q3 = np.round(f_mkt_regr(magic_q1+0.5), 2)
        q4 = np.round(f_mkt_regr(magic_q1+0.75), 2)
        ma = q1+q2+q3+q4
        if ma >= m_r:
            #print "\nsuggested per quarter mkting allocation for whole industry:"
            #print "q1: ", q1, " million"
            #print "q2: ", q2, " million"
            #print "q3: ", q3, " million"
            #print "q4: ", q4, " million"
            #print "all: ", ma, " million"
            #print "\nsuggested per firm per area mkting:"
            ## assume 1: all 14 backgound companies are in all areas
            ## assume 2: each area has two active companies, then 14+2 = 16
            ## assume 3: for more aggressive mkting, assume number of companies per area is 16-1=15
            q1a = int((q1/(15*4))*1000)
            q2a = int((q2/(15*4))*1000)
            q3a = int((q3/(15*4))*1000)
            q4a = int((q4/(15*4))*1000)
            #print "q1: ", q1a, " thousand"
            #print "q2: ", q2a, " thousand"
            #print "q3: ", q3a, " thousand"
            #print "q4: ", q4a, " thousand"

            #print "\tINDUSTRY (M)\t\t\t|\tA FIRM @ AN AREA (K)"
            #print "------------------------------------------------------------------------------"
            #print "q1\tq2\tq3\tq4\tall\t|\tq1\tq2\tq3\tq4"
            #print q1,"\t",q2,"\t",q3,"\t",q4,"\t",ma,"\t|\t",q1a,"\t",q2a,"\t",q3a,"\t",q4a

            break

        magic_q1 += 0.001 

    return (np.round(ma,2),q1,q2,q3,q4,q1a,q2a,q3a,q4a)

def f_mkt_plan_chart():
    print "==========================================================================================="
    print "YEAR\t|\t\tINDUSTRY (M)\t\t\t|\tA FIRM @ AN AREA (K)"
    print "-------------------------------------------------------------------------------------------"
    print "\t|\tall\tq1\tq2\tq3\tq4\t|\tq1\tq2\tq3\tq4"
    print "-------------------------------------------------------------------------------------------"
    year = 5
    while year < 9:
        (ma,q1,q2,q3,q4,q1a,q2a,q3a,q4a) = f_mkt_plan(year)
        ma = np.round(ma,2)
        q1 = np.round(q1,2)
        q2 = np.round(q2,2)
        q3 = np.round(q3,2)
        q4 = np.round(q4,2)
        print year,"\t|\t",ma,"\t",q1,"\t",q2,"\t",q3,"\t",q4,"\t|\t",q1a,"\t",q2a,"\t",q3a,"\t",q4a
        year += 1
    print "==========================================================================================="

#f_mkt_plan_chart()

