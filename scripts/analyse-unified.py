import os
import sys
import core
import glob
import yaml
import joblib
import itertools
import numpy as np
import pandas as pd
from analyse import aname, bname
import scipy.spatial.distance as dst

dirname = os.path.dirname(__file__)

def heatmap(data, x='GB', y='CB', centered=False, init=False):
    matrix = []
    for (m1, g1), mgdata1 in data.groupby(level=['motif', 'gap']):
        for (m2, g2), mgdata2 in data.groupby(level=['motif', 'gap']):
            proj_from = mgdata1.loc[m1, g1, x].projections
            proj_to = mgdata2.loc[m2, g2, y].projections
            distances = np.array([dst.euclidean(
                proj_from[t, :],
                proj_to[t, :]
            ) for t in np.arange(min(proj_from.shape[0], proj_to.shape[0]))])
            matrix.append({
                'from_m': m1,
                'from_g': g1,
                'to_m': m2,
                'to_g': g2,
                'dist': distances[0] if init else distances.mean()
            })
    heatmatrix = pd.DataFrame(matrix).set_index(['from_m', 'from_g', 'to_m', 'to_g']).unstack(['to_m', 'to_g'])
    return heatmatrix

def export(df, exp, tag):
    export_data = df.stack([1,2], future_stack=True).reset_index(drop=False)
    export_data['same_CI'] = export_data.apply(
        lambda row: (row.from_m==row.to_m)&(row.from_g==row.to_g),
        axis=1)
    export_data['exp'] = exp
    export_data['GB_to'] = tag
    return export_data


win=100
nbasis=15
for exp, dataset in [('nat8b','cohort'), ('nat8a','alpha'), ('nat8a','beta'), ('synth8b','cohort')]:
    print(exp, dataset)
    stim_info = pd.read_csv(os.path.join(dirname, f"../inputs/stimuli/{exp}-info.csv"))
    spectrograms = pd.read_csv(os.path.join(dirname, f"../build/{exp}/spectrograms.csv"), index_col=[0,1])
    motifs = stim_info.motif.unique()

    if exp in ['nat8b','synth8b']:
        namefn = bname
        gaps = stim_info[stim_info.type=='G'].groupby(['motif','gap']).first()[['gap_start', 'gap_stop']]
        gaplocs = gaps.index.levels[1].to_numpy().astype(int)
        dsetdata = []
        for h5file in glob.glob(os.path.join(dirname, f"../build/{exp}/**_delemb_win{win}_basis{nbasis}.h5")):
            dsetdata.append(pd.read_hdf(h5file, key='Induction'))
        responses = pd.concat(dsetdata, axis=1)
    else:
        namefn = aname
        gaps = stim_info[stim_info.type=='gap'].groupby(['motif','gap']).first()[['gap_start', 'gap_stop']]
        gaplocs = gaps.index.levels[1].to_numpy().astype(int)
        responses = pd.read_hdf(
            os.path.join(dirname, f"../build/{exp}/{dataset}_delemb_win{win}_basis{nbasis}.h5"),
            key="Induction")    

    models = joblib.load(os.path.join(dirname, f"../output/{exp}/{dataset}_PLS_models.pkl"))
    model = models['all']
    
    projections = []
    for m in motifs:
        cstim = spectrograms.loc[namefn(m, 'C', None)]
        for g in gaplocs:
            ga, gb = gaps.loc[m].loc[g].astype(int)
            for c in ['C','CB','GB','N']:
                stim = namefn(m, c, g)
                X = model.transform(
                    X = responses.loc[stim].loc[ga:gb]
                )
                projections.append({'motif': m,
                                    'gap': g,
                                    'condition': c,
                                    'projections': X})
    result = pd.DataFrame(projections).set_index(['motif', 'gap', 'condition'])
    GBC = heatmap(result, 'GB', 'C', centered=False)
    GBCB = heatmap(result, 'GB', 'CB', centered=False)
    
    pd.concat([
        export(GBC, exp, 'C'),
        export(GBCB, exp, 'CB'),
    ]).to_csv(os.path.join(dirname, f'../output/pairwise-{exp}-{dataset}-unified.csv'))