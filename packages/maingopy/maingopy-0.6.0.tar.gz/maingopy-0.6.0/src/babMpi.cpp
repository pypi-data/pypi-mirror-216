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

#ifdef HAVE_MAiNGO_MPI

#include "MAiNGOException.h"
#include "bab.h"
#include "getTime.h"
#include "lbp.h"
#include "mpiUtilities.h"
#include "ubp.h"

#include <limits>

using namespace maingo;
using namespace bab;


/**
* MANAGER FUNCTIONS
*/
////////////////////////////////////////////////////////////////////////////////////////
// function for recieving a solved problem from worker src
void
BranchAndBound::_recv_solved_problem(babBase::BabNode &node, double &lbd, std::vector<double> &lbdSolutionPoint, unsigned &lbdcnt,
                                     unsigned &ubdcnt, const COMMUNICATION_TAG status, const int src)
{

    const int statCount = (status == TAG_SOLVED_NODE_STATUS_NORMAL) ? 2 : 3;
    std::vector<unsigned> statistics(statCount);

    if (status == TAG_SOLVED_NODE_STATUS_NORMAL) {
        // Node solved normally ( not converged or infeasible)
        // => Receive node, lbd and corresponding point
        lbdSolutionPoint.resize(_nvar);
        // Receive node
        recv_babnode(node, src, _nvar);
        // Receive lbd
        MPI_Recv(&lbd, 1, MPI_DOUBLE, src, TAG_SOLVED_NODE_LBD, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        // Receive lbpSolutionPoint
        MPI_Recv(lbdSolutionPoint.data(), lbdSolutionPoint.size(), MPI_DOUBLE, src, TAG_SOLVED_NODE_SOLUTION_POINT, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
    else if (status == TAG_SOLVED_NODE_STATUS_CONVERGED) {
        // Node converged
        // => Send lbd
        MPI_Recv(&lbd, 1, MPI_DOUBLE, src, TAG_SOLVED_NODE_LBD, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
    else if (status == TAG_SOLVED_NODE_STATUS_INFEAS) {
        // Node infeasible
        lbd = _maingoSettings->infinity;
    }

    // Statistics and node id have to be sent in every case
    MPI_Recv(statistics.data(), statCount, MPI_UNSIGNED, src, TAG_SOLVED_NODE_STATISTICS, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

    lbdcnt = statistics[0];
    ubdcnt = statistics[1];

    // In case the node converged or was infeasible and therefore not sent back, create a dummy node
    if (status != TAG_SOLVED_NODE_STATUS_NORMAL) {
        unsigned nodeID = statistics[2];
        node            = babBase::BabNode(node.get_pruning_score(), node.get_lower_bounds(), node.get_upper_bounds(), node.get_index_dataset(), nodeID, node.get_depth(), node.get_augment_data());
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// function for sending a new problem and a new incumbent to worker dest
void
BranchAndBound::_send_new_problem(const babBase::BabNode &node, const int dest)
{

    // Check if worker knows current incumbent
    bool workerKnowsIncumbent = _informedWorkerAboutIncumbent[dest - 1];

    COMMUNICATION_TAG answerTag;
    if (!workerKnowsIncumbent) {
        answerTag                               = TAG_NEW_NODE_NEW_INCUMBENT;
        _informedWorkerAboutIncumbent[dest - 1] = true;
    }
    else {
        answerTag = TAG_NEW_NODE_NO_INCUMBENT;
    }

    // Send Request Answer
    MPI_Ssend(NULL, 0, MPI_INT, dest, answerTag, MPI_COMM_WORLD);

    // Send BabNode
    send_babnode(node, dest);

    // Only send incumbent if worker does not know it yet
    if (!workerKnowsIncumbent) {
        // Send bounds of objective function
        MPI_Ssend(&_ubd, 1, MPI_DOUBLE, dest, TAG_NEW_NODE_UBD, MPI_COMM_WORLD);

        // Send new incumbent
        MPI_Ssend(_incumbent.data(), _incumbent.size(), MPI_DOUBLE, dest, TAG_NEW_INCUMBENT, MPI_COMM_WORLD);

        // Send incumbent ID
        MPI_Ssend(&_incumbentNodeId, 1, MPI_UNSIGNED, dest, TAG_NEW_INCUMBENT_ID, MPI_COMM_WORLD);
    }
}


#ifdef HAVE_GROWING_DATASETS
////////////////////////////////////////////////////////////////////////////////////////
// function for sending a new dataset to worker dest
void
BranchAndBound::_send_new_dataset(const std::set<unsigned int> &newDataset, const int dest)
{
    // Check if worker knows current dataset vector
    bool workerKnowsDataset = _informedWorkerAboutDataset[dest - 1];

    COMMUNICATION_TAG answerTag;
    if (!workerKnowsDataset) {
        answerTag                             = TAG_NEW_NODE_NEW_DATASET;
        _informedWorkerAboutDataset[dest - 1] = true;
    }
    else {
        answerTag = TAG_NEW_NODE_NO_DATASET;
    }
    // Send Request Answer
    MPI_Ssend(NULL, 0, MPI_INT, dest, answerTag, MPI_COMM_WORLD);

    // Only send new dataset if worker does not know it yet
    if (!workerKnowsDataset) {
        // Push set into vector to send dataset at once
        unsigned int ndataNew = newDataset.size();
        MPI_Ssend(&ndataNew, 1, MPI_UNSIGNED, dest, TAG_NODE_DATAPOINT, MPI_COMM_WORLD);

        std::vector<unsigned int> datasetBuf(newDataset.begin(), newDataset.end());
        MPI_Ssend(datasetBuf.data(), ndataNew, MPI_UNSIGNED, dest, TAG_NODE_DATAPOINT, MPI_COMM_WORLD);
    }
}
#endif    // HAVE_GROWING_DATASETS


////////////////////////////////////////////////////////////////////////////////////////
// auxillary function for informing workers about occuring events
void
BranchAndBound::_inform_worker_about_event(const BCAST_TAG eventTag, const bool blocking)
{
    // Wait for pending bcast if there is one
    if (_bcastTag != BCAST_NOTHING_PENDING) {
        MPI_Wait(&_bcastReq, MPI_STATUS_IGNORE);
    }

    // Set bcast buffer and broadcast it
    _bcastTag = eventTag;
    MPI_Ibcast(&_bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD, &_bcastReq);

    // If the broadcast should be blocking wait for it to return
    if (blocking) {
        MPI_Wait(&_bcastReq, MPI_STATUS_IGNORE);
        _bcastTag = BCAST_NOTHING_PENDING;
    }
}


/**
* WORKER FUNCTIONS
*/
////////////////////////////////////////////////////////////////////////////////////////
// function for sending incumbent to the master
void
BranchAndBound::_send_incumbent(const double ubd, const std::vector<double> incumbent, const unsigned incumbentID)
{

    // Create new buffer for incumbent, the ubd and the Node ID
    std::vector<double> incumbentBuf(_nvarWOaux + 2);
    incumbentBuf[_nvarWOaux]     = ubd;
    incumbentBuf[_nvarWOaux + 1] = incumbentID;
    for (unsigned i = 0; i < _nvarWOaux; i++) {
        incumbentBuf[i] = incumbent[i];
    }

    // Send the Incumbent
    MPI_Issend(incumbentBuf.data(), _nvarWOaux + 2, MPI_DOUBLE, 0, TAG_FOUND_INCUMBENT, MPI_COMM_WORLD, &_incumbentReq);
    _pendingIncumbentUpdate = true;
}


////////////////////////////////////////////////////////////////////////////////////////
// function for sending a solved problem to the master
void
BranchAndBound::_send_solved_problem(const babBase::BabNode node, const double lbd, const std::vector<double> lbdSolutionPoint,
                                     const unsigned lbdcnt, const unsigned ubdcnt, const COMMUNICATION_TAG status)
{
    const int statCount = (status == TAG_SOLVED_NODE_STATUS_NORMAL) ? 2 : 3;
    unsigned counts[3]  = {lbdcnt, ubdcnt, (unsigned int)node.get_ID()};

    if (status == TAG_SOLVED_NODE_STATUS_NORMAL) {
        // Node solved normally ( not converged or infeasible)
        // => Send node, lbd and corresponding point
        // Send node
        send_babnode(node, 0);
        // Send lbd
        MPI_Ssend(&lbd, 1, MPI_DOUBLE, 0, TAG_SOLVED_NODE_LBD, MPI_COMM_WORLD);
        // Send lbdSolutionPoint
        MPI_Ssend(lbdSolutionPoint.data(), lbdSolutionPoint.size(), MPI_DOUBLE, 0, TAG_SOLVED_NODE_SOLUTION_POINT, MPI_COMM_WORLD);
    }
    else if (status == TAG_SOLVED_NODE_STATUS_CONVERGED) {
        // Node converged
        // => Send lbd
        MPI_Ssend(&lbd, 1, MPI_DOUBLE, 0, TAG_SOLVED_NODE_LBD, MPI_COMM_WORLD);
    }

    // Statistics have to be sent in every case
    MPI_Ssend(counts, statCount, MPI_UNSIGNED, 0, TAG_SOLVED_NODE_STATISTICS, MPI_COMM_WORLD);
}


////////////////////////////////////////////////////////////////////////////////////////
// function for recieving a new problem from the master with a new incumbent
void
BranchAndBound::_recv_new_problem(babBase::BabNode &node)
{
    MPI_Status status;
    MPI_Recv(NULL, 0, MPI_INT, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

    // Receive BabNode
    recv_babnode(node, 0, _nvar);

    if (status.MPI_TAG == TAG_NEW_NODE_NEW_INCUMBENT) {
        _incumbent.resize(_nvarWOaux);

        // Receive bounds of objective function
        MPI_Recv(&_ubd, 1, MPI_DOUBLE, 0, TAG_NEW_NODE_UBD, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        // Receive new incumbent
        MPI_Recv(_incumbent.data(), _incumbent.size(), MPI_DOUBLE, 0, TAG_NEW_INCUMBENT, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        // Receive incumbent ID
        MPI_Recv(&_incumbentNodeId, 1, MPI_UNSIGNED, 0, TAG_NEW_INCUMBENT_ID, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        _LBS->update_incumbent_LBP(_incumbent);
    }
}


#ifdef HAVE_GROWING_DATASETS
////////////////////////////////////////////////////////////////////////////////////////
// function for recieving a new dataset from the master
void
BranchAndBound::_recv_new_dataset()
{
    MPI_Status status;
    MPI_Recv(NULL, 0, MPI_INT, 0, MPI_ANY_TAG, MPI_COMM_WORLD, &status);

    if (status.MPI_TAG == TAG_NEW_NODE_NEW_DATASET) {
        // Receive dataset
        unsigned int ndataNew;
        MPI_Recv(&ndataNew, 1, MPI_UNSIGNED, 0, TAG_NODE_DATAPOINT, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        std::vector<unsigned int> datasetBuf;
        datasetBuf.resize(ndataNew);
        MPI_Recv(datasetBuf.data(), datasetBuf.size(), MPI_UNSIGNED, 0, TAG_NODE_DATAPOINT, MPI_COMM_WORLD, MPI_STATUS_IGNORE);

        // Add dataset and corresponding subgraph to solvers
        std::set<unsigned int> newDataset;
        for (auto idx : datasetBuf) {
            newDataset.insert(newDataset.end(), idx);
        }

        _LBS->update_datasets_and_storedSubgraphs(newDataset);
        _UBS->update_datasets_and_storedSubgraphs(newDataset);
    }
}
#endif    // HAVE_GROWING_DATASETS


////////////////////////////////////////////////////////////////////////////////////////
// function for syncing with master
void
BranchAndBound::_sync_with_master(MPI_Request &req)
{
    bool dummy;
    _sync_with_master(req, dummy);
}


////////////////////////////////////////////////////////////////////////////////////////
// function for syncing with master via broadcast
void
BranchAndBound::_sync_with_master(MPI_Request &req, bool &terminate)
{
    terminate = false;
    int index;

    do {
        // Wait for either node or bcast request to return
        MPI_Request requests[2] = {_bcastReq, req};
        MPI_Waitany(2, requests, &index, MPI_STATUS_IGNORE);

        // Handle broadcast messages from manager
        if (index == 0) {
            MPI_Status status;
            int flag;

            MPI_Request_get_status(req, &flag, &status);
            if (_bcastTag == BCAST_EXCEPTION) {    // Other worker ran into an exception
                _logger->print_message("  Received exception flag from master.\n", VERB_NORMAL, BAB_VERBOSITY);
                // Cancel pending node request
                MPI_Cancel(&req);
                MPI_Request_free(&req);
                throw MAiNGOMpiException("  Received exception flag from master", MAiNGOMpiException::ORIGIN_OTHER);
            }
            else if (_bcastTag == BCAST_TERMINATE) {    // Termination condition reached
                                                        // Cancel pending node request
                MPI_Cancel(&req);
                MPI_Request_free(&req);

                terminate = true;
                return;
            }
            else if (_bcastTag == BCAST_FOUND_FEAS) {    // Other worker found a feasible point
                _foundFeas = true;
            }
            else if (_bcastTag == BCAST_SCALING_NEEDED) {    // Activate scaling
                _LBS->activate_more_scaling();
            }

            // Open buffer for new incoming broadcasts
            MPI_Ibcast(&_bcastTag, 1, MPI_INT, 0, MPI_COMM_WORLD, &_bcastReq);
        }
    } while (index == 0);
}


////////////////////////////////////////////////////////////////////////////////////////
// function for handling exceptions
void
BranchAndBound::_communicate_exception_and_throw(const maingo::MAiNGOMpiException &e)
{

    MAiNGO_IF_BAB_MANAGER
        _inform_worker_about_event(BCAST_EXCEPTION, true);
        MAiNGO_ELSE
            if (e.origin() == MAiNGOMpiException::ORIGIN_ME) {
                std::cout << e.what() << std::endl;
                MPI_Request req;
                MPI_Issend(NULL, 0, MPI_INT, 0, TAG_EXCEPTION, MPI_COMM_WORLD, &req);

                _sync_with_master(req);
            }
        MAiNGO_END_IF

        throw e;
}
#endif
