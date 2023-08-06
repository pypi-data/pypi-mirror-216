import scanpy as sc
import anndata
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import scvi
import scarches as sca
import tensorflow as tf
from scipy.stats import pearsonr
import anndata as ad
from scipy.stats import ttest_ind
from scipy.stats import norm

def lineagePredict(adata,chondroPath,mesPath,leprPath,max_epoch=100):
    #= predict chondro lineage
    print("predicting chondro path")
    model_chondro = sca.models.SCANVI.load_query_data(
        adata,
        chondroPath,
        freeze_dropout = True,
    )
    model_chondro.train(
        max_epochs=max_epoch,
        plan_kwargs=dict(weight_decay=0.0),
        check_val_every_n_epoch=10
    )
    adata.obs["chondro_prediction"]=model_chondro.predict()
    print("predicting lepr path")
    model_lepr = sca.models.SCANVI.load_query_data(
        adata,
        leprPath,
        freeze_dropout = True,
    )
    model_lepr.train(
        max_epochs=max_epoch,
        plan_kwargs=dict(weight_decay=0.0),
        check_val_every_n_epoch=10
    )
    adata.obs["lepr_prediction"]=model_lepr.predict()
    print("predicting mes/fibro path")
    model_mes = sca.models.SCANVI.load_query_data(
        adata,
        mesPath,
        freeze_dropout = True,
    )
    model_mes.train(
        max_epochs=max_epoch,
        plan_kwargs=dict(weight_decay=0.0),
        check_val_every_n_epoch=10
    )
    adata.obs["mes_prediction"]=model_mes.predict()
    return(adata)


