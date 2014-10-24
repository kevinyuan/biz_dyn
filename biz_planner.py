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
    production_change = float(production) / float(production_prev)
    if (production_change > 1.3):
        #print "warning: production_change > 1.3 : ", production_change
        sys.exit(1)
    disruption_ratio = 0.83*production_change**2-1.125* production_change+1.2542 
    direct_cost = 257.29 * ((production/1000)**0.0942) * (total_tool_qty**(-0.3425)) 
    direct_cost_w_disrpt = direct_cost * disruption_ratio  
    #print "production_change: ", production_change  
    #print "disruption_ratio: ", disruption_ratio
    #print "direct_cost: ",  direct_cost
    #print "direct_cost_w_disrpt: ",  direct_cost_w_disrpt
    return direct_cost

def f_mkt_cost(sales, price, gnp):
    mkt_cost = (sales + 2.578*107 + 1095.4160 * price - 2.652*105 * gnp) / 0.1533       
    #print "mkt_cost: ", mkt_cost
    return mkt_cost

def f_trading_cost(ship_cost, dealer_cost):
    trading_cost = ship_cost + dealer_cost 
    #print "trading_cost: ", trading_cost
    return trading_cost

def f_ship_cost(ship_qty):
    if (ship_qty >= 1000000):
        ship_cost = ship_qty * 4
    else:
        ship_cost = ship_qty * 8
    #print "ship_cost: ", ship_cost
    return ship_cost

def f_dealer_cost(sales):
    dealer_qty = np.ceil(sales / 2500)
    dealer_cost = dealer_qty * 30000
    #print "dealer_qty: ", dealer_qty
    #print "dealer_cost: ", dealer_cost
    return dealer_cost

def f_tool_cost(tool_price, tool_owned_qty, tool_buy_qty, tool_hire_qty):
    tool_hire_cost = 2000 * tool_hire_qty
    tool_buy_cost = tool_price * tool_buy_qty
    tool_depr_cost = tool_owned_qty * tool_price * 2.5/100
    tool_cost = tool_hire_cost + tool_buy_cost + tool_depr_cost
    #print "tool_hire_cost :",  tool_hire_cost 
    #print "tool_buy_cost :",   tool_buy_cost  
    #print "tool_depr_cost :",  tool_depr_cost 
    #print "tool_cost :",  tool_cost 
    return tool_cost

def f_pretax_profit(trading_profit, bank_interest_rec, bank_interest_pay, bond_interest):
    pretax_profit  = trading_profit + bank_interest_rec - bank_interest_pay - bond_interest   
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

def f_when_hire_tool_1(production, production_prev, tool_price, tool_owned_qty):
    cost_of_production_list = []
    num_of_tool_list = []
    tool_hire_qty = 0
    total_tool_qty = tool_owned_qty 
    while (total_tool_qty <= 2000):
    #while (total_tool_qty <= 662):
        total_tool_qty  = tool_owned_qty + tool_hire_qty
        direct_cost = f_direct_cost(production, production_prev, total_tool_qty)
        tool_cost = f_tool_cost(tool_price, tool_owned_qty, 0, tool_hire_qty)
        cost_of_production = int(direct_cost*production+tool_cost)
        tool_hire_qty += 10
        num_of_tool_list.append(total_tool_qty)
        #print "-------- num_of_tool: ", total_tool_qty, " ---------"
        cost_of_production_list.append(cost_of_production)
        #print "-------- cost_of_production: ", cost_of_production, " ---------"
    pl.plot(num_of_tool_list, cost_of_production_list)
    pl.show()
    #print cost_of_production_list

#f_when_hire_tool_1(91000,70000,23000,662)
#f_when_hire_tool_1(118000,91000,23000,662)
#f_when_hire_tool_1(200000,154000,23000,662)

def f_when_hire_tool(tool_price):

    pl.figure(figsize=(38,37),dpi=98)
    pl.close("all")
    f, p = pl.subplots(4,4) 
    f.subplots_adjust(hspace=0.6)
    f.subplots_adjust(wspace=0.3)

    tool_hire_qty = 0
    production = 50000
    i = 0
    while (production <= 200000):
    #while (production <= 60000):
        tool_owned_qty = 400

        cost_delta_list = []
        num_of_tool_list = []

        while (tool_owned_qty < 2000):

            # cost with tool_owned_qty 
            tool_hire_qty = 0
            total_tool_qty  = tool_owned_qty + tool_hire_qty
            direct_cost = f_direct_cost(production, production*1.1, total_tool_qty)
            tool_cost = f_tool_cost(tool_price, tool_owned_qty, 0, tool_hire_qty)
            cost_of_production = int(direct_cost*production+tool_cost)

            # cost with tool_owned_qty + tool_hire_qty
            tool_hire_qty = 10 
            total_tool_qty  = tool_owned_qty + tool_hire_qty
            direct_cost = f_direct_cost(production, production*1.1, total_tool_qty)
            tool_cost = f_tool_cost(tool_price, tool_owned_qty, 0, tool_hire_qty)
            cost_of_production_new = int(direct_cost*production+tool_cost)

            # compare costs
            cost_delta = cost_of_production_new - cost_of_production
            num_of_tool_list.append(tool_owned_qty)
            #print "-------- num_of_tool: ", tool_owned_qty, " -> ", total_tool_qty, " ---------"
            cost_delta_list.append(cost_delta)
            #print "-------- cost_delta: ", cost_delta, " ---------"

            tool_owned_qty += 50

        print "production:", production
        x = i % 4
        y = i / 4
        #print " i: " , i, " x: ", x, " y: ", y

        lb = "Production: " + str(production)

        p[y, x].plot(num_of_tool_list, cost_delta_list, label=lb)
        p[y, x].xaxis.set_tick_params(labelsize=8)
        p[y, x].yaxis.set_tick_params(labelsize=8)
        p[y, x].hlines(0, num_of_tool_list[0], num_of_tool_list[31],"r")
        p[y, x].set_title(lb, fontsize = 9)
        p[y, x].set_xlabel("Number of tools", fontsize = 8)
        p[y, x].set_ylabel("Cost", fontsize = 8)
        p[y, x].grid(True)
        #p[y, x].legend(loc="best", fontsize = 8)

        production+=10000
        i = i + 1
    pl.show()


f_when_hire_tool(23000)

def f_optimize_production(production_prev, tool_price, tool_owned_qty):
    production_list = []
    cost_of_production_list = []
    trading_cost_list = []
    production_change = 1.01 
    total_tool_qty = tool_owned_qty 
    while (production_change <= 1.3):
        production = production_prev*production_change
        production_list.append(production)
        #print "-------- production: ", production, " ---------"

        direct_cost = f_direct_cost(production, production_prev, total_tool_qty)
        tool_cost = f_tool_cost(tool_price, tool_owned_qty, 0, 0)
        cost_of_production = int(direct_cost*production+tool_cost)
        cost_of_production_list.append(cost_of_production)
        #print "-------- cost_of_production: ", cost_of_production, " ---------"

        trading_cost = cost_of_production + f_dealer_cost(production) # assume no shipment
        trading_cost_list.append(trading_cost)
        #print "-------- trading_cost: ", trading_cost, " ---------"

        production_change += 0.1
    pl.plot(production_list, cost_of_production_list, "g", label="Production cost")
    pl.plot(production_list, trading_cost_list, "r", label="Trading cost")
    #pl.axis([0.0,5.01,-1.0,1.5])
    pl.xlabel("Production",fontsize=14)
    pl.ylabel("Cost",fontsize=14)
    pl.title("Cost vs production curve",fontsize=18)
    pl.grid(True)
    pl.legend(loc="best")
    pl.show()
    #print cost_of_production_list

#f_optimize_production(70000,23000,662) # planner for Y6Q2
#f_optimize_production(91000,23000,645) # planner for Y6Q3, TODO: chagne tools price


