%%
%  @file example_training_of_GP.m
%
%  @brief Illustrative training script for Gaussian processes in Matlab.
%
% ==============================================================================\n
%   Aachener Verfahrenstechnik-Systemverfahrenstechnik, RWTH Aachen University  \n
% ==============================================================================\n
%
%  @author Artur Schweidtmann, Xiaopeng Lin, Daniel Grothe, and Alexander Mitsos
%  @date 16. January 2020

%%

clc
clear all
close all

addpath("Direct");           % Add path for DIRECT solver
addpath("GP training");      % Add path for Gaussian process training functions
addpath("Write GP to files");% Add path for Gaussian process export functions


%% General
nX = 20;                    % Number of training data points
DX = 2;                     % Input dimension of data / GP

lb = [-3, -3];              % Define Lower bound of inputs
ub = [ 3,  3];              % Define upper bound of inputs

test_func = @(x) 3*(1-x(1)).^2.*exp(-(x(1).^2) - (x(2)+1).^2) ... 
   - 10*(x(1)/5 - x(1).^3 - x(2).^5).*exp(-x(1).^2-x(2).^2) ... 
   - 1/3*exp(-(x(1)+1).^2 - x(2).^2) ; % Function for data generation


%% Generate training data

X = lhsdesign(nX,DX);       % Generate inputs using a Latin hypercube
X = lb + (ub-lb) .* X ;     % Scale inputs onto interval [lb, ub]

Y = cellfun(test_func, num2cell(X,2)); % Evaluate test_func for all X


%% Tranining of GPs
Opt.GP(1).matern = 5 ;          % Define covariance function Martern 1, 3, 5, inf
Opt.GP(1).fun_eval = 200;       % internal option for solver

Opt = Train_GP_and_return_hyperparameters(X,Y,lb,ub,Opt) ; % Training of GP


%% Save GP parameters in json file
% We write a json-file that is read by our MAiNGO model.
filename = "GP_Parameters" ; 
Write_GP_to_json(join([filename, ".json"]), Opt.GP(1), X, Y, lb, ub);


%% Compute GP predictions in Matlab (just for information) 
x_Test_Point = [1.5, 2] ;
[ prediction, std ] = Predict_GP(x_Test_Point, X, Y, lb, ub, Opt.GP ) ;


%% Plot generated data (just for information) 

% Generate a mesh on the inputs
[x_1_prediction,x_2_prediction] = meshgrid(linspace(lb(1), ub(1), 100), linspace(lb(2), ub(2),100) );


y_prediction = zeros(size(x_2_prediction,1),1) ;
y_std = zeros(size(x_2_prediction,1),1) ;

% Evaluate prediction at all mesh points
for i = 1 : size(x_1_prediction,1)
    for j = 1 : size(x_2_prediction,1)
        x_Test_Point = [x_1_prediction(i,j), x_2_prediction(i,j)] ;
        [ prediction, std ] = Predict_GP(x_Test_Point, X, Y, lb, ub, Opt.GP ) ;
        y_prediction(i,j) = prediction ;
        y_std(i,j) = std ;
    end
end

figure
surf(x_1_prediction,x_2_prediction,y_prediction)
hold on
plot3(X(:,1), X(:,2), Y(:), 'X') ;

figure
surf(x_1_prediction,x_2_prediction,y_std)
