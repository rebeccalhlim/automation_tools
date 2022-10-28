import pandas as pd
import numpy as np
import empyrical as empy

import matplotlib.pyplot as plt
import seaborn as sns


long_path = r'C:\Stuff\AML\codes\coding_projects\test123\automation_tools\output' + '\\'

def empy_metric(ret):
    if isinstance(ret, pd.DataFrame):
        return ret.apply(empy_metric).T
    total_return = lambda x: (1+x).prod()-1
    met_func = [total_return, empy.annual_return, empy.sharpe_ratio, empy.annual_volatility, empy.max_drawdown]
    
    if ret.name not in ['Growth','Mod','FICon','Con']:
        ret_clean = ret[ret!=0]
        if str(ret_clean.index[0])[:10]!='2008-01-02':
            print('{} start at {}'.format(ret.name, str(ret_clean.index[0])[:10]))
        if str(ret_clean.index[-1])[:10]!='2021-05-28':
            print('{} end at {}'.format(ret.name, str(ret_clean.index[-1])[:10]))
    else:
        ret_clean = ret.copy()
    
    return pd.Series([f(ret_clean) for f in met_func], 
                    ['total_return', 'annual_return', 'sharpe_ratio', 'annual_volatility', 'max_drawdown'])

def print_clustermap(data, title=''):
    
    #corr = data.corr()
    data_clean = data.applymap(lambda x: x if x!=0 else np.nan)
    for n in ['Growth','Mod','FICon','Con']:
        data_clean[n] = data_clean[n].fillna(0)
    corr = data_clean.corr()
    
    g = sns.clustermap(corr, method="complete", cmap='PuOr', annot=True, 
                   annot_kws={"size": 10}, vmin=-1, vmax=1, figsize=(8,8))
    g.fig.suptitle(title)
    plt.show()

def generate(name_list, file_list):
    ret_list = []
    for f in file_list:
        ret_ = pd.read_excel(f, sheet_name='KPI(Daily)', index_col=0)['Daily Return']
        ret_list.append(ret_)
    ret = pd.concat(ret_list, 1, keys=name_list)
    ret.index = pd.to_datetime(ret.index)
    #ret
    a = empy_metric(ret)
    print(a)
    a.to_csv(long_path + 'a.csv')
