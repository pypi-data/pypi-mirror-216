import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import os
import json

def save_model_to_json(filepath, filename, clf, scalers=dict()):
    """
    Write a json file to be used in Maingo / Melon
    return None
    """
    prediction_parameters = dict()
    prediction_parameters["rho"] = np.asscalar(clf.intercept_)
    prediction_parameters["support_vectors"] = clf.support_vectors_.tolist()
    prediction_parameters["dual_coefficients"] = clf.dual_coef_.ravel().tolist()
    prediction_parameters["kernel_parameters"] = [clf._gamma]
    prediction_parameters["kernel_function"] = clf.kernel

    prediction_parameters["scaling"] = dict()
    for var, scaler in scalers.items():
        if scaler is not None:
            if isinstance(scaler, MinMaxScaler):
                prediction_parameters["scaling"][var] = {
                    "scaler": "MinMax",
                    "min": scaler.data_min_.tolist(),
                    "max": scaler.data_max_.tolist()
                }    
            elif isinstance(scaler, StandardScaler):
                prediction_parameters["scaling"][var] = {
                    "scaler": "Standard",
                    "mean": scaler.mean_.tolist(),
                    "stddev": np.sqrt(scaler.var_).tolist()
                }
            else:
                raise TypeError("Can only write parameters for scalers of type 'MinMaxScaler' and 'StandardScaler' to JSON file.")
        else:
            prediction_parameters["scaling"][var] = {"scaler": "Identity"}

    if not os.path.exists(filepath):
        os.makedirs(filepath)
    
    with open(os.path.join(filepath,filename), 'w') as outfile:
        json.dump(prediction_parameters, outfile)
