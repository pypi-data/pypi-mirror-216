"""Main function
"""
from .main import formOsteoAdata, lineagePredict, pseduo_predict, pseduo_traj,integrateTrajMap, calculate_posterior

import os

location = os.path.dirname(os.path.realpath(__file__))
highVarGeneFile = os.path.join(location, 'dataset', 'variable_2000.csv')