/**********************************************************************************
 * Copyright (c) 2021-2023 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 **********************************************************************************/

#include "logger.h"
#include "settings.h"

#include <gtest/gtest.h>


///////////////////////////////////////////////////
// struct on which the unit test will be preformed on
struct TestLogger: testing::Test {
    std::shared_ptr<maingo::Settings> settings = std::make_shared<maingo::Settings>();
    std::shared_ptr<maingo::Logger> logger     = std::make_shared<maingo::Logger>(settings);
};


///////////////////////////////////////////////////
// testing all three versions of _get_(max_)verb on different verbosities
TEST_F(TestLogger, TestVerb)
{
    settings->loggingDestination = maingo::LOGGING_OUTSTREAM;

    testing::internal::CaptureStdout();


    // test _get_verb()

    settings->LBP_verbosity = maingo::VERB_NONE;
    settings->UBP_verbosity = maingo::VERB_NORMAL;
    settings->BAB_verbosity = maingo::VERB_ALL;

    logger->print_message("1", maingo::VERB_NONE, maingo::LBP_VERBOSITY);
    logger->print_message("2", maingo::VERB_NORMAL, maingo::LBP_VERBOSITY);
    logger->print_message("3", maingo::VERB_ALL, maingo::LBP_VERBOSITY);

    logger->print_message("4", maingo::VERB_NONE, maingo::UBP_VERBOSITY);
    logger->print_message("5", maingo::VERB_NORMAL, maingo::UBP_VERBOSITY);
    logger->print_message("6", maingo::VERB_ALL, maingo::UBP_VERBOSITY);

    logger->print_message("7", maingo::VERB_NONE, maingo::BAB_VERBOSITY);
    logger->print_message("8", maingo::VERB_NORMAL, maingo::BAB_VERBOSITY);
    logger->print_message("9", maingo::VERB_ALL, maingo::BAB_VERBOSITY);


    // test _get_max_verb() for two input verbosities

    settings->LBP_verbosity = maingo::VERB_NORMAL;
    settings->UBP_verbosity = maingo::VERB_NONE;

    logger->print_message("A", maingo::VERB_NONE, maingo::LBP_VERBOSITY, maingo::UBP_VERBOSITY);
    logger->print_message("B", maingo::VERB_NORMAL, maingo::LBP_VERBOSITY, maingo::UBP_VERBOSITY);
    logger->print_message("C", maingo::VERB_ALL, maingo::LBP_VERBOSITY, maingo::UBP_VERBOSITY);

    logger->print_message("D", maingo::VERB_NONE, maingo::UBP_VERBOSITY, maingo::LBP_VERBOSITY);
    logger->print_message("E", maingo::VERB_NORMAL, maingo::UBP_VERBOSITY, maingo::LBP_VERBOSITY);
    logger->print_message("F", maingo::VERB_ALL, maingo::UBP_VERBOSITY, maingo::LBP_VERBOSITY);

    // test _get_max_verb() for three input verbosities

    settings->LBP_verbosity = maingo::VERB_ALL;
    settings->UBP_verbosity = maingo::VERB_NORMAL;
    settings->BAB_verbosity = maingo::VERB_NONE;

    logger->print_message("G", maingo::VERB_NONE, maingo::LBP_VERBOSITY, maingo::UBP_VERBOSITY, maingo::BAB_VERBOSITY);
    logger->print_message("H", maingo::VERB_NORMAL, maingo::LBP_VERBOSITY, maingo::UBP_VERBOSITY, maingo::BAB_VERBOSITY);
    logger->print_message("I", maingo::VERB_ALL, maingo::LBP_VERBOSITY, maingo::UBP_VERBOSITY, maingo::BAB_VERBOSITY);

    logger->print_message("J", maingo::VERB_NONE, maingo::BAB_VERBOSITY, maingo::BAB_VERBOSITY, maingo::BAB_VERBOSITY);
    logger->print_message("K", maingo::VERB_NORMAL, maingo::BAB_VERBOSITY, maingo::BAB_VERBOSITY, maingo::BAB_VERBOSITY);
    logger->print_message("L", maingo::VERB_ALL, maingo::BAB_VERBOSITY, maingo::BAB_VERBOSITY, maingo::BAB_VERBOSITY);


    std::string output = testing::internal::GetCapturedStdout();

    EXPECT_EQ("145789ABDEGHIJ", output);
}


///////////////////////////////////////////////////
// testing output of logger to screen and log at different verbosities
TEST_F(TestLogger, TestOutputLogger)
{
    settings->LBP_verbosity = maingo::VERB_NONE;
    settings->UBP_verbosity = maingo::VERB_NORMAL;
    settings->BAB_verbosity = maingo::VERB_ALL;


    // testing setting option LOGGING_OUTSTREAM by capturing output to console
    settings->loggingDestination = maingo::LOGGING_OUTSTREAM;

    testing::internal::CaptureStdout();

    logger->print_message("1", maingo::VERB_NONE, maingo::BAB_VERBOSITY);
    logger->print_message("2", maingo::VERB_ALL, maingo::LBP_VERBOSITY);
    logger->print_message("3", maingo::VERB_NORMAL, maingo::UBP_VERBOSITY);

    std::string output = testing::internal::GetCapturedStdout();

    // second message should not be printed
    EXPECT_EQ("13", output);

    logger->clear();


    // testing setting option LOGGING_FILE
    settings->loggingDestination = maingo::LOGGING_FILE;

    logger->print_message("1", maingo::VERB_NONE, maingo::BAB_VERBOSITY);
    logger->print_message("2", maingo::VERB_ALL, maingo::LBP_VERBOSITY);
    logger->print_message("3", maingo::VERB_NORMAL, maingo::UBP_VERBOSITY);

    // second message should not be printed
    EXPECT_EQ("1", logger->babLine.front());
    logger->babLine.pop();
    EXPECT_EQ("3", logger->babLine.front());
    logger->babLine.pop();


    logger->clear();

    // testing clear()
    EXPECT_EQ(true, logger->babLine.empty());


    // testing setting option LOGGING_FILE_AND_STREAM
    settings->loggingDestination = maingo::LOGGING_FILE_AND_STREAM;

    testing::internal::CaptureStdout();

    logger->print_message("1", maingo::VERB_NONE, maingo::BAB_VERBOSITY);
    logger->print_message("2", maingo::VERB_ALL, maingo::LBP_VERBOSITY);
    logger->print_message("3", maingo::VERB_NORMAL, maingo::UBP_VERBOSITY);

    // second message should not be printed
    EXPECT_EQ("1", logger->babLine.front());
    logger->babLine.pop();
    EXPECT_EQ("3", logger->babLine.front());
    logger->babLine.pop();

    output = testing::internal::GetCapturedStdout();

    EXPECT_EQ("13", output);
}


///////////////////////////////////////////////////
//testing the output of print_vector() by capturing the output to the consol and comparing it to the expected output
TEST_F(TestLogger, TestPrintVector)
{
    std::vector<double> testVector = {0.0, 1.0};

    settings->LBP_verbosity      = maingo::VERB_NONE;
    settings->loggingDestination = maingo::LOGGING_OUTSTREAM;


    // capturing output of print_vector second statement should not create output
    testing::internal::CaptureStdout();

    logger->print_vector(2, testVector, "TestString", maingo::VERB_NONE, maingo::LBP_VERBOSITY);
    logger->print_vector(1, testVector, "TestString", maingo::VERB_NORMAL, maingo::LBP_VERBOSITY);


    std::string output = testing::internal::GetCapturedStdout();


    // expected output
    std::ostringstream compString;

    compString << "TestString" << std::endl;
    for (unsigned int i = 0; i < 2; i++) {
        compString << "   x(" << i << "): " << testVector[i] << std::endl;
    }


    EXPECT_EQ(compString.str(), output);

    // expecting error if the numbers of values to be printed exceed the number of elements in the testVector
    ASSERT_ANY_THROW(logger->print_vector(3, testVector, "TestString", maingo::VERB_NONE, maingo::LBP_VERBOSITY));
}