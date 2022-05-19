import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hapi import *
# df = pd.read_pickle("10mix_result_false.pickle")
# nu = df.loc[1, 'nu']
# coef =df.loc[1,'coef']
# nu, absorp = absorptionSpectrum(nu, coef)
# nu_, absorp_, i1, i2, slit = convolveSpectrum(nu, absorp, Resolution=0.25, AF_wing=10) #res小于AF*2
# plt.figure(figsize=(9,6))
# plt.xlim((1300, 4300))
# plt.xlabel('Wavenumber/cm-1')
# plt.title('Absorption Spectrum (Resolution=0.25)')
# plt.plot(nu_,absorp_,color='skyblue')
# plt.show()

df1 = pd.DataFrame(columns=['id','conc','nu','absorp'])
for i in range(2000):
    df1.loc[i,'conc'] = df.loc[i,'conc']
    nu = df.loc[i, 'nu']
    coef =df.loc[i,'coef']
    nu, absorp = absorptionSpectrum(nu, coef)
    nu_, absorp_, i1, i2, slit = convolveSpectrum(nu, absorp, Resolution=20, AF_wing=10)
    df1.loc[i, 'nu'], df1.loc[i, 'absorp'] = nu, absorp
    df1.loc[i, 'id'] = i
# df1.to_csv('10mix_absorp_ori.csv')
df1.to_pickle('10mix_absorp_false_res=20.pickle')

# dff=df.loc[0:100]
# dff.to_pickle('100.pickle')

