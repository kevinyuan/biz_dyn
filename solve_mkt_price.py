from sympy import solve
from sympy.abc import s, p, m, g

import numpy as np
import pylab as pl

sel = input("select solver: \n\t1: marketing\n\t2: price\n\t3: sales\n\t4: gnp\n\t5: marketing vs price\n?")
print sel
if sel == 1:
    g = input("gnp:")
    s = input("sales:")
    p = input("price:")
    mkting = solve(-2.578*(10**7)-1095.4160*p+0.1533*m+2.652*(10**5)*g-s, m, rational=True)
    print ("mkting:" , int(mkting[0]))
elif sel == 2:
    g = input("gnp:")
    s = input("sales:")
    m = input("mkting:")
    price = solve(-2.578*(10**7)-1095.4160*p+0.1533*m+2.652*(10**5)*g-s, p, rational=True)
    print ("price:" , int(price[0]))
elif sel == 3:
    g = input("gnp:")
    p = input("price:")
    m = input("mkting:")
    sales = solve(-2.578*(10**7)-1095.4160*p+0.1533*m+2.652*(10**5)*g-s, s, rational=True)
    print ("sales:", int(sales[0]))
elif sel == 4:
    p = input("price:")
    s = input("sales:")
    m = input("mkting:")
    gnp = solve(-2.578*(10**7)-1095.4160*p+0.1533*m+2.652*(10**5)*g-s, g, rational=True)
    print ("gnp:", int(gnp[0]))
elif sel == 5:
    g = input("gnp:")
    s = input("sales:")
    pa = np.linspace(40, 100, 61)
    a = np.linspace(1, 1, 61)
    ga = a*g
    sa = a*s
    ma = []
    for i in range(len(pa)):
        p = int(pa[i])
        s = int(sa[i])
        g = int(ga[i])
        xm = solve(-2.578*(10**7)-1095.4160*p+0.1533*m+2.652*(10**5)*g-s, m, rational=True)
        ma.append(int(xm[0]))
    print ("mkting:" , ma)
    pl.plot(pa, ma)
    pl.show()
else:
    print ("unknown option", sel)

