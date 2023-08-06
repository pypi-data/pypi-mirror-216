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
* @brief File implementing the test for the convex hull.
*
**********************************************************************************/

#include <iostream>
#include <vector>

#include "convexhull.h"

/////////////////////////////////////////////////////////////////////////////////////////////
// Main function of test
int main(int argc, char** argv)
{
	try {

		// ---------------------------------------------------------------------------------
		// 0: Create Network and define input
		// ---------------------------------------------------------------------------------


		// Load a Gaussian process from a json file
		std::cout << "Load convex hull from a json file." << std::endl;
		melon::ConvexHull<double> hull("testConvexHull");
		std::cout << "Loading successful." << std::endl;
		std::cout << std::endl;

		std::vector<double> input(2, 1.);

		// ---------------------------------------------------------------------------------
		// 1: Test convex hull
		// ---------------------------------------------------------------------------------

		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << "Test convex hull" << std::endl;
		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << std::endl;

		// Evaluate network    
		std::cout << "Evaluate convex hull constraints at (1,1)." << std::endl;
		std::cout << "Expected result: [-1.10940, -2.10859, 0, 0]." << std::endl;

		std::vector<double> results = hull.generate_constraints(input);

		std::cout << "Result: [" << results.at(0) << ", " << results.at(1) << ", " << results.at(2) << ", " << results.at(3) << "]." << std::endl;

		std::cout << "Mean Error: " << abs(1/4*(results.at(0) - (-1.10940) + results.at(1) - (-2.10859) + results.at(2) + results.at(3))) << std::endl;

		std::cout << std::endl;
		std::cout << "Note: The expected results are computed in Python. Small varientions are expected." << std::endl;

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