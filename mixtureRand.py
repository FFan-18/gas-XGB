import random as rd
import pandas as pd
from multiprocessing import Pool,cpu_count
from hapi import *
db_begin('datamix')
fetch_by_ids('10mix',[7,21,26,39,42,44,51,52,70,114],1300,4300)
generate_times = 4
amount_per_generate = 500
#
def generate_gas(start_index,generate_amount):
    df = pd.DataFrame(columns=['id','conc','nu','coef'])
    for i in range(generate_amount):
        cCO2 = rd.uniform(0.1, 0.2)
        cN2O = rd.uniform(0, (1E-5))
        cCO = rd.uniform(0, (1.6E-3))
        cNO = rd.uniform(0, (1E-5))
        cSO2 = rd.uniform(0, (2E-3))
        cNO2 = rd.uniform(0, (1E-3))
        cHF = rd.uniform(0, (1.2E-6))
        cHCl = rd.uniform(0, (1.3E-5))
        cHCN = rd.uniform(0, (2E-6))
        cSO3 = rd.uniform(0, (1.7E-5))
        df.loc[i,'id'] = start_index + i
        df.loc[i,'conc'] = [cCO2,cN2O,cCO,cNO,cSO2,cNO2,cHF,cHCl,cHCN,cSO3]
        df.loc[i, 'nu'], df.loc[i, 'coef'] = absorptionCoefficient_Lorentz(SourceTables='10mix',HITRAN_units = False, OmegaStep = 0.1,Components = [(2,1,cCO2),(4,1,cN2O),
            (5,1,cCO),(8,1,cNO),(9,1,cSO2),(10,1,cNO2),(14,1,cHF),(15,1,cHCl),(23,1,cHCN),(47,1,cSO3)],Diluent={'self': (cCO2+cN2O+cNO+cNO2+cSO2+cCO+cHCl+cHF+cHCN+cSO3),'air':(1.0-cCO2-cN2O-cNO-cNO2-cSO2-cCO-cHCl-cHF-cHCN-cSO3)})

    return df

if __name__ == "__main__":
    start_index_list = [amount_per_generate * i for i in range(generate_times)]
    generate_amount_list = [amount_per_generate] * generate_times
    process_pool = Pool(4)
    all_dfs = process_pool.starmap(generate_gas,zip(start_index_list,generate_amount_list))
    full_df = pd.concat(all_dfs,axis=0,ignore_index=True)
    full_df.to_csv('10mix_result_false.csv')
    full_df.to_pickle('10mix_result_false.pickle')