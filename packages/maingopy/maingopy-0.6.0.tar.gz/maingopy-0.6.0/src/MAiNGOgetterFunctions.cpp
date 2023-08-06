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

#include "MAiNGO.h"
#include "MAiNGOException.h"
#include "bab.h"


using namespace maingo;


/////////////////////////////////////////////////////////////////////////
// returns the value of the objective at solution point
double
MAiNGO::get_objective_value() const
{
    if ((_maingoStatus != GLOBALLY_OPTIMAL) && (_maingoStatus != FEASIBLE_POINT)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying objective value. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    return _solutionValue;
}


/////////////////////////////////////////////////////////////////////////
// returns the solution point
std::vector<double>
MAiNGO::get_solution_point() const
{
    if (_solutionPoint.empty()) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying solution point. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    std::vector<double> solutionPoint;
    unsigned removed = 0;
    for (unsigned i = 0; i < _nvarOriginal; ++i) {
        if (_removedVariables[i]) {
            // If the variable has been removed from the optimization problem, simply return the middle point of the original interval
            solutionPoint.push_back(_originalVariables[i].get_lower_bound());
            removed++;
        }
        else {
            // Otherwise simply return the value of the variable at solution point
            solutionPoint.push_back(_solutionPoint[i - removed]);
        }
    }
    return solutionPoint;
}


/////////////////////////////////////////////////////////////////////////
// returns the solution time
double
MAiNGO::get_cpu_solution_time() const
{
    if ((_maingoStatus == NOT_SOLVED_YET)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying solution time. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    return _solutionTime;
}


/////////////////////////////////////////////////////////////////////////
// returns the solution time
double
MAiNGO::get_wallclock_solution_time() const
{
    if ((_maingoStatus == NOT_SOLVED_YET)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying solution time. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    return _solutionTimeWallClock;
}


////////////////////////////////////////////////////////////////////////////////////////
// function returning the number of iterations
double
MAiNGO::get_iterations() const
{
    if ((_maingoStatus == NOT_SOLVED_YET)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying number of iterations. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    if (_myBaB) {
        return _myBaB->get_iterations();
    }
    else {
        return 0;
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// function returning the maximum number of nodes in memory
double
MAiNGO::get_max_nodes_in_memory() const
{
    if ((_maingoStatus == NOT_SOLVED_YET)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying number of nodes in memory. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    if (_myBaB) {
        return _myBaB->get_max_nodes_in_memory();
    }
    else {
        return 1;
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// function returning number of UBD problems solved
double
MAiNGO::get_UBP_count() const
{
    if ((_maingoStatus == NOT_SOLVED_YET)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying UBP count. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    if (_myBaB) {
        return _myBaB->get_UBP_count();
    }
    else {
        return 1;
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// function returning number of LBD problems solved
double
MAiNGO::get_LBP_count() const
{
    if ((_maingoStatus == NOT_SOLVED_YET)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying LBP count. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    if (_myBaB) {
        return _myBaB->get_LBP_count();
    }
    else {
        return 0;
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// function returning the final LBD
double
MAiNGO::get_final_LBD() const
{
    if ((_maingoStatus == NOT_SOLVED_YET)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying final LBD. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    if (_myBaB) {
        return _myBaB->get_final_LBD();
    }
    else {
        return _solutionValue;    // In case of an LP, MIP, QP, or MIQP, we take the solution to be exact for now...
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// function returning the final absolute gap
double
MAiNGO::get_final_abs_gap() const
{
    if ((_maingoStatus == NOT_SOLVED_YET)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying final absolute gap. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    if (_myBaB) {
        return _myBaB->get_final_abs_gap();
    }
    else {
        return 0;
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// function returning the final relative gap
double
MAiNGO::get_final_rel_gap() const
{
    if ((_maingoStatus == NOT_SOLVED_YET)) {
        std::ostringstream errmsg;
        errmsg << "  MAiNGO: Error querying final relative gap. MAiNGO status: " << _maingoStatus;
        throw MAiNGOException(errmsg.str());
    }
    if (_myBaB) {
        return _myBaB->get_final_rel_gap();
    }
    else {
        return 0;
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// function returning the value of a desired option
double
MAiNGO::get_option(const std::string& option) const
{
    if (option == "epsilonA") {
        return _maingoSettings->epsilonA;
    }
    else if (option == "epsilonR") {
        return _maingoSettings->epsilonR;
    }
    else if (option == "deltaIneq") {
        return _maingoSettings->deltaIneq;
    }
    else if (option == "deltaEq") {
        return _maingoSettings->deltaEq;
    }
    else if (option == "relNodeTol") {
        return _maingoSettings->relNodeTol;
    }
    else if (option == "BAB_maxNodes") {
        return _maingoSettings->BAB_maxNodes;
    }
    else if (option == "BAB_maxIterations") {
        return _maingoSettings->BAB_maxIterations;
    }
    else if (option == "maxTime") {
        return _maingoSettings->maxTime;
    }
    else if (option == "confirmTermination") {
        return _maingoSettings->confirmTermination;
    }
    else if (option == "terminateOnFeasiblePoint") {
        return _maingoSettings->terminateOnFeasiblePoint;
    }
    else if (option == "targetLowerBound") {
        return _maingoSettings->targetLowerBound;
    }
    else if (option == "targetUpperBound") {
        return _maingoSettings->targetUpperBound;
    }
    else if (option == "PRE_maxLocalSearches") {
        return _maingoSettings->PRE_maxLocalSearches;
    }
    else if (option == "PRE_obbtMaxRounds") {
        return _maingoSettings->PRE_obbtMaxRounds;
    }
    else if (option == "PRE_pureMultistart") {
        return _maingoSettings->PRE_pureMultistart;
    }
    else if (option == "BAB_nodeSelection") {
        return _maingoSettings->BAB_nodeSelection;
    }
    else if (option == "BAB_branchVariable") {
        return _maingoSettings->BAB_branchVariable;
    }
    else if (option == "BAB_alwaysSolveObbt") {
        return _maingoSettings->BAB_alwaysSolveObbt;
    }
    else if (option == "BAB_probing") {
        return _maingoSettings->BAB_probing;
    }
    else if (option == "BAB_dbbt") {
        return _maingoSettings->BAB_dbbt;
    }
    else if (option == "BAB_constraintPropagation") {
        return _maingoSettings->BAB_constraintPropagation;
    }
    else if (option == "LBP_solver") {
        return _maingoSettings->LBP_solver;
    }
    else if (option == "LBP_linPoints") {
        return _maingoSettings->LBP_linPoints;
    }
    else if (option == "LBP_subgradientIntervals") {
        return _maingoSettings->LBP_subgradientIntervals;
    }
    else if (option == "LBP_obbtMinImprovement") {
        return _maingoSettings->LBP_obbtMinImprovement;
    }
    else if (option == "LBP_activateMoreScaling") {
        return _maingoSettings->LBP_activateMoreScaling;
    }
    else if (option == "LBP_addAuxiliaryVars") {
        return _maingoSettings->LBP_addAuxiliaryVars;
    }
    else if (option == "LBP_minFactorsForAux") {
        return _maingoSettings->LBP_minFactorsForAux;
    }
    else if (option == "LBP_maxNumberOfAddedFactors") {
        return _maingoSettings->LBP_maxNumberOfAddedFactors;
    }
    else if (option == "MC_mvcompUse") {
        return _maingoSettings->MC_mvcompUse;
    }
    else if (option == "MC_mvcompTol") {
        return _maingoSettings->MC_mvcompTol;
    }
    else if (option == "MC_envelTol") {
        return _maingoSettings->MC_envelTol;
    }
    else if (option == "UBP_solverPreprocessing") {
        return _maingoSettings->UBP_solverPreprocessing;
    }
    else if (option == "UBP_maxStepsPreprocessing") {
        return _maingoSettings->UBP_maxStepsPreprocessing;
    }
    else if (option == "UBP_maxTimePreprocessing") {
        return _maingoSettings->UBP_maxTimePreprocessing;
    }
    else if (option == "UBP_solverBab") {
        return _maingoSettings->UBP_solverBab;
    }
    else if (option == "UBP_maxStepsBab") {
        return _maingoSettings->UBP_maxStepsBab;
    }
    else if (option == "UBP_maxTimeBab") {
        return _maingoSettings->UBP_maxTimeBab;
    }
    else if (option == "UBP_ignoreNodeBounds") {
        return _maingoSettings->UBP_ignoreNodeBounds;
    }
    else if (option == "EC_nPoints") {
        return _maingoSettings->EC_nPoints;
    }
    else if (option == "LBP_verbosity") {
        return _maingoSettings->LBP_verbosity;
    }
    else if (option == "UBP_verbosity") {
        return _maingoSettings->UBP_verbosity;
    }
    else if (option == "BAB_verbosity") {
        return _maingoSettings->BAB_verbosity;
    }
    else if (option == "BAB_printFreq") {
        return _maingoSettings->BAB_printFreq;
    }
    else if (option == "BAB_logFreq") {
        return _maingoSettings->BAB_logFreq;
    }
    else if (option == "loggingDestination") {
        return _maingoSettings->loggingDestination;
    }
    else if (option == "writeCsv") {
        return _maingoSettings->writeCsv;
    }
    else if (option == "writeJson") {
        return _maingoSettings->writeJson;
    }
    else if (option == "writeResultFile") {
        return _maingoSettings->writeResultFile;
    }
    else if (option == "writeToLogSec") {
        return _maingoSettings->writeToLogSec;
    }
    else if (option == "PRE_printEveryLocalSearch") {
        return _maingoSettings->PRE_printEveryLocalSearch;
    }
    else if (option == "modelWritingLanguage") {
        return _maingoSettings->modelWritingLanguage;
    }
    std::cout << "Warning: No setting \"" << option << "\" found. \n";
    return -1;
}


////////////////////////////////////////////////////////////////////////////////////////
// function returning the current MAiNGO status
RETCODE
MAiNGO::get_status() const
{
    return _maingoStatus;
}