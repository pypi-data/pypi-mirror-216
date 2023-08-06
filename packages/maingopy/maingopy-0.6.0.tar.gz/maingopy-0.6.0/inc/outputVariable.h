/**********************************************************************************
 * Copyright (c) 2019 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 **********************************************************************************/

#pragma once

#include "ffunc.hpp"

#include <string>


namespace maingo {


/**
	* @struct OutputVariable
	* @brief Struct for storing additional output variables
	*
	* Since the model evaluation can contain several intermediate variables that appear neither as optimization variables nor as constraints directly, but the value of which might be interesting at the optimal solution point,
	* a vector of these structs can be used in the EvaluationContainer to give such additional output after the problem is solved.
	*/
struct OutputVariable {

  public:
    /**
			* @brief Constructor for use in the evaluate function
			*
			* @param[in] descIn is a string describing the variable
			* @param[in] valueIn is the value of the variable at the current point
			*/
    OutputVariable(const std::string descIn, const mc::FFVar valueIn):
        description(descIn), value(valueIn) {}

    /**
			* @brief Constructor for use in the evaluate function
			*
			* @param[in] valueIn is the value of the variable at the current point
			* @param[in] descIn is a string describing the variable
			*/
    OutputVariable(const mc::FFVar valueIn, const std::string descIn):
        value(valueIn), description(descIn) {}

    /**
			* @brief Constructor for use in the evaluate function
			*
			* @param[in] inTuple is a tuple containing the value of the variable at the current point and a descriptive string
			*/
    OutputVariable(const std::tuple<mc::FFVar, std::string> inTuple):
        value(std::get<0>(inTuple)), description(std::get<1>(inTuple)) {}

    /**
			* @brief Constructor for use in the evaluate function
			*
			* @param[in] inTuple is a tuple containing the value of the variable at the current point and a descriptive string
			*/
    OutputVariable(const std::tuple<std::string, mc::FFVar> inTuple):
        value(std::get<1>(inTuple)), description(std::get<0>(inTuple)) {}

    /**
			* @brief Destructor
			*/
    ~OutputVariable() = default;

    /**
			* @brief Copy constructor
			*
			* @param[in] variableIn is the output variable to be copied
			*/
    OutputVariable(const OutputVariable& variableIn) = default;

    /**
			* @brief Move constructor
			*
			* @param[in] variableIn is the output variable to be moved
			*/
    OutputVariable(OutputVariable&& variableIn) = default;

    /**
			* @brief Copy assignment operator
			*
			* @param[in] variableIn is the output variable to be copied
			*/
    OutputVariable& operator=(const OutputVariable& variableIn) = default;

    /**
			* @brief Move assignment operator
			*
			* @param[in] variableIn is the output variable to be moved
			*/
    OutputVariable& operator=(OutputVariable&& variableIn) = default;

    /**
        *  @brief Equality comparison operator
        */
    inline bool operator==(const OutputVariable& other) const
    {
        return ((description == other.description) && (value == other.value));
    }

    mc::FFVar value         = {}; /*!< Variable object */
    std::string description = {}; /*!< Description, e.g. name of variable */
};


}    // end namespace maingo