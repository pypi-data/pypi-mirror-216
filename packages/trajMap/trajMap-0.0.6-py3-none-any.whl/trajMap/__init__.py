"""Main function
"""
from .main import formOsteoAdata, lineagePredict, pseduo_predict, pseduo_traj,integrateTrajMap, calculate_posterior

import os

location = os.path.dirname(os.path.realpath(__file__))
highVarGeneFile = os.path.join(location, 'dataset', 'variable_2000.csv')
trajMapFile=os.path.join(location, 'dataset', 'trajMap_reference_1.h5ad')
scanviMesFile=os.path.join(location, 'dataset', "scanvi_mes")
scanviLeprFile=os.path.join(location, 'dataset', "scanvi_lepr")
scanviChondroFile=os.path.join(location, 'dataset', "scanvi_chondro")
pseduoPredFile=os.path.join(location, 'dataset', "pseduoPred")