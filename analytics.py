import os
import json
import pandas as pd
from dateutil.parser import parse

def analytics(path):
    f_keys = {'STATS_ICM_ACTIVE_CALLS=':[],'STATS_ICM_ACTIVE_VRU_LEGS=':[],'STATS_SIP_ACTIVE_CALLS=':[], 'STATS_IVR_ACTIVE_CALLS=':[]}
    licenses ={'STATS_RT_PORT_LICENSES_IN_USE=':[], 'STATS_RT_PORT_LICENSES_AVAILABLE=':[]}
    application={'application=':[]}
    for file in os.listdir (path):
        with open (os.path.join(path, file),'r',errors='ignore') as f:
            for line in f.readlines():
                for word in f_keys.keys():
                    try:
                        if word in line:
                            x = parse(line.split(word)[0].split(": ")[2].split('-')[0],fuzzy=True)
                            y = int(line.split(word)[1].split(',')[0])
                            f_keys[word].append([x.timestamp()*1000, y])
                    except:
                        print("error")
                for word in licenses.keys():
                    if word in line:
                        x = parse(line.split(word)[0].split(": ")[2].split('-')[0],fuzzy=True)
                        y = int(line.split(word)[1].split(",")[0].split('}][')[0])
                        licenses[word].append([x.timestamp()*1000, y])
                for word in application.keys():
                    if word in line:
                        if ";" in line:
                            application[word].append(line.split(word)[1].split(';')[0])
                        else:
                            application[word].append(line.split(word)[1].split(',')[0])
    calls_series = []
    licenses_series = []
    App_series = pd.DataFrame(application)
    calls_series.append({"name":"SIP_Active", "data": sorted(f_keys["STATS_SIP_ACTIVE_CALLS="], key=lambda x: x[0])})
    calls_series.append({"name":"ICM_Active","data": sorted(f_keys["STATS_ICM_ACTIVE_CALLS="], key = lambda x: x[0])})
    calls_series.append({"name":"ICM_VRU_Active", "data": sorted(f_keys["STATS_ICM_ACTIVE_VRU_LEGS="], key = lambda x: x[0])})
    calls_series.append({"name": "IVR_Active", "data": sorted(f_keys["STATS_IVR_ACTIVE_CALLS="], key = lambda x: x[0])})

    licenses_series.append({"name": "CVP_License_InUse", "data": sorted(licenses["STATS_RT_PORT_LICENSES_IN_USE="], key = lambda x: x[0])})
    licenses_series.append({"name": "CVP_License_Available", "data": sorted(licenses["STATS_RT_PORT_LICENSES_AVAILABLE="], key = lambda x: x[0])})
    
    application_series = App_series.pivot_table(index=['application='], aggfunc='size')

    return (calls_series, licenses_series,application_series)