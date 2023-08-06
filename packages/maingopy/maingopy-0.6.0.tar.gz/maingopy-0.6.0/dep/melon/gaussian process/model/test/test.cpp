/**********************************************************************************
* Copyright (c) 2020 Process Systems Engineering (AVT.SVT), RWTH Aachen University
*
* This program and the accompanying materials are made available under the
* terms of the Eclipse Public License 2.0 which is available at
* http://www.eclipse.org/legal/epl-2.0.
*
* SPDX-License-Identifier: EPL-2.0
*
* @file test.cpp
*
* @brief File implementing a test.
*
**********************************************************************************/

#include <iostream>
#include <vector>

#include "mcfunc.hpp"

using mc::xexpax;
using mc::expx_times_y;

#include "gp.h"

/////////////////////////////////////////////////////////////////////////////////////////////
// Main function of test
int main(int argc, char** argv)
{
	try {

	// ---------------------------------------------------------------------------------
  // 0: Create Gaussian process and define input
  // ---------------------------------------------------------------------------------

	// Load a Gaussian process from a json file
	std::cout << "Load a Gaussian process from a json file." << std::endl;
	melon::GaussianProcess<double> gp = melon::GaussianProcess<double>("testGP");
	std::cout << "Loading successful." << std::endl;

	std::cout << std::endl;

	std::vector<double>  input;  //input(gp.getDX()); 
	input.push_back(1.5);
	input.push_back(-2);

	// ---------------------------------------------------------------------------------
	// 1: Test prediction of Gaussian process parsed from json file
	// ---------------------------------------------------------------------------------

	std::cout << "---------------------------------------------------------------------------------" << std::endl;
	std::cout << "1: Test prediction of Gaussian process parsed from json file" << std::endl;
	std::cout << "---------------------------------------------------------------------------------" << std::endl;
	std::cout << std::endl;


	// Evaluate prediction    
	std::cout << "Evaluate Gaussian process prediction at (1.5,-2)." << std::endl;
	std::cout << "Expected result: -0.728381223890336" << std::endl;

	double mu = gp.calculate_prediction_reduced_space(input);

	std::cout << "Result prediction: " << mu << std::endl;
	std::cout << "Error: " << abs(mu + 0.728381223890336) << std::endl;
	std::cout << std::endl;


	// ---------------------------------------------------------------------------------
	// 2: Test variance of Gaussian process parsed from json file
	// ---------------------------------------------------------------------------------

	std::cout << "---------------------------------------------------------------------------------" << std::endl;
	std::cout << "2: Test variance of Gaussian process parsed from json file" << std::endl;
	std::cout << "---------------------------------------------------------------------------------" << std::endl;
	std::cout << std::endl;


	// Evaluate variance    
	std::cout << "Evaluate Gaussian process variance at (1.5,-2)." << std::endl;
	std::cout << "Expected result: 0.475676568363487" << std::endl;

	double variance = gp.calculate_variance_reduced_space(input); // variance
	// double sigma = sqrt(variance + 1e-16); // standard deviation

	std::cout << "Result variance: " << variance << std::endl;
	std::cout << "Error: " << abs(variance- 0.475676568363487) << std::endl;

	std::cout << std::endl;

	std::cout << "Note: The expected results are computed in Matlab. Small varientions are expected." << std::endl;

	}
	catch (std::exception &e) {
	std::cerr << std::endl
		<< "  Encountered exception:" << std::endl
		<< e.what() << std::endl;
	}
	catch (...) {
	std::cerr << std::endl
		<< "  Encountered an unknown fatal error. Terminating." << std::endl;
	}

}