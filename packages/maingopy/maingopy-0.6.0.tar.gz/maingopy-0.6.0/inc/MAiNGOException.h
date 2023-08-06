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

#include "babNode.h"

#include <exception>
#include <sstream>
#include <string>
#include <typeinfo>


namespace maingo {


/**
* @class MAiNGOException
* @brief This class defines the exceptions thrown by MAiNGO
*
* The class contains different constructors that allow incorporating information about the error.
* The minimum requirement is an error message. Additionally, information can be given about a
* branch-and-bound node that the error occurred in, or information on the original exception can be included
* in case the MAiNGOException is thrown in response to another type of exception.
*
*/
class MAiNGOException: public std::exception {

  public:
    MAiNGOException()                                  = delete;
    MAiNGOException(const MAiNGOException&)            = default;
    MAiNGOException(MAiNGOException&&)                 = default;
    MAiNGOException& operator=(const MAiNGOException&) = default;
    MAiNGOException& operator=(MAiNGOException&&)      = default;
    virtual ~MAiNGOException()                         = default;

    explicit MAiNGOException(const std::string& errorMessage)
    {
        _construct_complete_error_message(errorMessage, nullptr, nullptr);
    }

    MAiNGOException(const std::string& errorMessage, const babBase::BabNode& nodeThatErrorOccurredIn)
    {
        _construct_complete_error_message(errorMessage, nullptr, &nodeThatErrorOccurredIn);
    }

    MAiNGOException(const std::string& errorMessage, const std::exception& originalException)
    {
        _construct_complete_error_message(errorMessage, &originalException, nullptr);
    }

    MAiNGOException(const std::string& errorMessage, const std::exception& originalException, const babBase::BabNode& nodeThatErrorOccurredIn)
    {
        _construct_complete_error_message(errorMessage, &originalException, &nodeThatErrorOccurredIn);
    }

    const char* what() const noexcept override
    {
        return _errorMessage.c_str();
    }


  private:
    std::string _errorMessage{""};

    void _construct_complete_error_message(const std::string& errorMessage, const std::exception* originalException, const babBase::BabNode* nodeThatErrorOccurredIn)
    {
        std::ostringstream errorMessageStream;

        _append_original_exception_info_to_message(originalException, errorMessageStream);
        _append_current_error_message_to_message(errorMessage, errorMessageStream);
        _append_node_info_to_message(nodeThatErrorOccurredIn, errorMessageStream);

        _errorMessage = errorMessageStream.str();
    }

    void _append_current_error_message_to_message(const std::string& currentErrorMessage, std::ostringstream& completeErrorMessage)
    {
        completeErrorMessage << currentErrorMessage;
    }

    void _append_original_exception_info_to_message(const std::exception* originalException, std::ostringstream& completeErrorMessage)
    {
        if (originalException) {
            if (typeid(*originalException).name() != typeid(*this).name()) {
                completeErrorMessage << "  Original exception type: " << typeid(*originalException).name() << ": " << std::endl
                                     << "   ";
            }
            completeErrorMessage << originalException->what() << std::endl;
        }
    }

    void _append_node_info_to_message(const babBase::BabNode* nodeThatErrorOccurredIn, std::ostringstream& completeErrorMessage)
    {
        if (nodeThatErrorOccurredIn) {
            std::vector<double> lowerVarBounds(nodeThatErrorOccurredIn->get_lower_bounds()), upperVarBounds(nodeThatErrorOccurredIn->get_upper_bounds());
            completeErrorMessage << std::endl
                                 << "  Exception was thrown while processing node no. " << nodeThatErrorOccurredIn->get_ID() << ":";
            for (size_t i = 0; i < lowerVarBounds.size(); i++) {
                completeErrorMessage << std::endl
                                     << "    x(" << i << "): " << std::setprecision(16) << lowerVarBounds[i] << ":" << upperVarBounds[i];
            }
        }
    }
};


}    // end namespace maingo