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

#include "MAiNGOdebug.h"
#include "logger.h"
#include "mpiUtilities.h"
#ifdef HAVE_MAiNGO_MPI
#include "MAiNGOMpiException.h"
#endif

#include "babBrancher.h"

#include <cmath>
#include <map>
#include <memory>
#include <string>
#include <vector>


namespace maingo {


namespace lbp {
class LowerBoundingSolver;
struct LbpDualInfo;
}    // namespace lbp
namespace ubp {
class UpperBoundingSolver;
}    // namespace ubp


/**
*   @namespace maingo::bab
*   @brief namespace holding everything related to the actual branch-and-bound algorithm
*/
namespace bab {


/**
 * @class BranchAndBound
 * @brief This class contains the main algorithm, including handling of pre-processing routines and managing the B&B tree as well as the respective sub-solvers
 *
 * The class BranchAndBound implements a basic branch-and-bound (BaB) solver with some simple features for range reduction.
 * These include optimization-based range reduction (OBBT; cf., e.g., Gleixner et al., J. Glob. Optim. 67 (2017) 731), which can be conducted multiple times at the root node, and also once at every
 * node of the BAB tree, as well as duality-based bounds tightening (DBBT) and probing (cf. Ryoo&Sahinidis, Comput. Chem. Eng. 19 (1995) 551).
 * It also contains a multi-start local search from randomly generated initial points at the root node. Lower and upper bounding are conducted by the respective lower and upper bounding solvers (LBS / UBS).
*/
class BranchAndBound {

  public:
    /**
        * @brief Constructor, stores information on problem and settings
        *
        * @param[in] variables is a vector containing the initial optimization variables defined in problem.h
        * @param[in] LBSIn is a pointer to the LowerBoundingSolver object
        * @param[in] UBSIn is a pointer to the UpperBoundingSolver object
        * @param[in] settingsIn is a pointer to an object containing the settings for the Branch-and-Bound solvers
        * @param[in] loggerIn is a pointer to the MAiNGO logger object
        * @param[in] nvarWOaux is the number of optimization variables without the additional auxiliary variables added by the LBP_addAuxiliaryVars option
        */
    BranchAndBound(const std::vector<babBase::OptimizationVariable> &variables, std::shared_ptr<lbp::LowerBoundingSolver> LBSIn, std::shared_ptr<ubp::UpperBoundingSolver> UBSIn,
                   std::shared_ptr<Settings> settingsIn, std::shared_ptr<Logger> loggerIn, const unsigned nvarWOaux);

    /**
        * @brief Destructor
        */
    ~BranchAndBound() {}

    /**
        * @brief Main function to solve the optimization problem
        * @param[in] rootNodeIn Root node to start Branch&Bound on.
        * @param[in,out] solutionValue Objective value of best feasible point found (empty if no feasible point was found); Also used for communicating objective value of initial feasible point.
        * @param[in,out] solutionPoint Solution point, i.e., (one of) the point(s) at which the best objective value was found (empty if no feasible point was found); Also used for communicating initial feasible point.
        * @param[in] preprocessTime Is the CPU time spent in pre-processing before invoking this solve routine (needed for correct output of total CPU time during B&B)
        * @param[out] timePassed Is the CPU time spent in B&B (especially useful if time is >24h)
        * @return Return code summarizing the solution status.
        */
    babBase::enums::BAB_RETCODE solve(babBase::BabNode &rootNodeIn, double &solutionValue, std::vector<double> &solutionPoint, const double preprocessTime, double &timePassed);

    /**
        *  @brief Function returning the number of iterations
        */
    double get_iterations() { return _iterations; }

    /**
        *  @brief Function returning the maximum number of nodes in memory
        */
    double get_max_nodes_in_memory() { return _nNodesMaxInMemory; }

    /**
        *  @brief Function returning number of UBD problems solved
        */
    double get_UBP_count() { return _ubdcnt; }

    /**
        *  @brief Function returning number of LBD problems solved
        */
    double get_LBP_count() { return _lbdcnt; }

    /**
        *  @brief Function returning the final LBD
        */
    double get_final_LBD() { return _lbd; }

    /**
        *  @brief Function returning the final absolute gap
        */
    double get_final_abs_gap() { return _ubd - _lbd; }

    /**
        *  @brief Function returning the final relative gap
        */
    double get_final_rel_gap() { return ((_ubd == 0) ? (get_final_abs_gap()) : ((_ubd - _lbd) / std::fabs(_ubd))); }

    /**
        *  @brief Function returning the ID of the node where the incumbent was first found
        */
    double get_first_found() { return _firstFound; }

    /**
        *  @brief Function returning the number of nodes left after termination of B&B
        */
    double get_nodes_left() { return _nNodesLeft; }

#ifdef HAVE_GROWING_DATASETS
    /**
    * @brief Function for passing pointer of vector containing datasets to B&B
    *
    * @param[in] datasetsIn is a pointer to a vector containing all available datasets
    */
    void pass_datasets_to_bab(const std::shared_ptr<std::vector<std::set<unsigned int>>> datasetsIn)
    {
        _datasets = datasetsIn;
    }
#endif    // HAVE_GROWING_DATASETS
#if defined(MAiNGO_DEBUG_MODE) && defined(HAVE_GROWING_DATASETS)
    /**
	* @brief Function for passing pointer of LBS with full dataset to B&B
	*
	* @param[in] LBSFullIn is a pointer to an LBS object using the full dataset only
	*/
    void pass_LBSFull_to_bab(const std::shared_ptr<lbp::LowerBoundingSolver> LBSFullIn)
    {
        _LBSFull = LBSFullIn;
    }
#endif

  private:
    /**
        * @enum _TERMINATION_TYPE
        * @brief Enum for representing different termination types in B&B
        */
    enum _TERMINATION_TYPE {
        _TERMINATED = 0,            /*!< termination condition has been reached and no worker is processing any nodes */
        _TERMINATED_WORKERS_ACTIVE, /*!< termination condition has been reached, but there are still nodes being processed by workers */
        _NOT_TERMINATED             /*!< termination condition has not been reached yet*/
    };

    /**
        * @brief Function processing the current node
        *
        * @param[in,out] currentNodeInOut  The node to be processed
        */
    std::tuple<bool, bool, int, int, double, std::vector<double>, bool, double, std::vector<double>> _process_node(babBase::BabNode &currentNodeInOut);

    /**
        * @brief Function for pre-processing the current node. Includes bound tightening and OBBT.
        *
        * @param[in,out] currentNodeInOut  The node to be processed
        * @return Flag indicating whether the node was proven to be infeasible
        */
    bool _preprocess_node(babBase::BabNode &currentNodeInOut);

    /**
        * @brief Function invoking the LBS to solve the lower bounding problem
        *
        * @param[in] currentNode  The node to be processed
        * @return Tuple consisting of flags for whether the node is infeasible and whether it is converged, the lower bound, the lower bounding solution point, and dual information for DBBT
        */
    std::tuple<bool, bool, double, std::vector<double>, lbp::LbpDualInfo> _solve_LBP(const babBase::BabNode &currentNode);

    /**
        * @brief Function invoking the UBS to solve the upper bounding problem
        *
        * @param[in] currentNode  The node to be processed
        * @param[in,out] ubpSolutionPoint  On input: initial point for local search. On output: solution point.
        * @param[in] currentLBD Lower bound of current Node. Needed for sanity check.
        * @return Tuple consisting of flags indicating whether a new feasible point has been found and whether the node converged, and the optimal objective value of the new point
        */
    std::tuple<bool, bool, double> _solve_UBP(const babBase::BabNode &currentNode, std::vector<double> &ubpSolutionPoint, const double currentLBD);

    /**
        * @brief Function for post-processing the current node. Includes bound DBBT and probing
        *
        * @param[in,out] currentNodeInOut  The node to be processed
        * @param[in] lbpSolutionPoint  Solution point of the lower bounding problem
        * @param[in] dualInfo is a struct containing information from the LP solved during LBP
        * @return Flag indicating whether the node has converged
        */
    bool _postprocess_node(babBase::BabNode &currentNodeInOut, const std::vector<double> &lbpSolutionPoint, const lbp::LbpDualInfo &dualInfo);

    /**
        * @brief Function for updating the incumbent and fathoming accordingly
        *
        * @param[in] solval is the value of the processed solution
        * @param[in] sol is the solution point
        * @param[in] currentNodeID is the ID of the new node holding the incumbent (it is used instead of directly giving the node to match the parallel implementation)
        */
    void _update_incumbent_and_fathom(const double solval, const std::vector<double> sol, const unsigned int currentNodeID);

    /**
        * @brief Function for updating the global lower bound
        */
    void _update_lowest_lbd();

#ifdef HAVE_GROWING_DATASETS
    /**
    * @brief Function which checks whether to augment the dataset
    *
    * @param[in] currentNode is the node to be processed
    * @param[in] lbpSolutionPoint is the solution point of the LBP of the current node
    * @param[in] currentLBD is the objective value of the LBP of the current node
    */
    bool _check_whether_to_augment(const babBase::BabNode &currentNode, const std::vector<double> &lbpSolutionPoint, const double currentLBD);

    /**
    * @brief Function for augmenting dataset of node
    *
    * @param[in] current index of dataset
    * @param[out] new index of dataset after augmentation
    */
    unsigned int _augment_dataset(babBase::BabNode &currentNode);
#endif    // HAVE_GROWING_DATASETS

    /**
        * @brief Function which checks whether it is necessary to activate scaling within the LBD solver. This is a heuristic approach, which does not affect any deterministic optimization assumptions
        */
    void _check_if_more_scaling_needed();

    /**
        * @brief Function for checking if the B&B algorithm terminated
        */
    _TERMINATION_TYPE _check_termination();

    /**
        * @brief Function for printing the current progress on the screen and appending it to the internal log to be written to file later
        *
        * @param[in] currentNodeLBD is the lower bound for the current node
        * @param[in] currentNode is the current node
        */
    void _display_and_log_progress(const double currentNodeLBD, const babBase::BabNode &currentNode);

#if defined(MAiNGO_DEBUG_MODE) && defined(HAVE_GROWING_DATASETS)
    /**
		* @brief Function for printing the current node to a separate log file
		*
		* @param[in] currentNode is the current node
		* @param[in] currentNodeLbd is the lower bound calculated in the current node
		* @param[in] currentNodeLbdFull is the lower bound calculated based on the full dataset in the current node
		* @param[in] currentNodeUbdFull is the upper bound of the current node
		* @param[in] lbpSolutionPoint is the solution point of the lower bound calculated und used in the current node
		* @param[in] lbpSolutionPointFullis the solution point of the lower bound calculated based on the full dataset in the current node
		*/
    void _log_nodes(const babBase::BabNode &currentNode, const double currentNodeLbd, const double currentNodeLbdFull, const double currentNodeUbdFull, const std::vector<double> lbpSolutionPoint, const std::vector<double> lbpSolutionPointFull);
#endif

    /**
        * @brief Function printing a termination message
        *
        * @param[in] message is a string holding the message to print
        */
    void _print_termination(std::string message);

    /**
        * @brief Function printing one node
        *
        * @param[in] theLBD is the lower bound of the node
        * @param[in] ID is the id of the node
        * @param[in] lowerVarBounds are the variables lower bounds
        * @param[in] upperVarBounds are the variables upper bounds
        */
    void _print_one_node(const double theLBD, const int ID, const std::vector<double> lowerVarBounds, const std::vector<double> upperVarBounds);

    /**
        * @brief Function printing one node
        *
        * @param[in] theLBD is the lower bound of the node
        * @param[in] ID is the id of the node
        * @param[in] lowerVarBounds are the variables lower bounds
        * @param[in] upperVarBounds are the variables upper bounds
        * @param[in] outstream is the stream to be written to, e.g., an error message
        */
    void _print_one_node(const double theLBD, const int ID, const std::vector<double> lowerVarBounds, const std::vector<double> upperVarBounds, std::ostream &outstream);

    /**
        * @brief Function printing one node
        *
        * @param[in] theLBD is the lower bound of the node
        * @param[in] theNode is the node to be printed
        */
    void _print_one_node(const double theLBD, const babBase::BabNode &theNode)
    {
        _print_one_node(theLBD, theNode.get_ID(), theNode.get_lower_bounds(), theNode.get_upper_bounds());
    }

    /**
        * @brief Function printing one node
        *
        * @param[in] theLBD is the lower bound of the node
        * @param[in] theNode is the node to be printed
        * @param[in] outstream is the stream to be written to, e.g., an error message
        */
    void _print_one_node(const double theLBD, const babBase::BabNode &theNode, std::ostream &outstream)
    {
        _print_one_node(theLBD, theNode.get_ID(), theNode.get_lower_bounds(), theNode.get_upper_bounds(), outstream);
    }

#ifdef HAVE_MAiNGO_MPI
    /**
        * @name MPI management and communication functions of manager
        */
    /**@{*/
    /**
        * @brief Function for dealing with exceptions (informing workers etc.)
        *
        * @param[in] e is the exception to be handled
        */
    void _communicate_exception_and_throw(const maingo::MAiNGOMpiException &e);

    /**
        * @brief Auxiliary function for receiving solved problems from workers
        *
        * @param[out] node is the node corresponding to the solved problem
        * @param[out] lbd is the new lowerbound for the node
        * @param[out] lbdSolutionPoint is the solution point of the node
        * @param[out] lbdcnt is the number of lower bounding problems that were solved during solving the node
        * @param[out] ubdcnt is the number of upper bounding problems that were solved during solving the node
        * @param[in] status is the status of the node after solving it (NORMAL, CONVERGED, INFEASIBLE)
        * @param[in] src is the worker who solved the problem
        */
    void _recv_solved_problem(babBase::BabNode &node, double &lbd, std::vector<double> &lbdSolutionPoint, unsigned &lbdcnt,
                              unsigned &ubdcnt, const COMMUNICATION_TAG status, const int src);

    /**
        * @brief Auxiliary function for sending a new problem to a worker
        *
        * @param[in] node is the node that is sent to the worker for solving
        * @param[in] dest is the worker to whom the problem is sent
        */
    void _send_new_problem(const babBase::BabNode &node, const int dest);

#ifdef HAVE_GROWING_DATASETS
    /**
    * @brief Auxiliary function for sending new dataset to a worker
    *
    * @param[in] newDataset is the dataset that is sent to the worker for appending the datasets vector
    * @param[in] dest is the worker to whom the problem is sent
    */
    void _send_new_dataset(const std::set<unsigned int> &newDataset, const int dest);
#endif    // HAVE_GROWING_DATASETS

    /**
        * @brief Auxillary function for informing workers about occuring events
        *
        * @param[in] eventTag is the tag corresponding to the event the workers should be informed of
        * @param[in] blocking is a flag indicating if the communication should be performed in a blocking or non-blocking manner
        */
    void _inform_worker_about_event(const BCAST_TAG eventTag, const bool blocking);
    /**@}*/

    /**
        * @name MPI management and communication functions of worker
        */
    /**@{*/
    /**
        * @brief Auxiliary function for receiving a new problem from the manager
        *
        * @param[out] node is the node that is received from the manager for solving
        */
    void _recv_new_problem(babBase::BabNode &node);

#ifdef HAVE_GROWING_DATASETS
    /**
    * @brief Auxiliary function for receiving a new dataset from the manager
    */
    void _recv_new_dataset();
#endif    // HAVE_GROWING_DATASETS

    /**
        * @brief Auxiliary function for sending a new incumbent to the manager
        *
        * @param[in] ubd is the objective value of the found incumbent
        * @param[in] incumbent is the found incumbent point
        * @param[in] incumbentID is the ID of the node which holds the found incumbent
        */
    void _send_incumbent(const double ubd, const std::vector<double> incumbent, const unsigned incumbentID);

    /**
        * @brief Auxiliary function for sending a solved problem to the manager
        *
        * @param[in] node is the solved node which is sent to the manager
        * @param[in] lbd is the new lbd found for the node
        * @param[in] lbdSolutionPoint is the solution point of the node
        * @param[in] lbdcnt is the number of lower bounding problems that were solved during solving the node
        * @param[in] ubdcnt is the number of upper bounding problems that were solved during solving the node
        * @param[in] status is the status of the node after solving it (NORMAL, CONVERGED, INFEASIBLE)
        */
    void _send_solved_problem(const babBase::BabNode node, const double lbd, const std::vector<double> lbdSolutionPoint,
                              const unsigned lbdcnt, const unsigned ubdcnt, const COMMUNICATION_TAG status);

    /**
        * @brief Auxiliary function for synchronizing with the master (e.g., to manage termination, exceptions etc.)
        *
        * @param[in] req is the pending request for which the worker awaits an answer
        */
    void _sync_with_master(MPI_Request &req);

    /**
        * @brief Auxiliary function for synchronizing with the master (e.g., to manage termination, exceptions etc.)
        *
        * @param[in] req is the pending request for which the worker awaits an answer
        * @param[out] terminate is a flag that indicates if the worker should terminate the B&B loop
        */
    void _sync_with_master(MPI_Request &req, bool &terminate);
    /**@}*/
#endif

    std::unique_ptr<babBase::Brancher> _brancher;   /*!< pointer to brancher object that holds and manages the branch-and-bound tree */
    std::shared_ptr<ubp::UpperBoundingSolver> _UBS; /*!< pointer to upper bounding solver */
    std::shared_ptr<lbp::LowerBoundingSolver> _LBS; /*!< pointer to lower bounding solver */
#if defined(MAiNGO_DEBUG_MODE) && defined(HAVE_GROWING_DATASETS)
    std::shared_ptr<lbp::LowerBoundingSolver> _LBSFull; /*!< pointer to lower bounding solver using the full dataset only */
    double _currentLBDFull;                             /*!< lower bound of the current node when using the full dataset */
    std::vector<double> _lbpSolutionPointFull;          /*!< solution point of the LBP in the current node when using the full dataset */
#endif

    std::shared_ptr<Settings> _maingoSettings; /*!< pointer to object storing settings */

    /**
        * @name Internal variables for storing problem parameters
        */
    /**@{*/
    std::vector<babBase::OptimizationVariable> _originalVariables; /*!< vector holding the optimization variables */
    const unsigned _nvar;                                          /*!< stores number of optimization parameters */
    const unsigned _nvarWOaux;                                     /*!< stores number of optimization variables without additional auxiliary variables */
    std::vector<double> _lowerVarBoundsOrig;                       /*!< vector storing original lower bounds */
    std::vector<double> _upperVarBoundsOrig;                       /*!< vector storing upper bounds */
#ifdef HAVE_GROWING_DATASETS
    std::shared_ptr<std::vector<std::set<unsigned int>>> _datasets; /*!< pointer to a vector containing all available datasets */
#endif                                                              // HAVE_GROWING_DATASETS
    /**@}*/

    /**
        * @name Internal variables for storing solution information
        */
    /**@{*/
    std::vector<double> _incumbent;      /*!< vector storing solution (p^*) */
    std::vector<double> _initialPoint;   /*!< vector storing initial point */
    double _ubd;                         /*!< incumbent upper bound */
    double _lbd;                         /*!< lowest lower bound */
    double _bestLbdFathomed;             /*!< this is the lowest lower bound of a node that has been fathomed by value dominance so far (needed to compute the final optimality gap correctly) */
    bool _foundFeas;                     /*!< if a feasible point has been found */
    unsigned _firstFound;                /*!< first node to find incumbent */
    unsigned _incumbentNodeId;           /*!< node currently containing the incumbent (may already have been fathomed) */
    babBase::enums::BAB_RETCODE _status; /*!< status of the B&B */
    /**@}*/

    /**
        * @name Internal variables for heuristic approaches
        */
    /**@{*/
    double _lbdOld;             /*!< lowest lower bound before update in _update_lowest_lbd() */
    unsigned _lbdNotChanged;    /*!< counter on iterations where the lowest lbd did not change */
    bool _moreScalingActivated; /*!< bool telling whether more scaling has already been activated in the LBS */
    /**@}*/

    /**
        * @name Internal variables to store statistics
        */
    /**@{*/
    unsigned _nNodesTotal;       /*!< total nodes created in Iset */
    unsigned _nNodesLeft;        /*!< nodes left in Iset */
    unsigned _nNodesMaxInMemory; /*!< maximum number of nodes held in memory so far */
    unsigned _nNodesDeleted;     /*!< nodes deleted in Iset */
    unsigned _nNodesFathomed;    /*!< nodes fathomed in Iset */
    /**@}*/

    /**
        * @name Counters
        */
    /**@{*/
    unsigned _lbdcnt;       /*!< total number of LBPs solved */
    unsigned _ubdcnt;       /*!< total number of UBPs solved */
    double _timePassed;     /*!< total CPU time in seconds */
    double _timePreprocess; /*!< CPU time in seconds used for preprocessing */
    unsigned _daysPassed;   /*!< number of full days */
    /**@}*/

    /**
        * @name Internal variables used for printing
        */
    /**@{*/
    unsigned _linesprinted;          /*!< number of lines printed */
    unsigned _iterations;            /*!< number of iterations */
    unsigned _iterationsgap;         /*!< number defining the gap between two outputs*/
    bool _printNewIncumbent;         /*!< auxiliary variable to make sure a line is printed whenever a new incumbent, which is better than the old one for more than the tolerances, is found */
    unsigned _writeToLogEverySec;    /*!< auxiliary variable to make sure we print to log every writeToLogSec seconds */
    std::shared_ptr<Logger> _logger; /*!< pointer to MAiNGO logger */
                                     /**@}*/

#ifdef HAVE_MAiNGO_MPI
    /**
        * @name Internal variables used for MPI communication
        */
    /**@{*/
    int _rank;             /*!< rank of process*/
    int _nProcs;           /*!< number of processes*/
    BCAST_TAG _bcastTag;   /*!< MPI tag representig information which is spread among all processes*/
    MPI_Request _bcastReq; /*!< MPI request handle containing information about incoming/outgoing broadcasts*/
    /**@}*/

    /**
        * @name Internal variables used for MPI management
        */
    /**@{*/
    std::vector<bool> _informedWorkerAboutIncumbent;           /*!< stores information about which worker already knows about the current incumbent */
    bool _checkForNodeWithIncumbent;                           /*!< used to properly track the incumbent when a new one is found within the B&B tree */
    bool _confirmedTermination;                                /*!< stores whether termination was already confirmed by the user */
    unsigned _workCount;                                       /*!< number of  active workers */
    std::vector<std::pair<bool, double>> _nodesGivenToWorkers; /*!< vector holding whether worker i currently has a node and the double value of the lbd of this node */
#ifdef HAVE_GROWING_DATASETS
    std::vector<bool> _informedWorkerAboutDataset; /*!< stores information about which worker already knows about the current dataset vector */
#endif                                             // HAVE_GROWING_DATASETS
    /**@}*/

    /**
        * @name Internal variables used by worker processes
        */
    /**@{*/
    bool _pendingIncumbentUpdate; /*!< flag determining whether the workers should be informed about new incumbent */
    MPI_Request _incumbentReq;    /*!< MPI request handle for new incumbent */
    /**@}*/

#endif
};


}    // end namespace bab


}    // end namespace maingo