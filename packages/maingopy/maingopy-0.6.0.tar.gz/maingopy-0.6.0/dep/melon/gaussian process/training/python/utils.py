import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import os
import json
import pymelon
import torch

def generate_melon_scaler_object(scaler):
        scaler_data = pymelon.ScalerData()
        
        if scaler is None:
            scaler_data = pymelon.SCALER_TYPE.IDENTITY
            scaler_data.parameters = {}
        elif isinstance(scaler, MinMaxScaler):
            scaler_data.type = pymelon.SCALER_TYPE.MINMAX
            
            scaled_bounds = scaler.get_params()['feature_range']
            scaler_data.parameters = {
                pymelon.SCALER_PARAMETER.UPPER_BOUNDS : scaler.data_max_.tolist(),
                pymelon.SCALER_PARAMETER.LOWER_BOUNDS : scaler.data_min_.tolist(),
                pymelon.SCALER_PARAMETER.SCALED_LOWER_BOUNDS : [scaled_bounds[0]]*len(scaler.data_max_.tolist()), 
                pymelon.SCALER_PARAMETER.SCALED_UPPER_BOUNDS : [scaled_bounds[1]]*len(scaler.data_max_.tolist())
            }
        elif isinstance(scaler, StandardScaler):
            scaler_data.type = pymelon.SCALER_TYPE.STANDARD          
            scaler_data.parameters = {
                pymelon.SCALER_PARAMETER.STD_DEV : np.sqrt(scaler.var_).tolist(),
                pymelon.SCALER_PARAMETER.MEAN : scaler.mean_.tolist()
            }
        else:
            raise Exception("Unsupported scaler type. Scaler has to be either a scikit-learn MinMaxScaler or StandardScaler instance or None (=identity(no scaling))")
        
        return scaler_data 

def generate_melon_gp_object(GP_model, X, y, matern, scaler):
    gp_data = pymelon.GPData()
    
    gp_data.X = X.numpy()
    gp_data.Y = y.numpy()

    gp_data.nX, gp_data.DX = X.shape

    if len(y.shape) == 1:
        gp_data.DY = y.shape[0]
    else:
        gp_data.DY = y.shape[1]

    cov_mat = GP_model.covar_module(X)
    gp_data.K = cov_mat.numpy() 
    inv_cov_mat = torch.inverse(cov_mat.evaluate())
    gp_data.invK = inv_cov_mat.detach().numpy()

    gp_data.matern = matern
    kernel_data = pymelon.KernelData()
    kernel_data.sf2 = GP_model.covar_module.outputscale.detach().numpy().astype(float).item()               #outputscale sigma*K
    kernel_data.ell = GP_model.covar_module.base_kernel.lengthscale.detach().numpy().squeeze().tolist()     #lenghtscales kernel
    gp_data.kernelData = kernel_data

    if not 'input' in scaler:
        scaler['input'] = None
    gp_data.inputScalerData = generate_melon_scaler_object(scaler['input'])


    if not 'output' in scaler or not isinstance(scaler['output'], StandardScaler):
        raise Exception('The output scaler has to be as scikit-learn StandardScaler instance')   

    gp_data.predictionScalerData = generate_melon_scaler_object(scaler['output'])

    gp_data.stdOfOutput = np.sqrt(scaler['output'].var_)[0]
    gp_data.meanFunction = 0

    return gp_data


def save_model_to_json(filepath, filename, GP_model, X, y, matern, scalers=dict()):
    prediction_parameters = dict()
    prediction_parameters["nX"] = X.shape[0]
    prediction_parameters["DX"] = X.shape[1]

    if len(y.shape) == 1:
        prediction_parameters["DY"] = y.shape[0]
    else:
        prediction_parameters["DY"] = y.shape[1]

    prediction_parameters["matern"] = matern
    prediction_parameters["meanfunction"] = 0
    prediction_parameters["X"] = X.numpy().tolist()
    prediction_parameters["Y"] = y.numpy().tolist()

    cov_mat = GP_model.covar_module(X)
    prediction_parameters["K"] = cov_mat.numpy().tolist()
    prediction_parameters["invK"] = np.linalg.inv(prediction_parameters["K"]).tolist()

    if not 'input' in scalers or not isinstance(scalers['input'], MinMaxScaler):
        raise Exception("There has to be an inputscaler which is a scikit-learn MinMaxScaler instance")

    prediction_parameters["problemLowerBound"] = scalers['input'].data_min_.tolist()
    prediction_parameters["problemUpperBound"] = scalers['input'].data_max_.tolist()
    
    if not 'output' in scalers or not isinstance(scalers['output'], StandardScaler):
        raise Exception("There has to be an output scaler which is a scikit-learn StandardScaler instance")
    
    prediction_parameters["stdOfOutput"] = np.sqrt(scalers['output'].var_).item()
    prediction_parameters["meanOfOutput"] = scalers['output'].mean_.item()

    prediction_parameters["sf2"] = GP_model.covar_module.outputscale.detach().numpy().astype(float).item()           #outputscale sigma*K
    prediction_parameters["ell"] = GP_model.covar_module.base_kernel.lengthscale.detach().numpy().squeeze().tolist()     #lenghtscales kernel

    if not os.path.exists(filepath):
        os.makedirs(filepath)
    
    with open(os.path.join(filepath,filename), 'w') as outfile:
        json.dump(prediction_parameters, outfile)
