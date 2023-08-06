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
#include "MAiNGOmodelEpsCon.h"
#include "bab.h"
#include "getTime.h"
#include "intervalLibrary.h"
#include "lbp.h"
#include "mpiUtilities.h"
#include "ubp.h"


using namespace maingo;


/////////////////////////////////////////////////////////////////////////
// constructor which initializes models and solvers and performs a sanity check on the model
MAiNGO::MAiNGO(std::shared_ptr<MAiNGOmodel> myModel)
{

#ifdef HAVE_MAiNGO_MPI
    // Set MPI variables
    MPI_Comm_rank(MPI_COMM_WORLD, &_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &_nProcs);
    if (_nProcs < 2) {
        throw MAiNGOException("  Error initializing MAiNGO: The parallel version of MAiNGO requires at least 2 MPI processes.");
    }
#endif

    // Initialize  internal model representation
    set_model(myModel);
}


/////////////////////////////////////////////////////////////////////////
// solve function which actually solves the problem
RETCODE
MAiNGO::solve()
{

    if (!_readyToSolve) {
        throw MAiNGOException("  Error trying to solve problem: Model has not been set successfully.");
    }

    // ---------------------------------------------------------------------------------
    // 0: Prepare
    // ---------------------------------------------------------------------------------
    MAiNGO_IF_BAB_MANAGER
        // Start timing and print header
        _preprocessTime        = get_cpu_time();
        _solutionTimeWallClock = get_wall_time();
        _logger->clear();
        _logger->create_log_file();
        _print_MAiNGO_header();
#ifdef HAVE_MAiNGO_MPI
        _logger->print_message("\n  You are using the parallel MAiNGO version. This run uses " + std::to_string(_nProcs) + " processes ( 1 manager and " + std::to_string(_nProcs - 1) + " workers ).\n",
                               VERB_NORMAL, BAB_VERBOSITY);
#endif
    MAiNGO_END_IF
    MAiNGO_MPI_BARRIER


        // ---------------------------------------------------------------------------------
        // 1: Preliminaries: inform about changed settings and write model to file in other language
        // ---------------------------------------------------------------------------------
        _maingoOriginalSettings = *_maingoSettings;    // Save original settings
    MAiNGO_IF_BAB_MANAGER
        _logger->print_settings(VERB_NORMAL, BAB_VERBOSITY);

        // Write MAiNGO model to other language if desired
        if (_maingoSettings->modelWritingLanguage != LANG_NONE) {
            _inMAiNGOsolve = true;
            write_model_to_file_in_other_language(_maingoSettings->modelWritingLanguage);
            _inMAiNGOsolve     = false;
            double tmpTimeCPU  = get_cpu_time() - _preprocessTime;
            double tmpTimeWall = get_wall_time() - _solutionTimeWallClock;
            std::string str;
            switch (_maingoSettings->modelWritingLanguage) {
                case LANG_GAMS:
                    str = ".gms";
                    break;
                default:
                    str = ".txt";
                    break;
            }
            std::ostringstream outstr;
            outstr << "  Writing to file \"MAiNGO_written_model" + str + "\" took:\n";
            outstr << "  CPU time:         " << std::fixed << std::setprecision(3) << tmpTimeCPU << " seconds.\n";
            outstr << "  Wall-clock time:  " << std::fixed << std::setprecision(3) << tmpTimeWall << " seconds.\n";
            _logger->print_message(outstr.str(), VERB_NORMAL, BAB_VERBOSITY);
            // Reset times, since we don't want to add the file writing to the final MAiNGO solution time
            _preprocessTime        = get_cpu_time();
            _solutionTimeWallClock = get_wall_time();
        }
    MAiNGO_END_IF
    MAiNGO_MPI_BARRIER

    // ---------------------------------------------------------------------------------
    // 2: Construct DAG, possibly remove unused variables, and check constant constraints
    // ---------------------------------------------------------------------------------
    try {
        _construct_DAG();
    }
    catch (const std::exception& e) {
        MAiNGO_IF_BAB_MANAGER
            std::ostringstream errmsg;
            errmsg << e.what() << "\n  Encountered a fatal error during DAG construction.";
            _write_files_error(errmsg.str());
            throw MAiNGOException("  Encountered a fatal error during DAG construction.", e);
            MAiNGO_ELSE
                throw;
            MAiNGO_END_IF
    }
    catch (...) {
        MAiNGO_IF_BAB_MANAGER
            _write_files_error("  Encountered an unknown fatal error during DAG construction.");
            throw MAiNGOException("  Encountered an unknown fatal error during DAG construction.");
            MAiNGO_ELSE
                throw;
            MAiNGO_END_IF
    }
    if (_nobj > 1) {
        MAiNGO_IF_BAB_MANAGER
            throw MAiNGOException("  Error: Problem contains more than one objective. Did you want to call solve_epsilon_constraint instead of solve?");
            MAiNGO_ELSE
                throw;
            MAiNGO_END_IF
    }
    MAiNGO_IF_BAB_MANAGER
        _print_info_about_initial_point();
    MAiNGO_END_IF

    // ---------------------------------------------------------------------------------
    // 3: Determine structure, set constraint properties, and invoke internal solution routine
    // ---------------------------------------------------------------------------------
    _analyze_and_solve_problem();


    // ---------------------------------------------------------------------------------
    // 4: Final Output
    // ---------------------------------------------------------------------------------
    MAiNGO_IF_BAB_MANAGER
        // Timing for output
        _outputTime = get_cpu_time();

        // Print problem statistics, solution, additional output & CPU time.
        _print_statistics();
        _print_solution();
        _print_additional_output();
        _print_time();

        // Write files
        _write_files();

        // Restore settings
        *_maingoSettings = _maingoOriginalSettings;
    MAiNGO_END_IF


    return _maingoStatus;
}


/////////////////////////////////////////////////////////////////////////
// solve function for multi-objective problems using the epsilon-constraint method
RETCODE
MAiNGO::solve_epsilon_constraint()
{

    if (!_readyToSolve) {
        throw MAiNGOException("  Error trying to solve problem: Model has not been set successfully.");
    }

    // ---------------------------------------------------------------------------------
    // 0: Prepare
    // ---------------------------------------------------------------------------------
    double cpuTimeEpsCon, wallTimeEpsCon;
    MAiNGO_IF_BAB_MANAGER
        // Start timing and print header
        cpuTimeEpsCon  = 0.;    // We compute the CPU time by suming over all runs
        wallTimeEpsCon = get_wall_time();
        _logger->clear();
        _logger->create_log_file();
        _logger->create_iterations_csv_file(_maingoSettings->writeCsv);
        _print_MAiNGO_header();
#ifdef HAVE_MAiNGO_MPI
        _logger->print_message("\n  You are using the parallel MAiNGO version. This run uses " + std::to_string(_nProcs) + " processes ( 1 manager and " + std::to_string(_nProcs - 1) + " workers ).\n",
                               VERB_NORMAL, BAB_VERBOSITY);
#endif
    MAiNGO_END_IF
    MAiNGO_MPI_BARRIER


        // ---------------------------------------------------------------------------------
        // 1: Inform the user about changed Settings
        // ---------------------------------------------------------------------------------
        _maingoOriginalSettings = *_maingoSettings;    // Save original settings
    MAiNGO_IF_BAB_MANAGER
        _logger->print_settings(VERB_NORMAL, BAB_VERBOSITY);
        // Don't write MAiNGO model to other language, even if desired
        if (_maingoSettings->modelWritingLanguage != LANG_NONE) {
            _logger->print_message("  Warning: Not writing to other language when solving multi-objective problem.", VERB_NORMAL, BAB_VERBOSITY);
        }
    MAiNGO_END_IF
    MAiNGO_MPI_BARRIER


        // ---------------------------------------------------------------------------------
        // 2: Get information on model
        // ---------------------------------------------------------------------------------
        std::shared_ptr<MAiNGOmodelEpsCon>
            epsConModel = std::dynamic_pointer_cast<MAiNGOmodelEpsCon>(_myFFVARmodel);
    if (!epsConModel) {
        MAiNGO_IF_BAB_MANAGER
            throw MAiNGOException("  Error in epsilon-constraint method: model needs to be derived from MAiNGOmodelEpsCon.");
            MAiNGO_ELSE
                throw;
            MAiNGO_END_IF
    }
    EvaluationContainer userResult = epsConModel->evaluate_user_model(std::vector<mc::FFVar>(_nvarOriginal));
    size_t nObj                    = userResult.objective.size();
    if (nObj != 2) {
        MAiNGO_IF_BAB_MANAGER
            throw MAiNGOException("  Error in epsilon-constraint method: currently only supporting exactly two objectives.");
            MAiNGO_ELSE
                throw;
            MAiNGO_END_IF
    }
    std::vector<double> epsilon(nObj, _maingoSettings->infinity);


    // ---------------------------------------------------------------------------------
    // 2: Solve single-objective problems first
    // ---------------------------------------------------------------------------------
    epsConModel->set_epsilon(epsilon);
    std::vector<std::vector<double>> optimalObjectives;
    std::vector<std::vector<double>> solutionPoints;
    RETCODE status;
    for (size_t iObj = 0; iObj < nObj; iObj++) {
        // First, minimize objective iObj without additional constraints
        epsConModel->set_single_objective(true);
        MAiNGO_IF_BAB_MANAGER
            // Reset timing for this run and give intermediate output
            _preprocessTime        = get_cpu_time();
            _solutionTimeWallClock = get_wall_time();
            _print_message(std::string("*** Solving single-objective problem for objective " + std::to_string(iObj) + ". ***"));
        MAiNGO_END_IF
        epsConModel->set_objective_index(iObj);
        try {
            _construct_DAG();
        }
        catch (const std::exception& e) {
            MAiNGO_IF_BAB_MANAGER
                std::ostringstream errmsg;
                errmsg << e.what() << "\n  Encountered a fatal error during DAG construction.";
                _write_files_error(errmsg.str());
                throw MAiNGOException("  Encountered a fatal error during DAG construction.", e);
                MAiNGO_ELSE
                    throw;
                MAiNGO_END_IF
        }
        catch (...) {
            MAiNGO_IF_BAB_MANAGER
                _write_files_error("  Encountered an unknown fatal error during DAG construction.");
                throw MAiNGOException("  Encountered an unknown fatal error during DAG construction.");
                MAiNGO_ELSE
                    throw;
                MAiNGO_END_IF
        }
        status = _analyze_and_solve_problem();
        MAiNGO_IF_BAB_MANAGER
            // Print problem statistics, solution, additional output & CPU time.
            _outputTime = get_cpu_time();
            _print_statistics();
            _print_solution();
            _print_additional_output();
            _print_time();
            if (status == INFEASIBLE) {
                if (iObj != 0) {
                    _print_message(std::string("*** Error in epsilon-constraint: false infeasibility claim ***"));
                }
                else {
                    _print_message(std::string("*** Problem is infeasible. Stopping epsilon-constraint method. ***"));
                }
#ifdef HAVE_MAiNGO_MPI
                BCAST_TAG bcastTag = BCAST_EXCEPTION;
                MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
                break;
            }
            std::vector<double> tmpObjectives(nObj);
            std::vector<std::pair<std::string, double>> tmpOutput = evaluate_additional_outputs_at_solution_point();
            for (size_t jObj = 0; jObj < nObj; jObj++) {
                tmpObjectives[jObj] = tmpOutput[tmpOutput.size() - nObj + jObj].second;
            }
            optimalObjectives.push_back(tmpObjectives);
            cpuTimeEpsCon += get_cpu_solution_time();
#ifdef HAVE_MAiNGO_MPI
            BCAST_TAG bcastTag = BCAST_EVERYTHING_FINE;
            MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            MAiNGO_ELSE    // Workers just wait for a broadcast
                // Check whether an exception was raised
                BCAST_TAG tag;
                MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
                if (tag == BCAST_EXCEPTION) {
                    throw MAiNGOMpiException("  Worker " + std::to_string(_rank) + " received message about an exception during epsilon-constraint method.", MAiNGOMpiException::ORIGIN_OTHER);
                }
#endif
            MAiNGO_END_IF
            *_maingoSettings = _maingoOriginalSettings;
            // Next, minimize the other objective s.t. iObj stays the same
            MAiNGO_IF_BAB_MANAGER
                // Reset timing for this run and give intermediate output
                _preprocessTime        = get_cpu_time();
                _solutionTimeWallClock = get_wall_time();
                _print_message(std::string("*** Solving complementary problem to single-objective problem for objective " + std::to_string(iObj) + ". ***"));
            MAiNGO_END_IF
            // Get correct epsilon
            epsConModel->set_single_objective(false);
            double tmpOptimalObjective;
            MAiNGO_IF_BAB_MANAGER
                tmpOptimalObjective = optimalObjectives[iObj][iObj];
            MAiNGO_END_IF
#ifdef HAVE_MAiNGO_MPI
            MPI_Bcast(&tmpOptimalObjective, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
#endif
            epsilon[iObj] = tmpOptimalObjective;
            epsConModel->set_epsilon(epsilon);
            unsigned otherObj = (iObj == 0) ? 1 : 0;    // Works only for bi-objective
            epsConModel->set_objective_index(otherObj);
            try {
                _construct_DAG();
            }
            catch (const std::exception& e) {
                MAiNGO_IF_BAB_MANAGER
                    std::ostringstream errmsg;
                    errmsg << e.what() << "\n  Encountered a fatal error during DAG construction.";
                    _write_files_error(errmsg.str());
                    throw MAiNGOException("  Encountered a fatal error during DAG construction.", e);
                    MAiNGO_ELSE
                        throw;
                    MAiNGO_END_IF
            }
            catch (...) {
                MAiNGO_IF_BAB_MANAGER
                    _write_files_error("  Encountered an unknown fatal error during DAG construction.");
                    throw MAiNGOException("  Encountered an unknown fatal error during DAG construction.");
                    MAiNGO_ELSE
                        throw;
                    MAiNGO_END_IF
            }
            status = _analyze_and_solve_problem();
            MAiNGO_IF_BAB_MANAGER
                // Print problem statistics, solution, additional output & CPU time.
                _outputTime = get_cpu_time();
                _print_statistics();
                _print_solution();
                _print_additional_output();
                _print_time();
                if (status == INFEASIBLE) {
                    if (iObj != 0) {
                        _print_message(std::string("*** Error in epsilon-constraint: false infeasibility claim ***"));
                    }
                    else {
                        _print_message(std::string("*** Problem is infeasible. Stopping epsilon-constraint method. ***"));
                    }
#ifdef HAVE_MAiNGO_MPI
                    BCAST_TAG bcastTag = BCAST_EXCEPTION;
                    MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
                    break;
                }
                std::vector<std::pair<std::string, double>> tmpOutput2 = evaluate_additional_outputs_at_solution_point();
                for (size_t jObj = 0; jObj < nObj; jObj++) {
                    optimalObjectives[iObj][jObj] = tmpOutput2[tmpOutput2.size() - nObj + jObj].second;
                }
                solutionPoints.push_back(get_solution_point());
                cpuTimeEpsCon += get_cpu_solution_time();
#ifdef HAVE_MAiNGO_MPI
                BCAST_TAG bcastTag = BCAST_EVERYTHING_FINE;
                MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
                MAiNGO_ELSE    // Workers just wait for a broadcast
                    // Check whether an exception was raised
                    BCAST_TAG tag;
                    MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
                    if (tag == BCAST_EXCEPTION) {
                        throw MAiNGOMpiException("  Worker " + std::to_string(_rank) + " received message about an exception during epsilon-constraint method.", MAiNGOMpiException::ORIGIN_OTHER);
                    }
#endif
                MAiNGO_END_IF
                *_maingoSettings = _maingoOriginalSettings;
    }
    MAiNGO_MPI_BARRIER

        if (status != INFEASIBLE)
    {
        // ---------------------------------------------------------------------------------
        // 3: Solve problems with epsilon-constraint
        // ---------------------------------------------------------------------------------
#ifdef HAVE_MAiNGO_MPI
        MAiNGO_IF_BAB_MANAGER
            for (size_t i = 0; i < nObj; i++) {
                MPI_Bcast(optimalObjectives[i].data(), nObj, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            }
            MAiNGO_ELSE
                optimalObjectives.resize(nObj);
                for (size_t i = 0; i < nObj; i++) {
                    optimalObjectives[i].resize(nObj);
                    MPI_Bcast(optimalObjectives[i].data(), nObj, MPI_DOUBLE, 0, MPI_COMM_WORLD);
                }
            MAiNGO_END_IF
#endif
            epsConModel->set_single_objective(false);
            epsConModel->set_objective_index(0);
            const size_t nPoints = _maingoSettings->EC_nPoints;
            for (size_t iEps = 1; iEps < nPoints - 1; iEps++) {
                MAiNGO_IF_BAB_MANAGER
                    // Reset timing for this run and give intermediate output
                    _preprocessTime        = get_cpu_time();
                    _solutionTimeWallClock = get_wall_time();
                    _print_message(std::string("*** Solving epsilon-constraint problem number " + std::to_string(iEps) + ". ***"));
                MAiNGO_END_IF
                for (size_t iObj = 0; iObj < nObj; iObj++) {
                    if (iObj != 0) {
                        epsilon[iObj] = optimalObjectives[iObj][iObj] + iEps * (optimalObjectives[0][iObj] - optimalObjectives[iObj][iObj]) / (nPoints - 1);
                    }
                }
                epsConModel->set_epsilon(epsilon);
                try {
                    _construct_DAG();
                }
                catch (const std::exception& e) {
                    MAiNGO_IF_BAB_MANAGER
                        std::ostringstream errmsg;
                        errmsg << e.what() << "\n  Encountered a fatal error during DAG construction.";
                        _write_files_error(errmsg.str());
                        throw MAiNGOException("  Encountered a fatal error during DAG construction.", e);
                        MAiNGO_ELSE
                            throw;
                        MAiNGO_END_IF
                }
                catch (...) {
                    MAiNGO_IF_BAB_MANAGER
                        _write_files_error("  Encountered an unknown fatal error during DAG construction.");
                        throw MAiNGOException("  Encountered an unknown fatal error during DAG construction.");
                        MAiNGO_ELSE
                            throw;
                        MAiNGO_END_IF
                }
                status = _analyze_and_solve_problem();
                MAiNGO_IF_BAB_MANAGER
                    // Print problem statistics, solution, additional output & CPU time.
                    _outputTime = get_cpu_time();
                    _print_statistics();
                    _print_solution();
                    _print_additional_output();
                    _print_time();
                    if (status == INFEASIBLE) {
                        _print_message(std::string("*** Error in epsilon-constraint: false infeasibility claim ***"));
#ifdef HAVE_MAiNGO_MPI
                        BCAST_TAG bcastTag = BCAST_EXCEPTION;
                        MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
                        break;
                    }
                    std::vector<double> tmpObjectives(nObj);
                    std::vector<std::pair<std::string, double>> tmpOutput = evaluate_additional_outputs_at_solution_point();
                    for (size_t jObj = 0; jObj < nObj; jObj++) {
                        tmpObjectives[jObj] = tmpOutput[tmpOutput.size() - nObj + jObj].second;
                    }
                    optimalObjectives.push_back(tmpObjectives);
                    solutionPoints.push_back(get_solution_point());
                    cpuTimeEpsCon += get_cpu_solution_time();
#ifdef HAVE_MAiNGO_MPI
                    BCAST_TAG bcastTag = BCAST_EVERYTHING_FINE;
                    MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
                    MAiNGO_ELSE    // Workers just wait for a broadcast
                        // Check whether an exception was raised
                        BCAST_TAG tag;
                        MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
                        if (tag == BCAST_EXCEPTION) {
                            throw MAiNGOMpiException("  Worker " + std::to_string(_rank) + " received message about an exception during epsilon-constraint method.", MAiNGOMpiException::ORIGIN_OTHER);
                        }
#endif
                    MAiNGO_END_IF
                    *_maingoSettings = _maingoOriginalSettings;
            }
    }

    // ---------------------------------------------------------------------------------
    // 4: Final Output
    // ---------------------------------------------------------------------------------
    MAiNGO_IF_BAB_MANAGER
        // Restore settings
        *_maingoSettings = _maingoOriginalSettings;
        // Write files
        _write_files();
        _write_epsilon_constraint_result(optimalObjectives, solutionPoints);
        // Print time (slight abuse of regular time variables...)
        _logger->print_message("\n  Overall time for epsilon constraint method:", VERB_NORMAL, BAB_VERBOSITY);
        _preprocessTime        = 0.;
        _babTime               = cpuTimeEpsCon;
        _outputTime            = get_cpu_time();
        _solutionTimeWallClock = wallTimeEpsCon;
        _print_time();
    MAiNGO_END_IF

    return _maingoStatus;
}


/////////////////////////////////////////////////////////////////////////
// recognize structure, set constraint properties, and invoke solution routine
RETCODE
MAiNGO::_analyze_and_solve_problem()
{

    // Proceed only if the problem is not already found to be infeasible because of constant, infeasible constraints (e.g., 2<=1; this is checked in _construct_DAG()) or inconsistent variable bounds (e.g., x in [0,-1]; this is checked in set_model)
    if (_constantConstraintsFeasible && _infeasibleVariables.empty()) {

        // ----------------------------------------------------------------------------------------------------
        // 3: Structure recognition (LP, MIP, QP, NLP, MINLP) and constraint properties (Linear, convex, etc.)
        // ----------------------------------------------------------------------------------------------------

        try {
            _recognize_structure();
            _set_constraint_properties();
            MAiNGO_MPI_BARRIER
        }
        catch (const std::exception& e) {
            MAiNGO_IF_BAB_MANAGER
                std::ostringstream errmsg;
                errmsg << e.what() << "\n  Encountered a fatal error during structure recognition.";
                _write_files_error(errmsg.str());
                throw MAiNGOException("  Encountered a fatal error during structure recognition.", e);
                MAiNGO_ELSE
                    throw;
                MAiNGO_END_IF
        }
        catch (...) {
            MAiNGO_IF_BAB_MANAGER
                _write_files_error("  Encountered an unknown fatal error during structure recognition.");
                throw MAiNGOException("  Encountered an unknown fatal error during structure recognition.");
                MAiNGO_ELSE
                    throw;
                MAiNGO_END_IF
        }

        // ---------------------------------------------------------------------------------
        // 4: Solve the problem
        // ---------------------------------------------------------------------------------
        switch (_problemStructure) {
#ifdef HAVE_CPLEX    // If we have CPLEX, we can use of it directly for problems of type LP, MIP, QP, or MIQP
            case LP:
                MAiNGO_IF_BAB_MANAGER
                    _logger->print_message("\n  Recognized the problem to be a linear program.\n", VERB_NORMAL, BAB_VERBOSITY);
#ifdef HAVE_GROWING_DATASETS
                    _logger->print_message("\n  Growing datasets will not be used.\n", VERB_NORMAL, BAB_VERBOSITY);
#endif    //HAVE_GROWING_DATASETS
                MAiNGO_END_IF
                return _solve_MIQP();
                break;
            case MIP:
                MAiNGO_IF_BAB_MANAGER
                    _logger->print_message("\n  Recognized the problem to be a mixed-integer linear program.\n", VERB_NORMAL, BAB_VERBOSITY);
#ifdef HAVE_GROWING_DATASETS
                    _logger->print_message("\n  Growing datasets will not be used.\n", VERB_NORMAL, BAB_VERBOSITY);
#endif    //HAVE_GROWING_DATASETS
                MAiNGO_END_IF
                return _solve_MIQP();
                break;
            case QP:
                MAiNGO_IF_BAB_MANAGER
                    _logger->print_message("\n  Recognized the problem to be a quadratic program.\n", VERB_NORMAL, BAB_VERBOSITY);
#ifdef HAVE_GROWING_DATASETS
                    _logger->print_message("\n  Growing datasets will not be used.\n", VERB_NORMAL, BAB_VERBOSITY);
#endif    //HAVE_GROWING_DATASETS
                MAiNGO_END_IF
                return _solve_MIQP();
                break;
            case MIQP:
                MAiNGO_IF_BAB_MANAGER
                    _logger->print_message("\n  Recognized the problem to be a mixed-integer quadratic program.\n", VERB_NORMAL, BAB_VERBOSITY);
#ifdef HAVE_GROWING_DATASETS
                    _logger->print_message("\n  Growing datasets will not be used.\n", VERB_NORMAL, BAB_VERBOSITY);
#endif    //HAVE_GROWING_DATASETS
                MAiNGO_END_IF
                return _solve_MIQP();
                break;
#else    // If we don't CPLEX, we only pass LPs to CLP and solve all other problems as general MINLP
            case LP:
                MAiNGO_IF_BAB_MANAGER
                    _logger->print_message("\n  Recognized the problem to be a linear program.\n", VERB_NORMAL, BAB_VERBOSITY);
#ifdef HAVE_GROWING_DATASETS
                    _logger->print_message("\n  Growing datasets will not be used.\n", VERB_NORMAL, BAB_VERBOSITY);
#endif    //HAVE_GROWING_DATASETS
                MAiNGO_END_IF
                return _solve_MIQP();
                break;
            case QP:
                _logger->print_message("\n  Recognized the problem to be a quadratic program, but no dedicated QP solver is available.\n  Solving it as an NLP.\n", VERB_NORMAL, BAB_VERBOSITY);
                _problemStructure = NLP;
                return _solve_MINLP();
            case MIP:
                _logger->print_message("\n  Recognized the problem to be a mixed-integer linear program, but no dedicated MILP solver is available.\n  Solving it as an MINLP.\n", VERB_NORMAL, BAB_VERBOSITY);
                _problemStructure = MINLP;
                return _solve_MINLP();
            case MIQP:
                _logger->print_message("\n  Recognized the problem to be a mixed-integer quadratic program, but no dedicated MIQP solver is available.\n  Solving it as an MINLP.\n", VERB_NORMAL, BAB_VERBOSITY);
                _problemStructure = MINLP;
                return _solve_MINLP();
#endif
            case NLP:
            case DNLP:
            case MINLP:
            default:
                return _solve_MINLP();
                break;
        }
    }
    else {
        _set_constraint_properties();
        _initialize_solve();    // Needed to properly clear everything
        _preprocessTime = get_cpu_time() - _preprocessTime;

        MAiNGO_IF_BAB_MANAGER
            _maingoStatus = INFEASIBLE;
        MAiNGO_END_IF
    }

    return _maingoStatus;
}


////////////////////////////////////////////////////////////////////////
// solve function for MIPs
RETCODE
MAiNGO::_solve_MIQP()
{

    MAiNGO_IF_BAB_MANAGER
        try {

            // ---------------------------------------------------------------------------------
            // 1: Pre-processing
            // ---------------------------------------------------------------------------------

            // 1a: Initialize  & start timing
            std::string aboutSolver;
#ifdef HAVE_CPLEX
            switch (_maingoSettings->LBP_solver) {
                case lbp::LBP_SOLVER_MAiNGO: {
                    aboutSolver                              = "    MAiNGO solver is not available as (mixed-integer) linear/quadratic solver. Calling CPLEX.\n";
                    _maingoSettings->UBP_solverPreprocessing = ubp::UBP_SOLVER_CPLEX;
                    break;
                }
                case lbp::LBP_SOLVER_INTERVAL: {
                    aboutSolver                              = "    Interval solver is not available as (mixed-integer) linear/quadratic solver. Calling CPLEX.\n";
                    _maingoSettings->UBP_solverPreprocessing = ubp::UBP_SOLVER_CPLEX;
                    break;
                }
                case lbp::LBP_SOLVER_CPLEX: {
                    aboutSolver                              = "    Calling CPLEX.\n";
                    _maingoSettings->UBP_solverPreprocessing = ubp::UBP_SOLVER_CPLEX;
                    break;
                }
                case lbp::LBP_SOLVER_CLP: {
                    if (_problemStructure > LP) {
                        aboutSolver                              = "    CLP is not available as (mixed-integer) linear/quadratic solver. Calling CPLEX.\n";
                        _maingoSettings->UBP_solverPreprocessing = ubp::UBP_SOLVER_CPLEX;
                    }
                    else {
                        aboutSolver                              = "    Calling CLP.\n";
                        _maingoSettings->UBP_solverPreprocessing = ubp::UBP_SOLVER_CLP;
                    }
                    break;
                }
                default: {
                    std::ostringstream errmsg;
                    errmsg << "    Error in _solve_MIQP: Unknown lower bounding solver: " << _maingoSettings->LBP_solver;
                    throw MAiNGOException(errmsg.str());
                }
            }
#else
            // It is not possible to reach this point with a problem which is not an LP due to the code in lines 564-601
            switch (_maingoSettings->LBP_solver) {
                case lbp::LBP_SOLVER_MAiNGO: {
                    aboutSolver                              = "    MAiNGO solver is not available as a linear solver. Calling CLP.\n";
                    _maingoSettings->UBP_solverPreprocessing = ubp::UBP_SOLVER_CLP;
                    break;
                }
                case lbp::LBP_SOLVER_INTERVAL: {
                    aboutSolver                              = "    Interval solver is not available as a linear solver. Calling CLP.\n";
                    _maingoSettings->UBP_solverPreprocessing = ubp::UBP_SOLVER_CLP;
                    break;
                }
                case lbp::LBP_SOLVER_CPLEX: {
                    aboutSolver                              = "    CPLEX is not available on your machine. Calling CLP.\n";
                    _maingoSettings->UBP_solverPreprocessing = ubp::UBP_SOLVER_CLP;
                    break;
                }
                case lbp::LBP_SOLVER_CLP: {
                    aboutSolver                              = "    Calling CLP.\n";
                    _maingoSettings->UBP_solverPreprocessing = ubp::UBP_SOLVER_CLP;
                    break;
                }
                default: {
                    std::ostringstream errmsg;
                    errmsg << "    Error in _solve_MIQP: Unknown lower bounding solver: " << _maingoSettings->LBP_solver;
                    throw MAiNGOException(errmsg.str());
                }
            }
#endif
            _print_third_party_software_miqp();
            _initialize_solve();
            _logger->print_message(aboutSolver, VERB_NORMAL, BAB_VERBOSITY);
            _preprocessTime = get_cpu_time() - _preprocessTime;

            // ---------------------------------------------------------------------------------
            // 2: Solve the problem
            // ---------------------------------------------------------------------------------
            _babTime    = get_cpu_time();
            _miqpStatus = _myUBSPre->solve(_rootNode, _solutionValue, _solutionPoint);
            _babTime    = get_cpu_time() - _babTime;

            // ---------------------------------------------------------------------------------
            // 3: Determine return code
            // ---------------------------------------------------------------------------------
            if (_miqpStatus == SUBSOLVER_FEASIBLE) {
                _maingoStatus = GLOBALLY_OPTIMAL;
            }
            else if (_miqpStatus == SUBSOLVER_INFEASIBLE) {
                _maingoStatus = INFEASIBLE;
                _solutionPoint.clear();
            }

#ifdef HAVE_MAiNGO_MPI
            BCAST_TAG bcastTag = BCAST_FEASIBLE;
            MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
        }
#ifdef HAVE_MAiNGO_MPI
        catch (MAiNGOMpiException& e) {
            BCAST_TAG bcastTag = BCAST_EXCEPTION;
            MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            std::ostringstream errmsg;
            errmsg << e.what() << "\n  Encountered a fatal error during MIQP solution.";
            _write_files_error(errmsg.str());
            throw MAiNGOException("  Encountered a fatal error during MIQP solution.", e);
        }
#endif
        catch (const std::exception& e) {
#ifdef HAVE_MAiNGO_MPI
            BCAST_TAG bcastTag = BCAST_EXCEPTION;
            MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
            std::ostringstream errmsg;
            errmsg << e.what() << "\n  Encountered a fatal error during MIQP solution.";
            _write_files_error(errmsg.str());
            throw MAiNGOException("  Encountered a fatal error during MIQP solution.", e);
        }
        catch (...) {
#ifdef HAVE_MAiNGO_MPI
            BCAST_TAG bcastTag = BCAST_EXCEPTION;
            MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
            _write_files_error("  Encountered an unknown fatal error during MIQP solution.");
            throw MAiNGOException("  Encountered an unknown fatal error during MIQP solution.");
        }
#ifdef HAVE_MAiNGO_MPI
        MAiNGO_ELSE    // Workers just wait for a broadcast
            // Check whether an exception was raised
            BCAST_TAG tag;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            if (tag == BCAST_EXCEPTION) {
                throw MAiNGOMpiException("  Worker " + std::to_string(_rank) + " received message about an exception during MIQP solution.", MAiNGOMpiException::ORIGIN_OTHER);
            }
        MAiNGO_END_IF
#endif
        return _maingoStatus;
}


////////////////////////////////////////////////////////////////////////
// solve function for MINLPs
RETCODE
MAiNGO::_solve_MINLP()
{

    try {

#ifdef HAVE_MAiNGO_MPI
        // Auxiliary variables for parallelization
        std::ostringstream mutestream;
        std::streambuf* coutBuf = std::cout.rdbuf();

        // Mute cout for workers
        MAiNGO_IF_BAB_WORKER
            std::cout.rdbuf(mutestream.rdbuf());
        MAiNGO_END_IF
#endif

        // ---------------------------------------------------------------------------------
        // 1: Pre-processing at root node
        // ---------------------------------------------------------------------------------

        // 1a: Initialize
        MAiNGO_IF_BAB_MANAGER
            _print_third_party_software_minlp();

            _logger->print_message("\n  Pre-processing at root node:\n", VERB_NORMAL, BAB_VERBOSITY);
            if (_maingoSettings->LBP_addAuxiliaryVars) {
                std::ostringstream ostr;
                if (_nvarLbd - _nvar == 1) {
                    ostr << "    Added " << _nvarLbd - _nvar << " auxiliary variable...\n";
                }
                else {
                    ostr << "    Added " << _nvarLbd - _nvar << " auxiliary variables...\n";
                }
                _logger->print_message(ostr.str(), VERB_NORMAL, BAB_VERBOSITY);
            }
            // This stands BEFORE _initialize_solve, since it is checked in _initialize_solve() whether the user has CPLEX installed
            _logger->print_message("    Initialize subsolvers...\n", VERB_NORMAL, BAB_VERBOSITY);
        MAiNGO_END_IF
        _initialize_solve();

        if (!_maingoSettings->PRE_pureMultistart) {

            // 1b: Check set options (large values in LP and additional option checks based on chosen lower bounding strategy)
            _myLBS->preprocessor_check_options(_rootNode);
            MAiNGO_MPI_BARRIER

                // 1c: Constraint propagation before a local search is executed
                if (_maingoSettings->BAB_constraintPropagation)
            {
                _root_constraint_propagation();
            }
            MAiNGO_MPI_BARRIER

                if (_rootConPropStatus != TIGHTENING_INFEASIBLE)
            {    // If we haven't proven infeasibility, continue

                // 1d: Optimization-based bound tightening (OBBT) at the root node considering feasibility only
                if (_maingoSettings->PRE_obbtMaxRounds > 0) {
                    _root_obbt_feasibility();
                }
                MAiNGO_MPI_BARRIER

                    if (_rootObbtStatus != TIGHTENING_INFEASIBLE)
                {    // If we haven't proven infeasibility, continue

                    // 1e: Try to get a good feasible point using a multi-start heuristic
                    _root_multistart();
                    MAiNGO_MPI_BARRIER

                        if (_rootMultistartStatus == SUBSOLVER_FEASIBLE && !_maingoSettings->terminateOnFeasiblePoint && _solutionValue > _maingoSettings->targetUpperBound)
                    {    // If we have found a feasible point, but it isn't good enough yet, continue

                        // 1f: Constraint propagation after a local search has been executed
                        if (_maingoSettings->BAB_constraintPropagation) {
                            _root_constraint_propagation();
                        }
                        MAiNGO_MPI_BARRIER

                            // 1g: OBBT at the root node considering both feasibility and optimality
                            if (_maingoSettings->PRE_obbtMaxRounds > 0)
                        {
                            _root_obbt_feasibility_optimality();
                        }
                        MAiNGO_MPI_BARRIER
                    }
                }
            }
        }
        else {
            // 1b-g alternative: multi-start only
            _root_multistart();
            MAiNGO_MPI_BARRIER
        }

        // 1h: Timing
        MAiNGO_IF_BAB_MANAGER
            _preprocessTime = get_cpu_time() - _preprocessTime;
            std::ostringstream outstr;
            outstr << "    CPU time: " << std::setprecision(6) << _preprocessTime << " s." << std::endl;
            outstr << "  Done." << std::endl;
            _logger->print_message(outstr.str(), VERB_NORMAL, BAB_VERBOSITY);
        MAiNGO_END_IF

#ifdef HAVE_MAiNGO_MPI
        MAiNGO_IF_BAB_WORKER
            // Turn on cout again for workers
            std::cout.rdbuf(coutBuf);
        MAiNGO_END_IF
#endif
        MAiNGO_MPI_BARRIER

            // ----------------- End 1: Pre-processing at root node ----------------------------


            // ---------------------------------------------------------------------------------
            // 2: Branch & Bound
            // ---------------------------------------------------------------------------------

            if (_rootConPropStatus != TIGHTENING_INFEASIBLE && _rootObbtStatus != TIGHTENING_INFEASIBLE && !_maingoSettings->PRE_pureMultistart && !(_maingoSettings->terminateOnFeasiblePoint && _rootMultistartStatus == SUBSOLVER_FEASIBLE) && _solutionValue > _maingoSettings->targetUpperBound)
        {
#ifdef HAVE_GROWING_DATASETS
            _myBaB->pass_datasets_to_bab(_datasets);

            //Change full dataset (root for pre-processing) to smallest reduced dataset (root of BaB) if these are different
            if (_ndata > 1) {
                _rootNode.set_index_dataset(1);
            }
#endif
            _logger->create_iterations_csv_file(_maingoSettings->writeCsv);
            _babStatus = _myBaB->solve(_rootNode, _solutionValue, _solutionPoint, _preprocessTime, _babTime);
            _babTime -= _preprocessTime;    // Get the B&B time only
        }
        // ------------------------- End 2: Branch & Bound ---------------------------------


        // ---------------------------------------------------------------------------------
        // 3: Determine return code
        // ---------------------------------------------------------------------------------
        MAiNGO_IF_BAB_MANAGER
            if (_rootObbtStatus == TIGHTENING_INFEASIBLE || _rootConPropStatus == TIGHTENING_INFEASIBLE) {
                _maingoStatus = INFEASIBLE;
            }
            else {
                if (_babStatus == babBase::enums::BAB_RETCODE::GLOBALLY_OPTIMAL) {
                    _maingoStatus = GLOBALLY_OPTIMAL;
                }
                else if (_babStatus == babBase::enums::BAB_RETCODE::INFEASIBLE) {
                    _maingoStatus = INFEASIBLE;
                }
                else if (_babStatus == babBase::enums::BAB_RETCODE::TARGET_UBD || _babStatus == babBase::enums::BAB_RETCODE::TARGET_LBD) {
                    _maingoStatus = BOUND_TARGETS;
                }
                else {
                    if (!_solutionPoint.empty()) {
                        if (_solutionValue <= _maingoSettings->targetUpperBound) {
                            _maingoStatus = BOUND_TARGETS;
                        }
                        else {
                            _maingoStatus = FEASIBLE_POINT;
                        }
                    }
                    else {
                        _maingoStatus = NO_FEASIBLE_POINT_FOUND;
                    }
                }
            }
        MAiNGO_END_IF

        // ----------------------------- End 3: Output -------------------------------------

        return _maingoStatus;
    }
#ifdef HAVE_MAiNGO_MPI
    catch (MAiNGOMpiException& e) {
        MAiNGO_IF_BAB_MANAGER
            std::ostringstream errmsg;
            errmsg << e.what() << "\n  Encountered a fatal error during solution.";
            _write_files_error(errmsg.str());
            throw MAiNGOException("  Encountered a fatal error during solution.", e);
            MAiNGO_ELSE
                throw;
            MAiNGO_END_IF
    }
#endif
    catch (const std::exception& e) {
        MAiNGO_IF_BAB_MANAGER
            std::ostringstream errmsg;
            errmsg << e.what() << "\n  Encountered a fatal error during solution.";
            _write_files_error(errmsg.str());
            throw MAiNGOException("  Encountered a fatal error during solution.", e);
            MAiNGO_ELSE
                throw;
            MAiNGO_END_IF
    }
    catch (...) {
        MAiNGO_IF_BAB_MANAGER
            _write_files_error("  Encountered an unknown fatal error during solution.");
            throw MAiNGOException("  Encountered an unknown fatal error during solution.");
            MAiNGO_ELSE
                throw;
            MAiNGO_END_IF
    }
}


/////////////////////////////////////////////////////////////////////////
// initializes internal model representation
void
MAiNGO::set_model(std::shared_ptr<MAiNGOmodel> myModel)
{

    // Set correct status
    MAiNGO_IF_BAB_MANAGER
        _maingoStatus = NOT_SOLVED_YET;
#ifdef HAVE_MAiNGO_MPI
        MAiNGO_ELSE
            _maingoStatus = JUST_A_WORKER_DONT_ASK_ME;
#endif
        MAiNGO_END_IF
        _problemStructure   = MINLP;    // default
        _feasibilityProblem = false;
        _readyToSolve       = false;
        _DAGconstructed     = false;

        // Store pointer to problem
        _myFFVARmodel = myModel;

        // Read optimization variables (and optionally initial point)
        _originalVariables = myModel->get_variables();
        if (_originalVariables.empty()) {
            throw MAiNGOException("  MAiNGO: Error while setting model: Empty vector of optimization variables.");
        }
        _initialPointOriginal = myModel->get_initial_point();
        if ((!_initialPointOriginal.empty()) && (_initialPointOriginal.size() != _originalVariables.size())) {
            std::ostringstream errmsg;
            errmsg << "  MAiNGO: Error while setting model: Dimension of initial guess (" << _initialPointOriginal.size() << ") is inconsistent with number of variables (" << _originalVariables.size() << ").";
            throw MAiNGOException(errmsg.str());
        }

        // Save the size of original variables, this is needed since some of the user-defined variables may be not used in the problem and will be eliminated when the DAG is constructed
        _nvarOriginal           = _originalVariables.size();
        _nvarOriginalContinuous = 0;
        _nvarOriginalBinary     = 0;
        _nvarOriginalInteger    = 0;
        for (size_t i = 0; i < _originalVariables.size(); i++) {
            switch (_originalVariables[i].get_variable_type()) {
                case babBase::enums::VT_CONTINUOUS:
                    _nvarOriginalContinuous++;
                    break;
                case babBase::enums::VT_BINARY:
                    _nvarOriginalBinary++;
                    break;
                case babBase::enums::VT_INTEGER:
                    _nvarOriginalInteger++;
                    break;
                default:
                    break;
            }
        }

        // Check if the specified variable bounds define a non-empty set
        _infeasibleVariables.clear();
        for (unsigned iVar = 0; iVar < _originalVariables.size(); ++iVar) {
            if (!_originalVariables.at(iVar).has_nonempty_host_set()) {
                _infeasibleVariables.push_back(&(_originalVariables.at(iVar)));
            }
        }

        // Confirm model is ready to use
        _readyToSolve = true;
}


////////////////////////////////////////////////////////////////////////
// construct DAG
void
MAiNGO::_construct_DAG()
{

    // Build temporary DAG from problem definition first (before getting rid of unused variables)
    mc::FFGraph tmpDAG;
    std::vector<mc::FFVar> tmpDAGVars;
    std::vector<mc::FFVar> tmpFunctions;
    // Declare the correct amount of DAG variables
    for (unsigned int i = 0; i < _nvarOriginal; i++) {
        mc::FFVar X;
        tmpDAGVars.push_back(X);
        // Set the variables as DAG variables
        tmpDAGVars[i].set(&tmpDAG);
    }

    _modelOutput.clear();
    try {
        _modelOutput = _myFFVARmodel->evaluate(tmpDAGVars);
#ifdef HAVE_GROWING_DATASETS
        _initialize_objective_from_objective_per_data();
#endif
    }
    catch (std::exception& e) {
        throw MAiNGOException("  MAiNGO: Error while evaluating specified model to construct DAG.", e);
    }
    catch (...) {
        throw MAiNGOException("  MAiNGO: Unknown error while evaluating specified model to construct DAG.");
    }

    _classify_objective_and_constraints(tmpFunctions, tmpDAGVars);
#ifdef HAVE_GROWING_DATASETS
    _initialize_dataset();
#endif

    // Recognize and remove variables that do not participate in the actual problem
    // Recognize first
    _removedVariables = std::vector<bool>(_nvarOriginal, false);
    _variables.clear();
    _variablesLbd.clear();
    mc::FFGraph::t_Vars Vars = tmpDAG.Vars();
    mc::FFGraph::it_Vars itv = Vars.begin();
    unsigned nRemoved        = 0;
    for (unsigned i = 0; itv != Vars.end() && (*itv)->id().first <= mc::FFVar::VAR; ++itv, ++i) {
        // It is possible that a variable is used alone in a constraint, e.g., x <= 0 or in any output (don't ask me why someone would do that but it is possible)
        // and we have to recognize that and not remove this constraint/variable
        bool used_in_functions = false;
        for (unsigned j = 0; j < tmpFunctions.size() && !used_in_functions; j++) {
            if (tmpFunctions[j].id() == (*itv)->id()) {
                used_in_functions = true;
            }
        }
        if ((*itv)->ops().second.empty() && !used_in_functions) {
            _removedVariables[i] = true;
            nRemoved++;
        }
        else {
            _variables.push_back(_originalVariables[i]);
            _variablesLbd.push_back(_originalVariables[i]);
        }
    }
    _nvar = _nvarOriginal - nRemoved;

    // Make actual DAG without these unnecessary variables
    _DAG.clear();
    _DAGvars.clear();
    unsigned iNewVars = 0;
    for (unsigned int iOldVars = 0; iOldVars < _nvarOriginal; iOldVars++) {
        if (!_removedVariables[iOldVars]) {
            mc::FFVar Y;                      // Create a new DAG variable
            _DAGvars.push_back(Y);            // Add the new DAG variable to the vars vector
            _DAGvars[iNewVars].set(&_DAG);    // Add the new DAG variable to the DAG
            iNewVars++;
        }
    }
    for (int i = _nvarOriginal - 1; i >= 0; i--) {
        if (_removedVariables[i]) {
            tmpDAGVars.erase(tmpDAGVars.begin() + i);
        }
    }
    // Re-evaluate the DAG to recognize hidden zeros
    std::vector<mc::FFVar> tmpDAGoutputFunctions;
    bool foundHiddenZero = true;
    while (foundHiddenZero) {    // Re-evaluate until no more hidden zeros are found
        for (size_t i = 0; i < tmpDAGoutputFunctions.size(); i++) {
            tmpFunctions.push_back(tmpDAGoutputFunctions[i]);
        }
        mc::FFSubgraph tmpSubgraph = tmpDAG.subgraph(tmpFunctions.size(), tmpFunctions.data());
        std::vector<mc::FFVar> tmpDummy(tmpFunctions.size());
        _resultVars.clear();
        _resultVars.resize(tmpFunctions.size());
        tmpDAG.eval(tmpSubgraph, tmpDummy, tmpFunctions.size(), tmpFunctions.data(), _resultVars.data(), tmpDAGVars.size(), tmpDAGVars.data(), tmpDAGVars.data());    // Get functions
        tmpFunctions.clear();
        tmpDAGoutputFunctions.clear();
        foundHiddenZero = _check_for_hidden_zero_constraints(tmpDAGVars, tmpFunctions, tmpDAGoutputFunctions);
    }

    // After no more hidden zero are found, construct the actual DAG
    for (size_t i = 0; i < tmpDAGoutputFunctions.size(); i++) {
        tmpFunctions.push_back(tmpDAGoutputFunctions[i]);
    }
    mc::FFSubgraph tmpSubgraph = tmpDAG.subgraph(tmpFunctions.size(), tmpFunctions.data());
    std::vector<mc::FFVar> tmpDummy(tmpFunctions.size());
    _resultVars.clear();
    _resultVars.resize(tmpFunctions.size());
    tmpDAG.eval(tmpSubgraph, tmpDummy, tmpFunctions.size(), tmpFunctions.data(), _resultVars.data(), tmpDAGVars.size(), tmpDAGVars.data(), _DAGvars.data());    // Get functions

    _DAGfunctions.clear();
    _DAGoutputFunctions.clear();
    // Just to make sure, check one last time
    _check_for_hidden_zero_constraints(_DAGvars, _DAGfunctions, _DAGoutputFunctions);

    // Set initial point properly -- remove not used variables
    _initialPoint.clear();
    for (unsigned int i = 0; i < _initialPointOriginal.size(); i++) {
        if (!_removedVariables[i]) {
            _initialPoint.push_back(_initialPointOriginal[i]);
        }
    }

    _DAGlbd.clear();
    _DAGvarsLbd.clear();
    _DAGfunctionsLbd.clear();
    _DAGoutputFunctionsLbd.clear();
    _nvarLbd              = _nvar;
    _nauxiliaryRelOnlyEqs = 0;
    if (_maingoSettings->LBP_addAuxiliaryVars) {
        for (size_t i = 0; i < _DAGvars.size(); i++) {
            mc::FFVar Y;                     // Create a new DAG variable
            _DAGvarsLbd.push_back(Y);        // Add the new DAG variable to the vars vector
            _DAGvarsLbd[i].set(&_DAGlbd);    // Add the new DAG variable to the DAG
        }

        _resultVars.clear();
        _resultVars.resize(tmpFunctions.size());
        tmpDAG.eval(tmpSubgraph, tmpDummy, tmpFunctions.size(), tmpFunctions.data(), _resultVars.data(), tmpDAGVars.size(), tmpDAGVars.data(), _DAGvarsLbd.data());    // Get functions

        // Just to make sure, check one last time
        _check_for_hidden_zero_constraints(_DAGvarsLbd, _DAGfunctionsLbd, _DAGoutputFunctionsLbd);

        try {
            _add_auxiliary_variables_to_lbd_dag();
        }
        catch (const filib::interval_io_exception& e) {
            MAiNGO_IF_BAB_MANAGER
                const std::string errmsg = "  Encountered a fatal error in intervals while adding auxiliary variables to the DAG used for lower bounding.";
                std::ostringstream completeMessage;
                completeMessage << e.what() << std::endl
                                << errmsg;
                _write_files_error(completeMessage.str());
                throw MAiNGOException(completeMessage.str());
                MAiNGO_ELSE
                    throw;
                MAiNGO_END_IF
        }
        catch (const MC::Exceptions& e) {
            MAiNGO_IF_BAB_MANAGER
                const std::string errmsg = "  Encountered a fatal error in McCormick relaxations while adding auxiliary variables to the DAG used for lower bounding.";
                std::ostringstream completeMessage;
                completeMessage << e.what() << std::endl
                                << errmsg;
                _write_files_error(completeMessage.str());
                throw MAiNGOException(completeMessage.str());
                MAiNGO_ELSE
                    throw;
                MAiNGO_END_IF
        }
        catch (const vMC::Exceptions& e) {
            MAiNGO_IF_BAB_MANAGER
                const std::string errmsg = "  Encountered a fatal error in vMcCormick relaxations while adding auxiliary variables to the DAG used for lower bounding.";
                std::ostringstream completeMessage;
                completeMessage << e.what() << std::endl
                                << errmsg;
                _write_files_error(completeMessage.str());
                throw MAiNGOException(completeMessage.str());
                MAiNGO_ELSE
                    throw;
                MAiNGO_END_IF
        }
        catch (const std::exception& e) {
            MAiNGO_IF_BAB_MANAGER
                const std::string errmsg = "  Encountered a fatal error while adding auxiliary variables to the DAG used for lower bounding.";
                std::ostringstream completeMessage;
                completeMessage << e.what() << std::endl
                                << errmsg;
                _write_files_error(completeMessage.str());
                throw MAiNGOException(errmsg, e);
                MAiNGO_ELSE
                    throw;
                MAiNGO_END_IF
        }
        catch (...) {
            MAiNGO_IF_BAB_MANAGER
                const std::string errmsg = "  Encountered an unknown fatal error while adding auxiliary variables to the DAG used for lower bounding.";
                _write_files_error(errmsg);
                throw MAiNGOException(errmsg);
                MAiNGO_ELSE
                    throw;
                MAiNGO_END_IF
        }
    }

    _DAGconstructed = true;
    // ----- debugging purposes ----
    // std::ofstream o_F("DAG.txt", std::ios_base::out);
    // o_F<< _DAG <<std::endl;
    // print DAG as dot file, it can be converted to a nice image with a dot script, which can be found, e.g., on the RWTH cluster
    // std::ofstream o_F("F.dot", std::ios_base::out);
    // _DAG.dot_script(_DAGfunctions.size(), _DAGfunctions.data(), o_F);
    // o_F.close();
}


////////////////////////////////////////////////////////////////////////
// initializes subsolvers and internal solution variables for NLPs and MINLPs
void
MAiNGO::_initialize_solve()
{

    // Initialize subsolvers (upper bounding is always needed, lower bounding and B&B are not)
    _myUBSPre = ubp::make_ubp_solver(_DAG, _DAGvars, _DAGfunctions, _variables, _nineq, _neq, _nineqSquash, _maingoSettings, _logger, _nonconstantConstraintsUBP, ubp::UpperBoundingSolver::USE_PRE);
#ifdef HAVE_GROWING_DATASETS
    //objective per data saved after obj and non-constant constraints
    _myUBSPre->pass_data_position_to_solver(_datasets, 1 + _nineq + _neq + _nineqSquash);
#endif    // HAVE_GROWING_DATASETS

    _myUBSBab = nullptr;
    _myLBS    = nullptr;
    _myBaB    = nullptr;
    if (_problemStructure >= NLP) {
        if (!_maingoSettings->PRE_pureMultistart) {    // For a pure multistart, lower bounding solver and the B&B tree are not needed
            _myUBSBab = ubp::make_ubp_solver(_DAG, _DAGvars, _DAGfunctions, _variables, _nineq, _neq, _nineqSquash, _maingoSettings, _logger, _nonconstantConstraintsUBP, ubp::UpperBoundingSolver::USE_BAB);
            if (_maingoSettings->LBP_addAuxiliaryVars) {
                _myLBS = lbp::make_lbp_solver(_DAGlbd, _DAGvarsLbd, _DAGfunctionsLbd, _variablesLbd, _nineq, _neq, _nineqRelaxationOnly, _neqRelaxationOnly + _nauxiliaryRelOnlyEqs,
                                              _nineqSquash, _maingoSettings, _logger, _nonconstantConstraints);
            }
            else {
                _myLBS = lbp::make_lbp_solver(_DAG, _DAGvars, _DAGfunctions, _variables, _nineq, _neq, _nineqRelaxationOnly, _neqRelaxationOnly,
                                              _nineqSquash, _maingoSettings, _logger, _nonconstantConstraints);
            }
#ifdef HAVE_GROWING_DATASETS
            //objective per data saved after obj and non-constant constraints
            _myUBSBab->pass_data_position_to_solver(_datasets, 1 + _nineq + _neq + _nineqSquash);
            _myLBS->pass_data_position_to_solver(_datasets, 1 + _nineq + _neq + _nineqSquash + _nineqRelaxationOnly + _neqRelaxationOnly + _nauxiliaryRelOnlyEqs);
#endif    // HAVE_GROWING_DATASETS

            _myBaB = std::make_shared<bab::BranchAndBound>(_variablesLbd, _myLBS, _myUBSBab, _maingoSettings, _logger, /*number of variables w/o auxiliaries*/ _nvar);

#if defined(MAiNGO_DEBUG_MODE) && defined(HAVE_GROWING_DATASETS)
            _myLBSFull = nullptr;
            if (_maingoSettings->LBP_addAuxiliaryVars) {
                _myLBSFull = lbp::make_lbp_solver(_DAGlbd, _DAGvarsLbd, _DAGfunctionsLbd, _variablesLbd, _nineq, _neq, _nineqRelaxationOnly, _neqRelaxationOnly + _nauxiliaryRelOnlyEqs,
                                                  _nineqSquash, _maingoSettings, _logger, _nonconstantConstraints);
            }
            else {
                _myLBSFull = lbp::make_lbp_solver(_DAG, _DAGvars, _DAGfunctions, _variables, _nineq, _neq, _nineqRelaxationOnly, _neqRelaxationOnly,
                                                  _nineqSquash, _maingoSettings, _logger, _nonconstantConstraints);
            }
            _myBaB->pass_LBSFull_to_bab(_myLBSFull);
#endif
        }
    }


    // Initialize solution variables
    _solutionPoint.clear();
    _solutionValue = _maingoSettings->infinity;
    _babTime       = 0.;

    // Initialize status
    MAiNGO_IF_BAB_MANAGER
        _maingoStatus = NO_FEASIBLE_POINT_FOUND;
#ifdef HAVE_MAiNGO_MPI
        MAiNGO_ELSE
            _maingoStatus = JUST_A_WORKER_DONT_ASK_ME;
#endif
        MAiNGO_END_IF
        _rootObbtStatus       = TIGHTENING_UNCHANGED;
        _rootConPropStatus    = TIGHTENING_UNCHANGED;
        _rootMultistartStatus = SUBSOLVER_INFEASIBLE;
        _miqpStatus           = SUBSOLVER_INFEASIBLE;
        _babStatus            = babBase::enums::NOT_SOLVED_YET;

        // Initialize root node
        // with full dataset (MAiNGO with growing datasets)
        if (_maingoSettings->LBP_addAuxiliaryVars) {
            _rootNode = babBase::BabNode(-_maingoSettings->infinity, _variablesLbd, 0 /*index dataset*/, 0 /*ID*/, 0 /* depth */, false /*augment data*/);
        }
        else {
            _rootNode = babBase::BabNode(-_maingoSettings->infinity, _variables, 0 /*index dataset*/, 0 /*ID*/, 0 /* depth */, false /*augment data*/);
        }

        // Clear logging (except for settings)
        _objectivesAtRoot.clear();
        _feasibleAtRoot.clear();
        _initialPointFeasible = false;

        // Tell user about changed variable bounds
        for (size_t i = 0; i < _originalVariables.size(); i++) {
            std::string variableType = "";
            switch (_originalVariables[i].get_variable_type()) {
                case babBase::enums::VT_BINARY:
                    variableType = "binary";
                    break;
                case babBase::enums::VT_INTEGER:
                    variableType = "integer";
                    break;
                default:
                    break;
            }
            if (_originalVariables[i].bounds_changed_from_user_input()) {
                std::ostringstream ostr;
                ostr << "    Changing bounds of " << variableType << " variable " << _originalVariables[i].get_name() << " from "
                     << "[" << _originalVariables[i].get_user_lower_bound() << ", " << _originalVariables[i].get_user_upper_bound() << "] to "
                     << "[" << _originalVariables[i].get_lower_bound() << ", " << _originalVariables[i].get_upper_bound() << "].\n";
                _logger->print_message(ostr.str(), VERB_NORMAL, BAB_VERBOSITY);
            }
        }

        std::srand(42);    // For reproducible results despite (pseudo-)random starting points
}


////////////////////////////////////////////////////////////////////////
// conducts feasibility-based bound tightening at the root node
void
MAiNGO::_root_obbt_feasibility()
{

    MAiNGO_IF_BAB_MANAGER
        _logger->print_message("    Optimization-based bound tightening (feasibility only)...\n", VERB_NORMAL, BAB_VERBOSITY);

        for (unsigned iLP = 0; iLP < _maingoSettings->PRE_obbtMaxRounds; iLP++) {

            _logger->print_message("        Run " + std::to_string(iLP + 1) + "\n", VERB_ALL, BAB_VERBOSITY);
            try {
                _rootObbtStatus = _myLBS->solve_OBBT(_rootNode, _maingoSettings->infinity, lbp::OBBT_FEAS);
            }
            catch (std::exception& e) {
#ifdef HAVE_MAiNGO_MPI
                // Inform workers about exceptions
                BCAST_TAG bcastTag = BCAST_EXCEPTION;
                MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
                throw MAiNGOException("  Encountered a fatal error during feasibility-based OBBT during pre-processing.", e);
            }
            catch (...) {
#ifdef HAVE_MAiNGO_MPI
                // Inform workers about exceptions
                BCAST_TAG bcastTag = BCAST_EXCEPTION;
                MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
                throw MAiNGOException("  Encountered an unknown fatal error during feasibility-based OBBT during pre-processing.");
            }
            // If we make no more progress or prove infeasibility, terminate
            if ((_rootObbtStatus == TIGHTENING_INFEASIBLE) || (_rootObbtStatus == TIGHTENING_UNCHANGED)) {
                break;
            }
        }

        if (_rootObbtStatus == TIGHTENING_INFEASIBLE) {
            _logger->print_message("      Found problem to be infeasible.\n", VERB_NORMAL, BAB_VERBOSITY);
        }
#ifdef HAVE_MAiNGO_MPI
        // Send results to workers
        if (_rootObbtStatus == TIGHTENING_INFEASIBLE) {
            BCAST_TAG tag = BCAST_INFEASIBLE;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
        }
        else {
            BCAST_TAG tag = BCAST_FEASIBLE;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            for (unsigned int i = 1; i < (unsigned int)_nProcs; i++) {
                send_babnode(_rootNode, i);
            }
        }
        MAiNGO_ELSE    // MAiNGO_IF_BAB_WORKER
            // Check whether an exception was raised
            BCAST_TAG tag;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            if (tag == BCAST_EXCEPTION) {
                throw MAiNGOMpiException("  Worker " + std::to_string(_rank) + " received message about an exception during feasibility-based OBBT during pre-processing.", MAiNGOMpiException::ORIGIN_OTHER);
            }
            else if (tag == BCAST_INFEASIBLE) {
                _rootObbtStatus = TIGHTENING_INFEASIBLE;
            }
            else {
                recv_babnode(_rootNode, 0, _nvarLbd);
            }
#endif
        MAiNGO_END_IF
}


////////////////////////////////////////////////////////////////////////
// conducts feasibility- and optimality-based bound tightening at the root node
void
MAiNGO::_root_obbt_feasibility_optimality()
{

    MAiNGO_IF_BAB_MANAGER
        _logger->print_message("    Optimization-based bound tightening (feasibility and optimality)...\n", VERB_NORMAL, BAB_VERBOSITY);

        babBase::BabNode tmpNode(_rootNode);
        try {
            _rootObbtStatus = _myLBS->solve_OBBT(tmpNode, _solutionValue, lbp::OBBT_FEASOPT);
        }
        catch (std::exception& e) {
#ifdef HAVE_MAiNGO_MPI
            // Inform workers about exceptions
            BCAST_TAG bcastTag = BCAST_EXCEPTION;
            MPI_Bcast(&bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
            throw MAiNGOException("  Encountered a fatal error during feasibility- and optimality-based OBBT during pre-processing.", e);
        }
        catch (...) {
#ifdef HAVE_MAiNGO_MPI
            BCAST_TAG tag = BCAST_EXCEPTION;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
            throw MAiNGOException("  Encountered an unknown fatal error during feasibility- and optimality-based OBBT during pre-processing.");
        }

        if (_rootObbtStatus == TIGHTENING_INFEASIBLE) {
            std::string str = "      Warning: OBBT declared the problem infeasible although a feasible point was found.\n";
            str += "               This may be caused by numerical difficulties or an isolated optimum in your model.\n";
            str += "               Turning off OBBT, restoring valid bounds and proceeding...\n";
            _logger->print_message(str, VERB_NORMAL, BAB_VERBOSITY);
            _maingoSettings->PRE_obbtMaxRounds   = 0;
            _maingoSettings->BAB_alwaysSolveObbt = false;
            _rootObbtStatus                      = TIGHTENING_UNCHANGED;
#ifdef HAVE_MAiNGO_MPI
            BCAST_TAG tag = BCAST_TIGHTENING_INFEASIBLE;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
        }
        else if (_rootObbtStatus == TIGHTENING_UNCHANGED) {
            BCAST_TAG tag = BCAST_FEASIBLE;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
        }
        else if (_rootObbtStatus == TIGHTENING_CHANGED) {
            _rootNode = tmpNode;
#ifdef HAVE_MAiNGO_MPI
            BCAST_TAG tag = BCAST_FEASIBLE;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            // Manager does not send the root node to workers, since they will get the node in the B&B algorithm
#endif
        }
#ifdef HAVE_MAiNGO_MPI
        MAiNGO_ELSE    // MAiNGO_IF_BAB_WORKER
            // Check whether an exception was raised or if tightening provided an incorrect claim
            BCAST_TAG tag;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            if (tag == BCAST_EXCEPTION) {
                throw MAiNGOMpiException("  Worker " + std::to_string(_rank) + " received message about an exception during feasibility- and optimality-based during pre-processing.", MAiNGOMpiException::ORIGIN_OTHER);
            }
            else if (tag == BCAST_TIGHTENING_INFEASIBLE) {
                _maingoSettings->PRE_obbtMaxRounds   = 0;
                _maingoSettings->BAB_alwaysSolveObbt = 0;
            }
            // Note that workers don't need the possibly changed node, since they will get new nodes in the B&B algorithm
#endif
        MAiNGO_END_IF    //MAiNGO_IF_BAB_MANAGER
}


////////////////////////////////////////////////////////////////////////
// conducts constraint propagation at root node
void
MAiNGO::_root_constraint_propagation()
{

    MAiNGO_IF_BAB_MANAGER
        _logger->print_message("    Constraint propagation...\n", VERB_NORMAL, BAB_VERBOSITY);

        babBase::BabNode tmpNode(_rootNode);
        if (_rootMultistartStatus == SUBSOLVER_FEASIBLE) {
            _rootConPropStatus = _myLBS->do_constraint_propagation(tmpNode, _solutionValue, 30);
        }
        else {
            _rootConPropStatus = _myLBS->do_constraint_propagation(tmpNode, _maingoSettings->infinity, 30);
        }

        // If we prove infeasibility, don't overwrite root node
        if (_rootConPropStatus == TIGHTENING_INFEASIBLE) {
            // Don't overwrite root node
            if (_rootMultistartStatus == SUBSOLVER_FEASIBLE) {    // Something went wrong
                std::string str = "      Warning: Constraint propagation declared the problem infeasible although a feasible point was found.\n";
                str += "               This may be caused by numerical difficulties.\n";
                str += "               Turning off constraint propagation, restoring valid bounds and proceeding...\n";
                _logger->print_message(str, VERB_NORMAL, BAB_VERBOSITY);
                _maingoSettings->BAB_constraintPropagation = false;
                _rootConPropStatus                         = TIGHTENING_UNCHANGED;
#ifdef HAVE_MAiNGO_MPI
                BCAST_TAG tag = BCAST_CONSTR_PROP_INFEASIBLE;
                MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
            }
            else {
                _logger->print_message("      Found problem to be infeasible.\n", VERB_NORMAL, BAB_VERBOSITY);
#ifdef HAVE_MAiNGO_MPI
                BCAST_TAG tag = BCAST_INFEASIBLE;
                MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
            }
        }
        else if (_rootConPropStatus == TIGHTENING_CHANGED) {
            _rootNode = tmpNode;
#ifdef HAVE_MAiNGO_MPI
            BCAST_TAG tag = BCAST_FEASIBLE;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
#endif
        }
#ifdef HAVE_MAiNGO_MPI
        else {
            BCAST_TAG tag = BCAST_FEASIBLE;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
        }
        MAiNGO_ELSE    // MAiNGO_IF_BAB_WORKER
            // Check what happened
            BCAST_TAG tag;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            if (tag == BCAST_CONSTR_PROP_INFEASIBLE) {
                _maingoSettings->BAB_constraintPropagation = false;
            }
            else if (tag == BCAST_INFEASIBLE) {
                _rootConPropStatus = TIGHTENING_INFEASIBLE;
            }
            // Note that workers don't need the possibly changed node, since they will get new nodes in the B&B algorithm or before multistart in root_feas_obbt
#endif
        MAiNGO_END_IF    //MAiNGO_IF_BAB_MANAGER
}


////////////////////////////////////////////////////////////////////////
// conducts multistart local search at the root node
void
MAiNGO::_root_multistart()
{

    MAiNGO_IF_BAB_MANAGER
        if (_maingoSettings->PRE_pureMultistart) {
            if (_maingoSettings->PRE_maxLocalSearches > 0) {
                std::ostringstream outstr;
                outstr << "    Multistart with " << _maingoSettings->PRE_maxLocalSearches << " initial points...\n";
                _logger->print_message(outstr.str(), VERB_NORMAL, BAB_VERBOSITY);
            }
            else {
                // users... :-/
                _logger->print_message("    Requested pure multistart with 0 local searches. Only checking user-specified initial point for feasibility ...\n", VERB_NORMAL, BAB_VERBOSITY);
            }
        }
        else if (_maingoSettings->PRE_maxLocalSearches > 0) {
            _logger->print_message("    Multistart local searches...\n", VERB_NORMAL, BAB_VERBOSITY);
        }
        else if (_initialPoint.size() == _nvar) {
            _logger->print_message("    Checking user-specified initial point...\n", VERB_NORMAL, BAB_VERBOSITY);
        }
    MAiNGO_END_IF
    _solutionPoint        = _initialPoint;
    _rootMultistartStatus = _myUBSPre->multistart(_rootNode, _solutionValue, _solutionPoint, _feasibleAtRoot, _objectivesAtRoot, _initialPointFeasible);

#ifdef HAVE_MAiNGO_MPI
    MAiNGO_IF_BAB_MANAGER
        if (_rootMultistartStatus == SUBSOLVER_INFEASIBLE) {
            BCAST_TAG tag = BCAST_INFEASIBLE;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
        }
        else {
            BCAST_TAG tag = BCAST_FEASIBLE;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            MPI_Bcast(&_solutionValue, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
        }
        MAiNGO_ELSE
            // Process results
            BCAST_TAG tag;
            MPI_Bcast(&tag, 1, MPI_INT, 0, MPI_COMM_WORLD);
            if (tag == BCAST_INFEASIBLE) {
                _rootMultistartStatus = SUBSOLVER_INFEASIBLE;
            }
            else {
                _rootMultistartStatus = SUBSOLVER_FEASIBLE;
                MPI_Bcast(&_solutionValue, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);
            }
        MAiNGO_END_IF
#endif

        MAiNGO_IF_BAB_MANAGER
            if (_rootMultistartStatus == SUBSOLVER_INFEASIBLE) {
                _solutionPoint.clear();
            }
            else {
                if (!_maingoSettings->PRE_pureMultistart) {
                    _myLBS->update_incumbent_LBP(_solutionPoint);
                }
            }

            // Check whether the incumbent fullfils relaxation only constraints
            if (_rootMultistartStatus == SUBSOLVER_FEASIBLE && (_nineqRelaxationOnly > 0 || _neqRelaxationOnly > 0)) {    // Note that constant functions have been checked in _constructDAG
                std::string str;
                std::string whitespaces = "      ";
                _check_feasibility_of_relaxation_only_constraints(_solutionPoint, str, whitespaces);
                _logger->print_message(str, VERB_NORMAL, BAB_VERBOSITY);
            }
        MAiNGO_END_IF
}


////////////////////////////////////////////////////////////////////////
// recognizes structure of the problem
void
MAiNGO::_recognize_structure()
{

    _problemStructure = LP;

    // Get dependency sets of all functions
    // Note that we don't care about relaxation only (in)equalities and output
    std::vector<std::map<int, int>> func_dep;
    func_dep.resize(1 + _nineq + _neq);
    for (unsigned int i = 0; i < 1 + _nineq + _neq; i++) {
        func_dep[i] = _DAGfunctions[i].dep().dep();
    }
    std::vector<mc::FFDep::TYPE> functionsStructure(1 + _nineq + _neq, mc::FFDep::L);

    // Check if it is a mixed-integer program
    bool integer = false;
    for (unsigned int i = 0; i < _nvar && !integer; i++) {
        if (_variables[i].get_variable_type() > babBase::enums::VT_CONTINUOUS) {
            integer = true;
        }
    }

    // Set problem structure
    for (unsigned int i = 0; i < 1 + _nineq + _neq; i++) {
        for (unsigned int j = 0; j < _nvar; j++) {
            auto ito = func_dep[i].find(j);
            if (ito != func_dep[i].end()) {
                mc::FFDep::TYPE variableDep = (mc::FFDep::TYPE)(ito->second);
                if (functionsStructure[i] < variableDep) {
                    functionsStructure[i] = variableDep;
                }
            }
        }

        PROBLEM_STRUCTURE temp;
        switch (functionsStructure[i]) {
            case mc::FFDep::L:
                temp = integer ? MIP : LP;
                break;
            case mc::FFDep::B:
            case mc::FFDep::Q:
                // Check for quadratic inequalities or equalities <- they have to be convex, otherwise we get a CPLEX error
                if (i > 0) {    // i>0 are (in)equalities
                    temp = integer ? MINLP : NLP;
                }
                else {
                    temp = integer ? MIQP : QP;
                }
                break;
            case mc::FFDep::P:
            case mc::FFDep::R:
            case mc::FFDep::N:
                temp = integer ? MINLP : NLP;
                break;
            case mc::FFDep::D:
                temp = integer ? MINLP : DNLP;
                break;
            default:
                temp = integer ? MINLP : NLP;
                break;
        }
        _problemStructure = std::max(_problemStructure, temp);
    }

    switch (_problemStructure) {
        case LP:
            _logger->print_message("\n  The problem is an LP", VERB_ALL, BAB_VERBOSITY);
            break;
        case MIP:
            _logger->print_message("\n  The problem is an MIP", VERB_ALL, BAB_VERBOSITY);
            break;
        case QP:
            _logger->print_message("\n  The problem is a QP", VERB_ALL, BAB_VERBOSITY);
            break;
        case MIQP:
            _logger->print_message("\n  The problem is an MIQP", VERB_ALL, BAB_VERBOSITY);
            break;
        case NLP:
            _logger->print_message("\n  The problem is an NLP", VERB_ALL, BAB_VERBOSITY);
            break;
        case DNLP:
            _logger->print_message("\n  The problem is a DNLP", VERB_ALL, BAB_VERBOSITY);
            break;
        case MINLP:
            _logger->print_message("\n  The problem is an MINLP", VERB_ALL, BAB_VERBOSITY);
            break;
        default:
            _logger->print_message("\n  Could not recognize structure", VERB_ALL, BAB_VERBOSITY);
            break;
    }
}


////////////////////////////////////////////////////////////////////////
// check if point satisfies relaxation only constraints and give a warning if not
bool
MAiNGO::_check_feasibility_of_relaxation_only_constraints(const std::vector<double>& solutionPoint, std::string& str, const std::string& whitespaces)
{

    bool isFeasible;
    std::vector<double> modelValues;
    std::tie(modelValues, isFeasible) = _evaluate_model_at_point(solutionPoint);
    std::vector<unsigned> infeasibleRelOnlyIneqs;
    std::vector<unsigned> infeasibleRelOnlyEqs;
    const unsigned startingIndex = 1 + _nineq + _nconstantIneq + _neq + _nconstantEq;
    if (!isFeasible) {
        // Since the UBS found a feasible point, the point can only be infeasible in the relaxation only constraints
        // Relaxation only inequalities
        for (unsigned i = 0; i < _nineqRelaxationOnly + _nconstantIneqRelOnly; i++) {
            if (modelValues[i + startingIndex] > _maingoSettings->deltaIneq) {
                infeasibleRelOnlyIneqs.push_back(i);
                isFeasible = false;
            }
        }
        // Relaxations only equalities
        for (unsigned int i = 0; i < _neqRelaxationOnly + _nconstantEqRelOnly; i++) {
            if (modelValues[i + startingIndex + _nineqRelaxationOnly + _nconstantIneqRelOnly] > _maingoSettings->deltaEq || modelValues[i + startingIndex + _nineqRelaxationOnly + _nconstantIneqRelOnly] < -_maingoSettings->deltaEq) {
                infeasibleRelOnlyEqs.push_back(i);
                isFeasible = false;
            }
        }
    }
    if (infeasibleRelOnlyIneqs.size() > 0 || infeasibleRelOnlyEqs.size() > 0) {
        std::ostringstream outstr;
        if (infeasibleRelOnlyIneqs.size() > 0) {
            if (infeasibleRelOnlyIneqs.size() == 1) {
                outstr << whitespaces << "Warning: Current best feasible point does not satisfy relaxation only inequality";
            }
            else {
                outstr << whitespaces << "Warning: Current best feasible point does not satisfy relaxation only inequalities";
            }
            // Write all violated relaxation only inequalities
            for (size_t i = 0; i < infeasibleRelOnlyIneqs.size(); i++) {
                outstr << "\n"
                       << whitespaces << "         number " << infeasibleRelOnlyIneqs[i] + 1
                       << " (violation = " << std::setprecision(16) << modelValues[infeasibleRelOnlyIneqs[i] + startingIndex]
                       << " > " << std::setprecision(9) << _maingoSettings->deltaIneq << " = deltaIneq)";
            }
            outstr << ".\n";
        }
        if (infeasibleRelOnlyEqs.size() > 0) {
            if (infeasibleRelOnlyEqs.size() == 1) {
                outstr << whitespaces << "Warning: Current best feasible point does not satisfy relaxation only equality";
            }
            else {
                outstr << whitespaces << "Warning: Current best feasible point does not satisfy relaxation only equalities";
            }
            // Write all violated relaxation only equalities
            for (size_t i = 0; i < infeasibleRelOnlyEqs.size(); i++) {
                outstr << "\n"
                       << whitespaces << "         number " << infeasibleRelOnlyEqs[i] + 1
                       << " (violation = " << std::setprecision(9) << modelValues[infeasibleRelOnlyEqs[i] + startingIndex + _nineqRelaxationOnly + _nconstantIneqRelOnly]
                       << " not in [-" << std::setprecision(9) << _maingoSettings->deltaEq << "," << std::setprecision(9) << _maingoSettings->deltaEq << "] = deltaEq)";
            }
            outstr << ".\n";
        }
        str += outstr.str();
    }
    return isFeasible;
}


/////////////////////////////////////////////////////////////////////////
// fills the constraints vectors (and output vectors)
void
MAiNGO::_classify_objective_and_constraints(std::vector<mc::FFVar>& tmpFunctions, const std::vector<mc::FFVar>& tmpDAGVars)
{

    // Assign the array of functions
    _constantConstraintsFeasible = true;
    _originalConstraints         = std::make_shared<std::vector<Constraint>>();
    _constantConstraints         = std::make_shared<std::vector<Constraint>>();
    _nonconstantConstraints      = std::make_shared<std::vector<Constraint>>();
    _constantOutputs             = std::make_shared<std::vector<Constraint>>();
    _nonconstantOutputs          = std::make_shared<std::vector<Constraint>>();
    unsigned indexNonconstant = 0, indexOriginal = 0, indexConstant = 0, indexType = 0, indexTypeNonconstant = 0, indexTypeConstant = 0;
    _nobj                 = 0;
    _nineq                = 0;
    _neq                  = 0;
    _nineqRelaxationOnly  = 0;
    _neqRelaxationOnly    = 0;
    _nineqSquash          = 0;
    _nconstantIneq        = 0;
    _nconstantEq          = 0;
    _nconstantIneqRelOnly = 0;
    _nconstantEqRelOnly   = 0;
    _nconstantIneqSquash  = 0;
    _ndata                = 0;
    // Objective(s)
    _ensure_valid_objective_function_using_dummy_variable(tmpDAGVars[0]);
    for (size_t i = 0; i < _modelOutput.objective.size(); i++) {
        tmpFunctions.push_back(_modelOutput.objective.value[i]);
        _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::OBJ, indexOriginal, indexType, indexNonconstant, indexTypeNonconstant, _modelOutput.objective.name[i]));
        _nonconstantConstraints->push_back(Constraint(CONSTRAINT_TYPE::OBJ, indexOriginal++, indexType++, indexNonconstant++, indexTypeNonconstant++, _modelOutput.objective.name[i]));
        _nobj++;
    }
    // Inequalities
    indexType            = 0;
    indexTypeNonconstant = 0;
    indexTypeConstant    = 0;
    for (unsigned int i = 0; i < _modelOutput.ineq.size(); i++) {
        if (!_modelOutput.ineq[i].dag()) {    // Check if DAG pointer is set, if not the constraint is a constant
            double val = _modelOutput.ineq[i].num().val();
            _nconstantIneq++;
            if (val > _maingoSettings->deltaIneq) {
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.ineq.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.ineq.name[i]));
                _constantConstraintsFeasible = false;
            }
            else {
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.ineq.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.ineq.name[i]));
            }
        }
        else {    // Function is non-constant
            _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ, indexOriginal, indexType, indexNonconstant,
                                                       indexTypeNonconstant, _modelOutput.ineq.name[i]));
            _nonconstantConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ, indexOriginal++, indexType++, indexNonconstant++,
                                                          indexTypeNonconstant++, _modelOutput.ineq.name[i]));
            tmpFunctions.push_back(_modelOutput.ineq[i]);
            _nineq++;
        }
    }
    // Equalities
    indexType            = 0;
    indexTypeNonconstant = 0;
    indexTypeConstant    = 0;
    for (unsigned int i = 0; i < _modelOutput.eq.size(); i++) {
        if (!_modelOutput.eq[i].dag()) {    // Check if DAG pointer is set, if not the constraint is a constant
            double val = _modelOutput.eq[i].num().val();
            _nconstantEq++;
            if (std::fabs(val) > _maingoSettings->deltaEq) {
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.eq.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.eq.name[i]));
                _constantConstraintsFeasible = false;
            }
            else {
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.eq.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.eq.name[i]));
            }
        }
        else {
            _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ, indexOriginal, indexType, indexNonconstant,
                                                       indexTypeNonconstant, _modelOutput.eq.name[i]));
            _nonconstantConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ, indexOriginal++, indexType++, indexNonconstant++,
                                                          indexTypeNonconstant++, _modelOutput.eq.name[i]));
            tmpFunctions.push_back(_modelOutput.eq[i]);
            _neq++;
        }
    }
    // Relaxation-only inequalities
    indexType            = 0;
    indexTypeNonconstant = 0;
    indexTypeConstant    = 0;
    for (unsigned int i = 0; i < _modelOutput.ineqRelaxationOnly.size(); i++) {
        if (!_modelOutput.ineqRelaxationOnly[i].dag()) {    // Check if DAG pointer is set, if not the constraint is a constant
            double val = _modelOutput.ineqRelaxationOnly[i].num().val();
            _nconstantIneqRelOnly++;
            if (val > _maingoSettings->deltaIneq) {
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_REL_ONLY, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.ineqRelaxationOnly.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_REL_ONLY, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.ineqRelaxationOnly.name[i]));
                _constantConstraintsFeasible = false;
            }
            else {
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_REL_ONLY, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.ineqRelaxationOnly.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_REL_ONLY, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.ineqRelaxationOnly.name[i]));
            }
        }
        else {
            _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_REL_ONLY, indexOriginal, indexType,
                                                       indexNonconstant, indexTypeNonconstant, _modelOutput.ineqRelaxationOnly.name[i]));
            _nonconstantConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_REL_ONLY, indexOriginal++, indexType++,
                                                          indexNonconstant++, indexTypeNonconstant++, _modelOutput.ineqRelaxationOnly.name[i]));
            tmpFunctions.push_back(_modelOutput.ineqRelaxationOnly[i]);
            _nineqRelaxationOnly++;
        }
    }
    // Relaxation-only equalities
    indexType            = 0;
    indexTypeNonconstant = 0;
    indexTypeConstant    = 0;
    for (unsigned int i = 0; i < _modelOutput.eqRelaxationOnly.size(); i++) {
        if (!_modelOutput.eqRelaxationOnly[i].dag()) {    // Check if DAG pointer is set, if not the constraint is a constant
            double val = _modelOutput.eqRelaxationOnly[i].num().val();
            _nconstantEqRelOnly++;
            if (std::fabs(val) > _maingoSettings->deltaEq) {
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ_REL_ONLY, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.eqRelaxationOnly.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ_REL_ONLY, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.eqRelaxationOnly.name[i]));
                _constantConstraintsFeasible = false;
            }
            else {
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ_REL_ONLY, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.eqRelaxationOnly.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ_REL_ONLY, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.eqRelaxationOnly.name[i]));
            }
        }
        else {
            _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ_REL_ONLY, indexOriginal, indexType,
                                                       indexNonconstant, indexTypeNonconstant, _modelOutput.eqRelaxationOnly.name[i]));
            _nonconstantConstraints->push_back(Constraint(CONSTRAINT_TYPE::EQ_REL_ONLY, indexOriginal++, indexType++,
                                                          indexNonconstant++, indexTypeNonconstant++, _modelOutput.eqRelaxationOnly.name[i]));
            tmpFunctions.push_back(_modelOutput.eqRelaxationOnly[i]);
            _neqRelaxationOnly++;
        }
    }
    // Squash inequalities
    indexType            = 0;
    indexTypeNonconstant = 0;
    indexTypeConstant    = 0;
    for (unsigned int i = 0; i < _modelOutput.ineqSquash.size(); i++) {
        if (!_modelOutput.ineqSquash[i].dag()) {    // Check if DAG pointer is set, if not the constraint is a constant
            double val = _modelOutput.ineqSquash[i].num().val();
            _nconstantIneqSquash++;
            if (val > 0) {    // No tolerances are allowed for squash inequalities!
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_SQUASH, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.ineqSquash.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_SQUASH, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ false, val, _modelOutput.ineqSquash.name[i]));
                _constantConstraintsFeasible = false;
            }
            else {
                _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_SQUASH, indexOriginal, indexType, indexConstant, indexTypeConstant,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.ineqSquash.name[i]));
                _constantConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_SQUASH, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                           /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.ineqSquash.name[i]));
            }
        }
        else {
            _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_SQUASH, indexOriginal, indexType,
                                                       indexNonconstant, indexTypeNonconstant, _modelOutput.ineqSquash.name[i]));
            _nonconstantConstraints->push_back(Constraint(CONSTRAINT_TYPE::INEQ_SQUASH, indexOriginal++, indexType++,
                                                          indexNonconstant++, indexTypeNonconstant++, _modelOutput.ineqSquash.name[i]));
            tmpFunctions.push_back(_modelOutput.ineqSquash[i]);
            _nineqSquash++;
        }
    }
#ifdef HAVE_GROWING_DATASETS
    // Objective per data
    _ndata               = _modelOutput.objective_per_data.size();
    indexType            = 0;
    indexTypeNonconstant = 0;
    _ensure_valid_objective_per_data_function_using_dummy_variable(tmpDAGVars[0]);
    for (size_t i = 0; i < _modelOutput.objective_per_data.size(); i++) {
        tmpFunctions.push_back(_modelOutput.objective_per_data[i]);
    }
#endif

    // Output variables
    indexType                 = 0;
    indexOriginal             = 0;
    indexConstant             = 0;
    indexNonconstant          = 0;
    indexTypeNonconstant      = 0;
    indexTypeConstant         = 0;
    _noutputVariables         = 0;
    _nconstantOutputVariables = 0;
    for (unsigned int i = 0; i < _modelOutput.output.size(); i++) {
        if (!_modelOutput.output[i].value.dag()) {    // Check if DAG pointer is set, if not the output is a constant
            double val = _modelOutput.output[i].value.num().val();
            _constantOutputs->push_back(Constraint(CONSTRAINT_TYPE::OUTPUT, indexOriginal++, indexType++, indexConstant++, indexTypeConstant++,
                                                   /*isConstant*/ true, /*isFeasible*/ true, val, _modelOutput.output[i].description));
            _nconstantOutputVariables++;
        }
        else {
            _nonconstantOutputs->push_back(Constraint(CONSTRAINT_TYPE::OUTPUT, indexOriginal++, indexType++, indexNonconstant++,
                                                      indexTypeNonconstant++, _modelOutput.output[i].description));
            tmpFunctions.push_back(_modelOutput.output[i].value);
            _noutputVariables++;
        }
    }
}


/////////////////////////////////////////////////////////////////////////
// Ensures that the objective function stored in the _modelOutput is valid
void
MAiNGO::_ensure_valid_objective_function_using_dummy_variable(const mc::FFVar& dummyVariable)
{
    if (_modelOutput.objective.size() == 0) {
        // If no objective has been specified, simply add some dummy
        _modelOutput.objective.push_back(dummyVariable + 1.0 + 0 - dummyVariable - 1.0);
        _feasibilityProblem                       = true;
        _maingoSettings->terminateOnFeasiblePoint = true;
        _logger->print_message("\n  Warning: No objective function has been specified. Assuming this is a feasibility problem.\n           During solution, a constant dummy objective with value 0 will be used.",
                               VERB_NORMAL, BAB_VERBOSITY);
    }
    else {
        for (size_t i = 0; i < _modelOutput.objective.size(); i++) {
            if (!_modelOutput.objective[i].dag()) {    // Check if DAG pointer is set, if not the objective is a constant
                // This is basically saying objective = x1 + 1 + constant - x1 - 1 = constant.
                // We are doing this since 0*x1 or x1 - x1 will be recognized by the DAG (this may change in future).
                // Adding and substracting the 1.0 avoids errors in the case of non-defined objective.
                // An alternative would be to define a flag telling whether the objective is constant and propagate it to the LBD and UBD solvers.
                _logger->print_message("\n  Warning: Objective function is a constant with value " + std::to_string(_modelOutput.objective[i].num().val()) + ".",
                                       VERB_NORMAL, BAB_VERBOSITY);
                _modelOutput.objective.set_value(dummyVariable + 1.0 + _modelOutput.objective[i].num().val() - dummyVariable - 1.0, i);
            }
        }
    }
}


#ifdef HAVE_GROWING_DATASETS
/////////////////////////////////////////////////////////////////////////
// Ensures that constant objective_per_data is not removed
void
MAiNGO::_ensure_valid_objective_per_data_function_using_dummy_variable(const mc::FFVar& dummyVariable)
{
    for (size_t i = 0; i < _modelOutput.objective_per_data.size(); i++) {
        if (!_modelOutput.objective_per_data[i].dag()) {    // Check if DAG pointer is set, if not the objective is a constant
            // This is basically saying objective = x1 + 1 + constant - x1 - 1 = constant.
            // We are doing this since 0*x1 or x1 - x1 will be recognized by the DAG (this may change in future).
            // Adding and substracting the 1.0 avoids errors in the case of non-defined objective.
            // An alternative would be to define a flag telling whether the objective is constant and propagate it to the LBD and UBD solvers.
            _logger->print_message("\n  Warning: Objective_per_data [" + std::to_string(i) + "] is a constant with value " + std::to_string(_modelOutput.objective[i].num().val()) + ".",
                                   VERB_NORMAL, BAB_VERBOSITY);
            _modelOutput.objective_per_data.set_value(dummyVariable + 1.0 + _modelOutput.objective_per_data[i].num().val() - dummyVariable - 1.0, i);
        }
    }
}
#endif


/////////////////////////////////////////////////////////////////////////
// checks whether some constraints (or output) is not indeed 0 and also fills the _DAGoutputFunctions vector
bool
MAiNGO::_check_for_hidden_zero_constraints(const std::vector<mc::FFVar>& tmpDAGVars, std::vector<mc::FFVar>& tmpDAGFunctions, std::vector<mc::FFVar>& tmpDAGoutputFunctions)
{

    bool foundHiddenZero = false;
    // We will check again if the resulting functions are constant, since it is possible to construct a "hidden" 0 function which is recognized first after tmpDAG.eval(...)
    bool updateIndices = false;
    for (int i = _resultVars.size() - _noutputVariables - 1; i >= 0; i--) {
        if (!_resultVars[i].dag()) {
            foundHiddenZero = true;
            switch ((*_nonconstantConstraints)[i].type) {
                case OBJ:
                    _resultVars[i] = tmpDAGVars[0] + 1.0 + _modelOutput.objective[i].num().val() - tmpDAGVars[0] - 1.0;
                    tmpDAGFunctions.push_back(_resultVars[i]);    // Get functions
                    continue;
                case INEQ:
                    _nineq--;
                    _nconstantIneq++;
                    break;
                case EQ:
                    _neq--;
                    _nconstantEq++;
                    break;
                case INEQ_REL_ONLY:
                    _nineqRelaxationOnly--;
                    _nconstantIneqRelOnly++;
                    break;
                case EQ_REL_ONLY:
                    _neqRelaxationOnly--;
                    _nconstantEqRelOnly++;
                    break;
                case INEQ_SQUASH:
                    _nineqSquash--;
                    _nineqSquash++;
                    break;
                default:
                    break;

            }    // End of switch
            // Erase the constraint from nonconstant constraints and insert it into the constant constraints vector
            updateIndices  = true;
            Constraint tmp = (*_nonconstantConstraints)[i];
            _nonconstantConstraints->erase(_nonconstantConstraints->begin() + i);
            tmp.isFeasible                             = true;
            tmp.isConstant                             = true;
            tmp.constantValue                          = 0;
            tmp.indexNonconstant                       = 0;
            tmp.indexTypeNonconstant                   = 0;
            (*_originalConstraints)[tmp.indexOriginal] = tmp;
            // Insert the constraint to the constantConstraints vector at the right place
            if (_constantConstraints->empty()) {
                _constantConstraints->push_back(tmp);
            }
            else {
                for (size_t i = 0; i < _constantConstraints->size(); i++) {
                    if ((*_constantConstraints)[i].indexOriginal < tmp.indexOriginal) {
                        if (i == _constantConstraints->size() - 1) {
                            _constantConstraints->insert(_constantConstraints->end(), tmp);
                            break;
                        }
                        continue;
                    }
                    else {
                        _constantConstraints->insert(_constantConstraints->begin() + i, tmp);
                        break;
                    }
                }
            }
        }
        else {
            tmpDAGFunctions.push_back(_resultVars[i]);    // Get functions
        }
    }                                                                // End of for loop over _resultVars - _noutputVariables
    std::reverse(tmpDAGFunctions.begin(), tmpDAGFunctions.end());    // Reverse the ordering to be equal to initial user input
    // Update nonconstant and constant index of constraints
    if (updateIndices) {
        unsigned indexObj = 0, indexIneq = 0, indexEq = 0, indexIneqRelOnly = 0, indexEqRelOnly = 0, indexIneqSquash = 0;
        for (size_t i = 0; i < _nonconstantConstraints->size(); i++) {
            (*_nonconstantConstraints)[i].indexNonconstant                                        = i;
            (*_originalConstraints)[(*_nonconstantConstraints)[i].indexOriginal].indexNonconstant = i;
            switch ((*_nonconstantConstraints)[i].type) {
                case OBJ:
                    (*_nonconstantConstraints)[i].indexTypeNonconstant                                        = indexObj;
                    (*_originalConstraints)[(*_nonconstantConstraints)[i].indexOriginal].indexTypeNonconstant = indexObj++;
                    break;
                case INEQ:
                    (*_nonconstantConstraints)[i].indexTypeNonconstant                                        = indexIneq;
                    (*_originalConstraints)[(*_nonconstantConstraints)[i].indexOriginal].indexTypeNonconstant = indexIneq++;
                    break;
                case EQ:
                    (*_nonconstantConstraints)[i].indexTypeNonconstant                                        = indexEq;
                    (*_originalConstraints)[(*_nonconstantConstraints)[i].indexOriginal].indexTypeNonconstant = indexEq++;
                    break;
                case INEQ_REL_ONLY:
                    (*_nonconstantConstraints)[i].indexTypeNonconstant                                        = indexIneqRelOnly;
                    (*_originalConstraints)[(*_nonconstantConstraints)[i].indexOriginal].indexTypeNonconstant = indexIneqRelOnly++;
                    break;
                case EQ_REL_ONLY:
                    (*_nonconstantConstraints)[i].indexTypeNonconstant                                        = indexEqRelOnly;
                    (*_originalConstraints)[(*_nonconstantConstraints)[i].indexOriginal].indexTypeNonconstant = indexEqRelOnly++;
                    break;
                case INEQ_SQUASH:
                    (*_nonconstantConstraints)[i].indexTypeNonconstant                                        = indexIneqSquash;
                    (*_originalConstraints)[(*_nonconstantConstraints)[i].indexOriginal].indexTypeNonconstant = indexIneqSquash++;
                    break;
                default:
                    break;
            }
        }
        indexObj         = 0;
        indexIneq        = 0;
        indexEq          = 0;
        indexIneqRelOnly = 0;
        indexEqRelOnly   = 0;
        indexIneqSquash  = 0;
        for (size_t i = 0; i < _constantConstraints->size(); i++) {
            (*_constantConstraints)[i].indexConstant                                        = i;
            (*_originalConstraints)[(*_constantConstraints)[i].indexOriginal].indexConstant = i;
            switch ((*_constantConstraints)[i].type) {
                case OBJ:
                    (*_constantConstraints)[i].indexTypeConstant                                        = indexObj;
                    (*_originalConstraints)[(*_constantConstraints)[i].indexOriginal].indexTypeConstant = indexObj++;
                    break;
                case INEQ:
                    (*_constantConstraints)[i].indexTypeConstant                                        = indexIneq;
                    (*_originalConstraints)[(*_constantConstraints)[i].indexOriginal].indexTypeConstant = indexIneq++;
                    break;
                case EQ:
                    (*_constantConstraints)[i].indexTypeConstant                                        = indexEq;
                    (*_originalConstraints)[(*_constantConstraints)[i].indexOriginal].indexTypeConstant = indexEq++;
                    break;
                case INEQ_REL_ONLY:
                    (*_constantConstraints)[i].indexTypeConstant                                        = indexIneqRelOnly;
                    (*_originalConstraints)[(*_constantConstraints)[i].indexOriginal].indexTypeConstant = indexIneqRelOnly++;
                    break;
                case EQ_REL_ONLY:
                    (*_constantConstraints)[i].indexTypeConstant                                        = indexEqRelOnly;
                    (*_originalConstraints)[(*_constantConstraints)[i].indexOriginal].indexTypeConstant = indexEqRelOnly++;
                    break;
                case INEQ_SQUASH:
                    (*_constantConstraints)[i].indexTypeConstant                                        = indexIneqSquash;
                    (*_originalConstraints)[(*_constantConstraints)[i].indexOriginal].indexTypeConstant = indexIneqSquash++;
                    break;
                default:
                    break;
            }
        }
    }
    // Check if resulting output functions are constant
    updateIndices               = false;
    unsigned newConstantOutputs = 0;
    int maxIndex                = _resultVars.size() - (_noutputVariables);
    for (int i = _resultVars.size() - 1; i >= maxIndex; i--) {
        if (!_resultVars[i].dag()) {
            foundHiddenZero = true;
            _noutputVariables--;
            _nconstantOutputVariables++;
            newConstantOutputs++;
            updateIndices  = true;
            Constraint tmp = (*_nonconstantOutputs)[_noutputVariables + newConstantOutputs - _resultVars.size() + i];
            _nonconstantOutputs->erase(_nonconstantOutputs->begin() + (_noutputVariables - _resultVars.size() + i + newConstantOutputs));
            tmp.isFeasible       = true;
            tmp.isConstant       = true;
            tmp.constantValue    = 0;
            tmp.indexNonconstant = 0;
            // Insert the constraint to the constantOutputs vector at the right place
            if (_constantOutputs->empty()) {
                _constantOutputs->push_back(tmp);
            }
            else {
                for (size_t j = 0; j < _constantOutputs->size(); j++) {
                    if ((*_constantOutputs)[j].indexOriginal < tmp.indexOriginal) {
                        if (j == _constantOutputs->size() - 1) {
                            _constantOutputs->insert(_constantOutputs->end(), tmp);
                            break;
                        }
                        continue;
                    }
                    else {
                        _constantOutputs->insert(_constantOutputs->begin() + j, tmp);
                        break;
                    }
                }
            }
        }
        else {
            tmpDAGoutputFunctions.push_back(_resultVars[i]);    // Get pointers to functions
        }
    }
    std::reverse(tmpDAGoutputFunctions.begin(), tmpDAGoutputFunctions.end());    // Reverse the ordering to be equal to initial user input
                                                                                 // Update nonconstant and constant index of outputs
    if (updateIndices) {
        for (size_t i = 0; i < _nonconstantOutputs->size(); i++) {
            (*_nonconstantOutputs)[i].indexNonconstant = i;
        }
        for (size_t i = 0; i < _constantOutputs->size(); i++) {
            (*_constantOutputs)[i].indexConstant = i;
        }
    }
    return foundHiddenZero;
}


#ifdef HAVE_GROWING_DATASETS
/////////////////////////////////////////////////////////////////////////
// initializes objective via the user-defined objective_per_data when using MAiNGO with growing datasets
// currently: objective = sum of objective_per_data
void
MAiNGO::_initialize_objective_from_objective_per_data()
{
    if (_modelOutput.objective_per_data.size() == 0) {
        throw MAiNGOException("  Error initializing MAiNGO: MAiNGO with growing datasets requires setting objective per data.");
    }
    else {    // Objective per data is defined: print warning (in manager process)
        MAiNGO_IF_BAB_MANAGER
            if (_modelOutput.objective.size() > 0) {
                _logger->print_message("\n  Warning: Objective is overwritten based on objective_per_data. \n", VERB_NORMAL, BAB_VERBOSITY);
            }
        MAiNGO_END_IF    // End of MAiNGO_IF_BAB_MANAGER
        _modelOutput.objective.clear();

        //objective considering complete dataset for setting up complete DAG
        mc::FFVar obj = 0;
        for (auto i = 0; i < _modelOutput.objective_per_data.size(); i++) {
            obj += _modelOutput.objective_per_data[i];
        }
        _modelOutput.objective = obj;
    }
}


////////////////////////////////////////////////////////////////////////
// initializes full dataset (= largest set, index 0) and initial reduced dataset (= smallest set, index 1)
void
MAiNGO::_initialize_dataset()
{
    _datasets = std::make_shared<std::vector<std::set<unsigned int>>>();

    // Full dataset is range 0,...,_ndata-1
    std::set<unsigned int> tmpFullSet;
    for (unsigned int i = 0; i < _ndata; i++) {
        tmpFullSet.insert(tmpFullSet.end(), i);
    }
    _datasets->push_back(tmpFullSet);

    // Smallest reduced dataset
    // Random set with size given by settings
    if (_ndata > 1) {    // Only if smaller than full dataset
        std::set<unsigned int> tmpReducedSet;
        int noAddedData = std::round((double)_maingoSettings->growing_dataSizeInit * (double)_ndata);
        noAddedData     = std::max(1, noAddedData);

        std::srand(5);    // For reproducible results
        std::pair<std::set<unsigned int>::iterator, bool> ans;
        int count = 0;

        while (count < noAddedData) {
            double tmpRand = std::rand() / ((double)RAND_MAX + 1);    // Random value between 0. and 1.

            // Choose from unused data points (set difference)
            size_t idxRand = tmpRand * _ndata;
            ans            = tmpReducedSet.insert(*(std::next(tmpFullSet.begin(), idxRand)));
            if (ans.second == true) {
                count++;
            }
        }
        _datasets->push_back(tmpReducedSet);
    }
}
#endif    //HAVE_GROWING_DATASETS

/////////////////////////////////////////////////////////////////////////
// modifies the lower bound DAG _DAGlbd by adding auxiliary optimization variables for intermediate factors occuring multiple times
void
MAiNGO::_add_auxiliary_variables_to_lbd_dag()
{

    // First, we evaluate the model at mid point
    // This is done to get interval bounds for auxiliary factors and compute a score
    std::vector<MC> independentVariablesMC(_DAGvarsLbd.size());    // Vector holding the bounds of optimization variables as intervals
    std::vector<double> lowerVarBounds(_nvar);
    std::vector<double> upperVarBounds(_nvar);
    std::vector<double> referencePoint(_nvar);    // This is the point at which we evaluate the relaxations to assess how far away they are from the functions
    for (unsigned int i = 0; i < _nvar; i++) {
        lowerVarBounds[i]         = _variables[i].get_lower_bound();
        upperVarBounds[i]         = _variables[i].get_upper_bound();
        referencePoint[i]         = 0.5 * (lowerVarBounds[i] + upperVarBounds[i]);
        independentVariablesMC[i] = MC(I(lowerVarBounds[i], upperVarBounds[i]), referencePoint[i]);
        independentVariablesMC[i].sub(_nvar, i);    // Set subgradient dimension
    }

    // Set options for the McCormick relaxations and the subgradient heuristic (these may be reset later in the lower bounding solver)
    if (_maingoSettings->LBP_subgradientIntervals) {
        MC::options.SUB_INT_HEUR_USE = true;
    }
    else {
        MC::options.SUB_INT_HEUR_USE = false;
    }
    MC::subHeur.clear();
    MC::options.ENVEL_USE           = true;
    MC::options.ENVEL_MAXIT         = 100;
    MC::options.ENVEL_TOL           = _maingoSettings->MC_envelTol;
    MC::options.MVCOMP_USE          = _maingoSettings->MC_mvcompUse;
    MC::options.MVCOMP_TOL          = _maingoSettings->MC_mvcompTol;
    MC::subHeur.originalLowerBounds = &lowerVarBounds;
    MC::subHeur.originalUpperBounds = &upperVarBounds;
    MC::subHeur.referencePoint      = &referencePoint;

    // Get the subgraph of those things that actually occur in objective and constraints
    mc::FFSubgraph MCSubgraph = _DAGlbd.subgraph(_DAGfunctionsLbd.size(), _DAGfunctionsLbd.data());

    // Evaluate in McCormick arithmetic
    std::vector<MC> objectiveAndConstraintsMC(_DAGfunctionsLbd.size());    // Dummy vector holding the McCormick objects of all functions in the model
    std::vector<MC> operationResultsMC;                                    // Vector holding the range intervals for each operation in the DAG
    _DAGlbd.eval(MCSubgraph, operationResultsMC, _DAGfunctionsLbd.size(), _DAGfunctionsLbd.data(), objectiveAndConstraintsMC.data(), _DAGvarsLbd.size(), _DAGvarsLbd.data(), independentVariablesMC.data());

    // Evaluate in double arithmetic
    std::vector<double> operationResultsDouble;
    std::vector<double> objectiveAndConstraintsDouble(_DAGfunctionsLbd.size());
    _DAGlbd.eval(MCSubgraph, operationResultsDouble, _DAGfunctionsLbd.size(), _DAGfunctionsLbd.data(), objectiveAndConstraintsDouble.data(), _DAGvarsLbd.size(), _DAGvarsLbd.data(), referencePoint.data());


    // Based on the results, determine which dependent variables are candidates for being converted to auxiliary variables
    // To qualify, a variables has to
    //  - be dependent and non-constant
    //  - occur in at least LBP_minFactorsForAux other operations
    //  - depend nonlinearly on some variables
    //  - depend on at least 2 independent variables
    //  - contribute to the computation of the objective or at least one constraint residual
    // If a variable qualifies, it is added to the list of candidates.
    // The selection from this list is based on the factorRanking which considers (in order of importance)
    //   1. the number of operations the variable
    //   2. the sum of absolute differences between the function and the convex and concave relaxation at the reference point
    mc::FFGraph::t_Vars ffVars = _DAGlbd.Vars();    // Set of all FFVars in the DAG
    mc::FFGraph::it_Vars itv   = ffVars.begin();
    std::multimap<std::pair<unsigned, double>, std::pair<mc::FFVar*, mc::FFDep::TYPE>> factorRanking;
    for (; itv != ffVars.end(); ++itv) {

        // We are interested in non-constant dependent FFVars only
        if ((*itv)->id().first != mc::FFVar::VAR && (*itv)->id().first != mc::FFVar::CINT && (*itv)->id().first != mc::FFVar::CREAL) {
            const typename mc::FFVar::t_Ops operationsUsedIn = (*itv)->ops().second;    // This is a list of all operations where this FFVar is used
            const mc::FFOp* pOperation                       = (*itv)->ops().first;     // This is the operation of this FFVar

            if (operationsUsedIn.size() >= _maingoSettings->LBP_minFactorsForAux) {

                // Determine how the dependent variable depends on the independent ones
                const std::map<int, int> dependenceOnIndependentVars = (*itv)->dep().dep();
                mc::FFDep::TYPE functionStructure                    = mc::FFDep::L;
                std::vector<size_t> participatingVars;
                for (size_t j = 0; j < _nvar; j++) {
                    auto ito2 = dependenceOnIndependentVars.find(j);
                    // Count all participating variables
                    if (ito2 != dependenceOnIndependentVars.end()) {
                        participatingVars.push_back(j);
                        mc::FFDep::TYPE variableDep = (mc::FFDep::TYPE)(ito2->second);
                        // Update function type
                        if (functionStructure < variableDep) {
                            functionStructure = variableDep;
                        }
                    }
                }
                // Only add this auxiliary if it is at least bilinear and has at least 2 original variables
                if (functionStructure > mc::FFDep::L && participatingVars.size() >= 2) {
                    // Find the correct McCormick object for the replaced FFVar by searching the corresponding operation in MCSubgraph
                    size_t index                             = 0;
                    std::list<const mc::FFOp*>::iterator itL = MCSubgraph.l_op.begin();
                    for (; itL != MCSubgraph.l_op.end(); ++itL) {
                        if ((*itL) != pOperation) {
                            index++;
                        }
                        else {
                            break;
                        }
                    }
                    // Only add variable if it was found in MCSubgraph.l_op. Otherwise, it is not actually used in any function (i.e., objective or constraints)
                    if (itL != MCSubgraph.l_op.end()) {
                        const double averageRelaxationOffset = std::fabs(operationResultsMC[index].cv() - operationResultsDouble[index]) + std::fabs(operationResultsMC[index].cc() - operationResultsDouble[index]);
                        factorRanking.insert(std::make_pair(std::make_pair(operationsUsedIn.size(), averageRelaxationOffset), std::make_pair((*itv), functionStructure)));
                    }
                }
            }
        }
    }

    // Go through factor ranking to select the most promising candidates
    std::vector<MC> auxVariablesMCBounds;                                                                                                        // Vector holding McCormick objects to derive the bounds for auxiliary variables which will be added
    unsigned indexOriginal                                                                                   = _DAGfunctions.size() - _ndata;    // objective_per_data are not considered as constraints (without growing datasets: _ndata == 0 by initialization and never changed)
    unsigned indexType                                                                                       = 0;
    unsigned indexTypeNonconstant                                                                            = _neqRelaxationOnly;    // Auxiliary relaxation only constraints are handled as normal eq rel only constraints
    unsigned indexNonconstant                                                                                = 1 + _nineq + _neq + _nineqRelaxationOnly + _neqRelaxationOnly + _nineqSquash;
    unsigned counter                                                                                         = 0;
    std::multimap<std::pair<unsigned, double>, std::pair<mc::FFVar*, mc::FFDep::TYPE>>::reverse_iterator rit = factorRanking.rbegin();
#ifdef HAVE_GROWING_DATASETS
    // Keep obj_per_data behind auxiliary variables
    // Save function pointers into temporary vector
    unsigned int tmpSize = _DAGfunctionsLbd.size();
    std::vector<mc::FFVar> dataFunctions;
    dataFunctions.resize(_ndata);
    for (auto idx = 0; idx < _ndata; idx++) {
        dataFunctions[idx] = _DAGfunctionsLbd[tmpSize - _ndata + idx];
    }
    _DAGfunctionsLbd.resize(tmpSize - _ndata);
#endif    // HAVE_GROWING_DATASETS
    for (; rit != factorRanking.rend() && counter < _maingoSettings->LBP_maxNumberOfAddedFactors; ++rit) {

        mc::FFVar* itv                             = (*rit).second.first;
        mc::FFDep::TYPE functionStructure          = (*rit).second.second;
        typename mc::FFVar::t_Ops operationsUsedIn = itv->ops().second;    // This is a list of all operations where this FFVar is used
        mc::FFOp* pOperation                       = itv->ops().first;     // This is the operation of this FFVar

        // Get new independent variable and add it to list of DAG variables
        mc::FFVar newIndependentVar = _DAGlbd.replace_intermediate_variable_by_independent_copy(itv);
        _DAGvarsLbd.push_back(newIndependentVar);

        // Add the corresponding equality constraint: aux-f(x)=0
        mc::FFVar newConstraintResidual = newIndependentVar - (*itv);
        _DAGfunctionsLbd.push_back(newConstraintResidual);
        _originalConstraints->push_back(Constraint(CONSTRAINT_TYPE::AUX_EQ_REL_ONLY, indexOriginal, indexType,
                                                   indexNonconstant, indexTypeNonconstant));
        _nonconstantConstraints->push_back(Constraint(CONSTRAINT_TYPE::AUX_EQ_REL_ONLY, indexOriginal++, indexType++,
                                                      indexNonconstant++, indexTypeNonconstant++));
        _nauxiliaryRelOnlyEqs++;
        counter++;

        // Find the correct range interval of the replaced FFVar
        size_t index                             = 0;
        std::list<const mc::FFOp*>::iterator itL = MCSubgraph.l_op.begin();
        for (; itL != MCSubgraph.l_op.end(); ++itL) {
            if ((*itL) != pOperation) {
                index++;
            }
            else {
                break;
            }
        }
        auxVariablesMCBounds.push_back(operationResultsMC[index]);
    }
#ifdef HAVE_GROWING_DATASETS
    // Append obj_per_data once again
    for (auto dataPointer : dataFunctions) {
        _DAGfunctionsLbd.push_back(dataPointer);
    }
#endif    // HAVE_GROWING_DATASETS

    // Get valid variable bounds
    _variablesLbd.clear();
    for (size_t i = 0; i < _variables.size(); i++) {
        _variablesLbd.push_back(_variables[i]);
    }

    for (size_t i = 0; i < auxVariablesMCBounds.size(); i++) {
        std::string varName = "auxVar" + std::to_string(i);
        _variablesLbd.push_back(babBase::OptimizationVariable(Bounds(auxVariablesMCBounds[i].l(), auxVariablesMCBounds[i].u()), VT_CONTINUOUS, 0, varName));
    }
    _nvarLbd = _variablesLbd.size();

    // std::ofstream o_F("DAG.txt", std::ios_base::out);
    // o_F << _DAGlbd << std::endl;
    // o_F.close();
}


/////////////////////////////////////////////////////////////////////////
// sets function properties, number of variables and type (linear, bilinear...)
void
MAiNGO::_set_constraint_properties()
{

    // Get dependency sets of all functions
    std::vector<std::map<int, int>> func_dep;
    unsigned size = 1 + _nineq + _neq + _nineqRelaxationOnly + _neqRelaxationOnly + _nineqSquash + _nauxiliaryRelOnlyEqs;
    func_dep.resize(size);
    for (unsigned int i = 0; i < size; i++) {
        if (_maingoSettings->LBP_addAuxiliaryVars) {
            func_dep[i] = _DAGfunctionsLbd[i].dep().dep();
        }
        else {
            func_dep[i] = _DAGfunctions[i].dep().dep();
        }
    }

    // Loop over all functions
    unsigned indexLinear = 0, indexNonlinear = 0;
    for (unsigned int i = 0; i < size; i++) {
        mc::FFDep::TYPE functionStructure = mc::FFDep::L;
        std::vector<unsigned> participatingVars;
        for (unsigned int j = 0; j < _nvar; j++) {
            auto ito = func_dep[i].find(j);
            // Count all participating variables
            if (ito != func_dep[i].end()) {
                participatingVars.push_back(j);
                mc::FFDep::TYPE variableDep = (mc::FFDep::TYPE)(ito->second);
                // Update function type
                if (functionStructure < variableDep) {
                    functionStructure = variableDep;
                }
            }
        }
        (*_nonconstantConstraints)[i].nparticipatingVariables                                        = participatingVars.size();
        (*_originalConstraints)[(*_nonconstantConstraints)[i].indexOriginal].nparticipatingVariables = participatingVars.size();
        (*_nonconstantConstraints)[i].participatingVariables                                         = participatingVars;
        (*_originalConstraints)[(*_nonconstantConstraints)[i].indexOriginal].participatingVariables  = participatingVars;
        unsigned indexOriginal                                                                       = (*_nonconstantConstraints)[i].indexOriginal;
        switch (functionStructure) {
            case mc::FFDep::L:
                (*_nonconstantConstraints)[i].dependency           = LINEAR;
                (*_originalConstraints)[indexOriginal].dependency  = LINEAR;
                (*_nonconstantConstraints)[i].indexLinear          = indexLinear;
                (*_originalConstraints)[indexOriginal].indexLinear = indexLinear++;
                break;
            case mc::FFDep::B:
                (*_nonconstantConstraints)[i].dependency              = BILINEAR;
                (*_originalConstraints)[indexOriginal].dependency     = BILINEAR;
                (*_nonconstantConstraints)[i].indexNonlinear          = indexNonlinear;
                (*_originalConstraints)[indexOriginal].indexNonlinear = indexNonlinear++;
                break;
            case mc::FFDep::Q:
                (*_nonconstantConstraints)[i].dependency              = QUADRATIC;
                (*_originalConstraints)[indexOriginal].dependency     = QUADRATIC;
                (*_nonconstantConstraints)[i].indexNonlinear          = indexNonlinear;
                (*_originalConstraints)[indexOriginal].indexNonlinear = indexNonlinear++;
                break;
            case mc::FFDep::P:
                (*_nonconstantConstraints)[i].dependency              = POLYNOMIAL;
                (*_originalConstraints)[indexOriginal].dependency     = POLYNOMIAL;
                (*_nonconstantConstraints)[i].indexNonlinear          = indexNonlinear;
                (*_originalConstraints)[indexOriginal].indexNonlinear = indexNonlinear++;
                break;
            case mc::FFDep::R:
                (*_nonconstantConstraints)[i].dependency              = RATIONAL;
                (*_originalConstraints)[indexOriginal].dependency     = RATIONAL;
                (*_nonconstantConstraints)[i].indexNonlinear          = indexNonlinear;
                (*_originalConstraints)[indexOriginal].indexNonlinear = indexNonlinear++;
                break;
            case mc::FFDep::N:
            case mc::FFDep::D:
            default:
                (*_nonconstantConstraints)[i].dependency              = NONLINEAR;
                (*_originalConstraints)[indexOriginal].dependency     = NONLINEAR;
                (*_nonconstantConstraints)[i].indexNonlinear          = indexNonlinear;
                (*_originalConstraints)[indexOriginal].indexNonlinear = indexNonlinear++;
                break;
        }
        (*_nonconstantConstraints)[i].convexity             = CONV_NONE;
        (*_originalConstraints)[indexOriginal].convexity    = CONV_NONE;
        (*_nonconstantConstraints)[i].monotonicity          = MON_NONE;
        (*_originalConstraints)[indexOriginal].monotonicity = MON_NONE;
    }

    // Fill the vector with nonconstant constraints for the UBS properly
    unsigned indexUBP          = 0;
    unsigned offset            = _neq + _nineqRelaxationOnly + _neqRelaxationOnly;    // Auxiliary relaxation only equalities are added at the end
    _nonconstantConstraintsUBP = std::make_shared<std::vector<Constraint>>();
    _nonconstantConstraintsUBP->resize(1 + _nineq + _nineqSquash + _neq);
    for (unsigned int i = 0; i < size; i++) {
        unsigned indexOriginal = (*_nonconstantConstraints)[i].indexOriginal;
        switch ((*_nonconstantConstraints)[i].type) {
            case OBJ:
            case INEQ:    // Objective and inequalities keep their order
                (*_nonconstantConstraintsUBP)[i]                           = (*_nonconstantConstraints)[i];
                (*_nonconstantConstraintsUBP)[i].indexNonconstantUBP       = indexUBP;
                (*_nonconstantConstraints)[i].indexNonconstantUBP          = indexUBP;
                (*_originalConstraints)[indexOriginal].indexNonconstantUBP = indexUBP++;
                break;
            case EQ:
                (*_nonconstantConstraintsUBP)[i + _nineqSquash]                     = (*_nonconstantConstraints)[i];
                (*_nonconstantConstraintsUBP)[i + _nineqSquash].indexNonconstantUBP = indexUBP + _nineqSquash;
                (*_nonconstantConstraints)[i].indexNonconstantUBP                   = indexUBP + _nineqSquash;
                (*_originalConstraints)[indexOriginal].indexNonconstantUBP          = indexUBP + _nineqSquash;
                indexUBP++;
                break;
            case INEQ_SQUASH:
                (*_nonconstantConstraintsUBP)[i - offset]                     = (*_nonconstantConstraints)[i];
                (*_nonconstantConstraintsUBP)[i - offset].indexNonconstantUBP = indexUBP - _neq;
                (*_nonconstantConstraints)[i].indexNonconstantUBP             = indexUBP - _neq;
                (*_originalConstraints)[indexOriginal].indexNonconstantUBP    = indexUBP - _neq;
                indexUBP++;
                break;
            case INEQ_REL_ONLY:
            case EQ_REL_ONLY:
            case AUX_EQ_REL_ONLY:
            default:
                break;    // We don't use relaxation only constraints in the ubp
        }
    }
}
