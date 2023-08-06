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
* @brief File implementing a test for the support vector machine module.
*
**********************************************************************************/

#include <iostream>
#include <vector>
#include <string>

#include "svm.h"

/////////////////////////////////////////////////////////////////////////////////////////////
// Main function of test
int main(int argc, char** argv)
{
	try {

		// ---------------------------------------------------------------------------------
		// 1: Test Support Vector Regression
		// ---------------------------------------------------------------------------------
		
		melon::SupportVectorRegression<double> svm("sin");
		std::vector<double> input{ 1 };

		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << "1: Test Support Vector Regression" << std::endl;
		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << std::endl;

		// Load a feedforward neural network from csv files
		std::cout << "Load SVM from json file." << std::endl;
		std::cout << "Loading successful." << std::endl;

		std::cout << std::endl;


		// Evaluate SVM    
		std::cout << "Evaluate SVM at 1." << std::endl;
		std::cout << "Expected result: 0.75667891" << std::endl;

		double resultSVR = svm.calculate_prediction_reduced_space(input);

		std::cout << "Result: " << resultSVR << std::endl;
		std::cout << "Error: " << abs(resultSVR - 0.75667891) << std::endl;

		std::cout << std::endl;

		// ---------------------------------------------------------------------------------
		// 2: Test One Class Support Vector Machine
		// ---------------------------------------------------------------------------------

		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << "2: Test One Class Support Vector Machine" << std::endl;
		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << std::endl;

		// Object construction
		std::cout << "Construct SVM object loaded from json file." << std::endl;
		melon::SupportVectorMachineOneClass<double> constraint("banana");
		std::cout << "Constructing object successful." << std::endl;

		std::cout << std::endl;

		std::vector<double> input1{ 1, 1 };
		double expected_output1 = 2.79433356;

		std::cout << "Evaluate constraint at (" << input1[0] << " , " << input1[1] << " )" << std::endl;
		std::cout << "Expected result: " << expected_output1 << std::endl;
		double result = constraint.calculate_prediction_reduced_space(input1);
		std::cout << "Result: " << result << std::endl;
		std::cout << "Error: " << abs(result - expected_output1) << std::endl;
		std::cout << std::endl;

		std::cout << "Note: The expected results were computed in Python. Small varientions are expected." << std::endl;

		std::cout << std::endl;
	}
	catch (std::exception &e) {
		std::cerr << std::endl
			<< "  Encountered exception:" << std::endl
			<< e.what() << std::endl;
	}
	catch (...) {
		std::cerr << std::endl << "  Encountered an unknown fatal error. Terminating." << std::endl;
	}
}
	