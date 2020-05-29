import os
import pandas as pd
from dateutil.parser import parse

def analytics(path, app):
    CVP_CALLS=[]
    CVP_CALLS_DT=[]
    CVP_CALLS_Value=[]
    for file in os.listdir (path):
        with open(os.path.join(path, file),'r',errors='ignore') as f:
            f_keys = ['STATS_ICM_ACTIVE_CALLS=','STATS_ICM_ACTIVE_VRU_LEGS=','STATS_SIP_ACTIVE_CALLS=',
                      'STATS_IVR_ACTIVE_CALLS=']
            for line in f.readlines():
                for word in f_keys:
                    try:
                        if word in line:
                            CVP_CALLS_DT.append(parse(line.split(word)[0].split(": ")[2].split('-')[0],fuzzy=True))
                            CVP_CALLS.append(word)
                            CVP_CALLS_Value.append(int(line.split(word)[1].split(',')[0]))
                    except:
                        print(line)
    CVP_cl={'CVP_CALLS_DT':CVP_CALLS_DT,'CVP_CALLS':CVP_CALLS,'CVP_CALLS_Value':CVP_CALLS_Value}
    df_cl=pd.DataFrame(CVP_cl)
    df_cl['CVP_CALLS_DT'] = df_cl['CVP_CALLS_DT'].apply(lambda dt: dt.timestamp()*1000)
    
    series = []
    SIP_Active=df_cl[df_cl['CVP_CALLS']=='STATS_SIP_ACTIVE_CALLS=']
    ICM_Active=df_cl[df_cl['CVP_CALLS']=='STATS_ICM_ACTIVE_CALLS=']
    ICM_VRU_Active=df_cl[df_cl['CVP_CALLS']=='STATS_ICM_ACTIVE_VRU_LEGS=']
    IVR_Active=df_cl[df_cl['CVP_CALLS']=='STATS_IVR_ACTIVE_CALLS=']
    SIP_Active = SIP_Active.drop(['CVP_CALLS'], axis=1)
    ICM_Active = ICM_Active.drop(['CVP_CALLS'], axis=1)
    ICM_VRU_Active = ICM_VRU_Active.drop(['CVP_CALLS'], axis=1)
    IVR_Active = IVR_Active.drop(['CVP_CALLS'], axis=1)
    series.append({"name": "SIP_Active", "data": SIP_Active.to_numpy().tolist()})
    series.append({"name": "ICM_Active", "data": ICM_Active.to_numpy().tolist()})
    series.append({"name": "ICM_VRU_Active", "data": ICM_VRU_Active.to_numpy().tolist()})
    series.append({"name": "IVR_Active", "data": IVR_Active.to_numpy().tolist()})

    return series