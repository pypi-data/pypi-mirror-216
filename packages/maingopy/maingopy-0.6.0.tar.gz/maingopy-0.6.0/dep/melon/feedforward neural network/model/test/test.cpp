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
* @brief File implementing a test for the feedforward module.
*
**********************************************************************************/

#include <ffNet.h>
#include <iostream>
#include <vector>

/////////////////////////////////////////////////////////////////////////////////////////////
// Main function of test
int main(int argc, char** argv)
{
	try {

		// ---------------------------------------------------------------------------------
		// 0: Create Network and define input
		// ---------------------------------------------------------------------------------

		melon::FeedForwardNet<double> network;
		std::vector<double> input(2, 0.);

		// ---------------------------------------------------------------------------------
		// 1: Test Network parsed from CSV file
		// ---------------------------------------------------------------------------------

		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << "1: Test Network parsed from csv file" << std::endl;
		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << std::endl;

		// Load a feedforward neural network from csv files
		std::cout << "Load network from csv file." << std::endl;
		network.load_model("networks", "network_csv", melon::MODEL_FILE_TYPE::CSV);
		std::cout << "Loading successful." << std::endl;

		std::cout << std::endl;


		// Evaluate network    
		std::cout << "Evaluate network at (0,0)." << std::endl;
		std::cout << "Expected result: -9.99796e-06" << std::endl;

		double resultCsv = network.calculate_prediction_reduced_space(input).at(0);

		std::cout << "Result: " << resultCsv << std::endl;
		std::cout << "Error: " << abs(resultCsv + 9.99796e-06) << std::endl;

		std::cout << std::endl;


		// ---------------------------------------------------------------------------------
		// 2: Test Network parsed from XML file
		// ---------------------------------------------------------------------------------

		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << "2: Test Network parsed from xml file" << std::endl;
		std::cout << "---------------------------------------------------------------------------------" << std::endl;
		std::cout << std::endl;

		// Load a feedforward neural network from csv files
		std::cout << "Load network from xml file." << std::endl;
		network.load_model("networks", "network_xml", melon::MODEL_FILE_TYPE::XML);
		std::cout << "Loading successful." << std::endl;

		std::cout << std::endl;

		// Evaluate network
		std::cout << "Evaluate network at (0,0)." << std::endl;
		std::cout << "Expected result: -1.44385" << std::endl;

		double resultXml = network.calculate_prediction_reduced_space(input).at(0);

		std::cout << "Result: " << resultXml << std::endl;
		std::cout << "Error: " << abs(resultXml + 1.44385) << std::endl;

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