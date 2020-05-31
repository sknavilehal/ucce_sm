import os
import pandas as pd
from dateutil.parser import parse
from bokeh.palettes import Viridis4
from bokeh.plotting import figure, show
from bokeh.models.annotations import Title, Legend

def preprocess(path):
    CVP_CALLS_DT=[]
    CVP_CALLS=[]
    CVP_CALLS_Value=[]
    for file in os.listdir (path):
        with open (os.path.join(path, file),'r',errors='ignore') as f:
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
                        continue
    CVP_cl={'CVP_CALLS_DT':CVP_CALLS_DT,'CVP_CALLS':CVP_CALLS,'CVP_CALLS_Value':CVP_CALLS_Value}
    df_cl=pd.DataFrame(CVP_cl)

    SIP_Active=df_cl[df_cl['CVP_CALLS']=='STATS_SIP_ACTIVE_CALLS=']
    ICM_Active=df_cl[df_cl['CVP_CALLS']=='STATS_ICM_ACTIVE_CALLS=']
    ICM_VRU_Active=df_cl[df_cl['CVP_CALLS']=='STATS_ICM_ACTIVE_VRU_LEGS=']
    IVR_Active=df_cl[df_cl['CVP_CALLS']=='STATS_IVR_ACTIVE_CALLS=']

    return (SIP_Active, ICM_Active, ICM_VRU_Active, IVR_Active)

def make_plot(data):
    SIP_Active,ICM_Active,ICM_VRU_Active,IVR_Active = data

    p = figure(x_axis_type='datetime',plot_height=250, plot_width=900)
    aline = p.line(SIP_Active['CVP_CALLS_DT'], SIP_Active['CVP_CALLS_Value'], line_width=2, color=Viridis4[0])
    bline = p.line(ICM_Active['CVP_CALLS_DT'], ICM_Active['CVP_CALLS_Value'], line_width=2, color=Viridis4[1])
    cline = p.line(ICM_VRU_Active['CVP_CALLS_DT'], ICM_VRU_Active['CVP_CALLS_Value'],line_width=2, color=Viridis4[2])
    dline = p.line(IVR_Active['CVP_CALLS_DT'], IVR_Active['CVP_CALLS_Value'], line_width=2, color=Viridis4[3])

    p.yaxis.axis_label = 'Call Count'
    p.xaxis.axis_label = 'Time'

    legend1 = Legend(items=[
        ("SIP_Active",   [aline]),
        ("ICM_Active", [bline]),
        ("ICM_VRU_Active", [cline]),
        ("IVR_Active", [dline])
    ], location=("center"))

    p.add_layout(legend1, 'left')

    return p