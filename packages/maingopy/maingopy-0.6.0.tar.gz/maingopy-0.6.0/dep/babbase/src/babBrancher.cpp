/**********************************************************************************
 * Copyright (c) 2019-2023 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 **********************************************************************************/

#include "babBrancher.h"


using namespace babBase;


////////////////////////////////////////////////////////////////////////////////////////
// Constructor for brancher class
Brancher::Brancher(const std::vector<OptimizationVariable>& variables):
    _globalOptimizationVariables(variables)
{

    set_branching_dimension_selection_strategy(enums::BV::BV_PSCOSTS);
    _node_score_calculating_function = low_pruning_score_first;
    _pseudocosts_down                = std::vector<double>(variables.size(), 0);
    _pseudocosts_up                  = _pseudocosts_down;
    _number_of_trials_down           = std::vector<int>(variables.size(), 0);
    _number_of_trials_up             = _number_of_trials_down;
}


////////////////////////////////////////////////////////////////////////////////////////
// Set new branching dimension selection strategy
void
Brancher::set_branching_dimension_selection_strategy(const enums::BV branchingVarStratSelection)
{
    switch (branchingVarStratSelection) {
        case enums::BV_ABSDIAM:
            // Search for largest delta p and select that variable to branch on
            _select_branching_dimension = select_branching_dimension_absdiam;
            break;
        case enums::BV_RELDIAM:
            _select_branching_dimension = select_branching_dimension_reldiam;
            break;
        case enums::BV_PSCOSTS:
            using namespace std::placeholders;    // for _1, _2, _3
            _select_branching_dimension = std::bind(&Brancher::_select_branching_dimension_pseudo_costs, this, _1, _2, _3, _4);
            break;
        default:
            throw(BranchAndBoundBaseException("Error in bab - branching variable selection"));
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// Set the node selection strategy
void
Brancher::set_node_selection_strategy(const enums::NS nodeSelectionStratType)
{
    _internalBranchAndBoundTree.set_node_selection_strategy(nodeSelectionStratType);
}


////////////////////////////////////////////////////////////////////////////////////////
// Set the function for calculating node scores
void
Brancher::set_node_selection_score_function(
    std::function<double(const BabNode&, const std::vector<OptimizationVariable>&)> newNodeScoreFunction)
{
    _node_score_calculating_function = newNodeScoreFunction;
}


////////////////////////////////////////////////////////////////////////////////////////
// Registers the changes made to a node during processing to extract information for branching heuristics.
void
Brancher::register_node_change(const int Id, const BabNode& nodeAfterProcessing)
{

    auto it = std::find_if(_nodesWaitingForResponse.begin(), _nodesWaitingForResponse.end(), [Id](const std::tuple<unsigned, double, BranchingHistoryInfo>& s) { return (std::get<0>(s) == Id); });
    // here pseudocosts could be calculated by calling _update_branching_scores
    // it points to the nodeBeforeChanges
    if (it != _nodesWaitingForResponse.end()) {
        BranchingHistoryInfo info                             = std::move(std::get<2>(*it));
        int variableInd                                       = info.branchVar;
        BranchingHistoryInfo::BranchStatus branchingDirection = info.branchStatus;
        if ((branchingDirection != BranchingHistoryInfo::BranchStatus::wasNotBranched)) {
            double originalPruningScore            = std::get<1>(*it);
            double originalLowerBound              = info.parentLowerBound;
            double originalUpperBound              = info.parentUpperBound;
            double originalRelaxationSolutionPoint = info.relaxationSolutionPointForBranchingVariable;

            double branchingPoint = _calculate_branching_point(originalLowerBound, originalUpperBound, originalRelaxationSolutionPoint);
            double dminus, dplus;
            std::tie(dminus, dplus) = calculate_pseudocost_multipliers_minus_and_plus(_globalOptimizationVariables[variableInd].get_variable_type(), originalLowerBound, originalUpperBound, branchingPoint, originalRelaxationSolutionPoint);

            if (branchingDirection == BranchingHistoryInfo::BranchStatus::wasBranchedUp)    // we have one observation what happened after branching up
            {
                int K                = _number_of_trials_up[variableInd];
                double oldPseudocost = _pseudocosts_up[variableInd];
                if (K == 0)
                    oldPseudocost = 0;
                _pseudocosts_up[variableInd]      = (K * oldPseudocost + (nodeAfterProcessing.get_pruning_score() - originalPruningScore) / (dplus) / (this->get_pruning_score_threshold() - originalPruningScore)) / (K + 1);
                _number_of_trials_up[variableInd] = K + 1;
            }
            else {
                int K                = _number_of_trials_down[variableInd];
                double oldPseudocost = _pseudocosts_down[variableInd];
                if (K == 0)
                    oldPseudocost = 0;

                _pseudocosts_down[variableInd]      = (K * oldPseudocost + (nodeAfterProcessing.get_pruning_score() - originalPruningScore) / (dminus) / (this->get_pruning_score_threshold() - originalPruningScore)) / (K + 1);
                _number_of_trials_down[variableInd] = K + 1;
            }
        }
        _nodesWaitingForResponse.erase(it);
    }
    else {
        throw BranchAndBoundBaseException("Registered Id not found, called with node:", nodeAfterProcessing);
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// Inserts the root node into the tree.
void
Brancher::insert_root_node(const BabNode& rootNode)
{
    _internalBranchAndBoundTree.add_node(this->_create_node_with_info_from_node(rootNode, 0, BranchingHistoryInfo::BranchStatus::wasNotBranched, 0, 0, 0));
}


////////////////////////////////////////////////////////////////////////////////////////
// Function that branches on a node and (normally) adds two new children to the BranchAndBoundTree.
std::pair<bool /*isFixed*/, bool /*canBeConsideredFixed*/>
Brancher::branch_on_node(const BabNode& parentNode,
    const std::vector<double>& relaxationSolutionPoint,
    double relaxationSolutionObjValue, double relNodeSizeTol)
{
    std::vector<double> parentLowerBounds = parentNode.get_lower_bounds();
    std::vector<double> parentUpperBounds = parentNode.get_upper_bounds();
    bool nodeIsFixed                      = false;
    bool nodeCanBeThreatedAsFixed         = false;

    {
        std::vector<double> boundDifference;
        std::vector<double> relBoundDifference;
        boundDifference.reserve(parentLowerBounds.size());
        std::transform(parentLowerBounds.begin(), parentLowerBounds.end(), parentUpperBounds.begin(), std::back_inserter(boundDifference), [](double a, double b) { return b - a; });
        //   no gap between upper and lower (   upper>  lower )  left
        nodeIsFixed = std::none_of(boundDifference.begin(), boundDifference.end(), [](double val) { return val > 0.0; });


        for (size_t i = 0; i < boundDifference.size(); ++i) {
            relBoundDifference.push_back((boundDifference[i] > 0) ? (boundDifference[i] / (_globalOptimizationVariables[i].get_upper_bound() - _globalOptimizationVariables[i].get_lower_bound())) : 0.);    // need to account for the case where a variable was initially already fixed
        }
        //  if all dimensions have a relative ( to the original bounds)  gap between the bounds smaller than the given tolerance
        nodeCanBeThreatedAsFixed = std::none_of(relBoundDifference.begin(), relBoundDifference.end(), [relNodeSizeTol](double relSizeOfDimension) { return relSizeOfDimension > relNodeSizeTol; });
    }
    if (nodeIsFixed)    // Only happens for pure integer problems
    {
        // The node has been fixed, e.g. by probing.
        // Is readded to the tree, because it may need to be solved one more time.
        //all but the first argument are
        _internalBranchAndBoundTree.add_node(this->_create_node_with_info_from_node(parentNode, 0, BranchingHistoryInfo::BranchStatus::wasNotBranched, 0, 0, 0));
    }
    else if (nodeCanBeThreatedAsFixed)    // May also happen for problems with continuous variables if the node becomes too small due to excessive branching
    {
        //logged outside
    }
    else {
        unsigned branchVar = _select_branching_dimension(
            parentNode, relaxationSolutionPoint, relaxationSolutionObjValue, this->_globalOptimizationVariables);

        double branchVariableRelaxSolutionPoint;
        if (relaxationSolutionPoint.size() != parentLowerBounds.size()) {
            branchVariableRelaxSolutionPoint = 0.5 * (parentLowerBounds[branchVar] + parentUpperBounds[branchVar]);
        }
        else {
            branchVariableRelaxSolutionPoint = relaxationSolutionPoint[branchVar];
        }

        std::pair<BabNodeWithInfo, BabNodeWithInfo> children = _create_children(branchVar, parentNode, branchVariableRelaxSolutionPoint);
        _internalBranchAndBoundTree.add_node(children.first);
        _internalBranchAndBoundTree.add_node(children.second);
    }
    return std::make_pair(nodeIsFixed, nodeCanBeThreatedAsFixed);
}


#ifdef BABBASE_HAVE_GROWING_DATASETS
/////////////////////////////////////////////////////////////////////////////////////////////////
// Function for creating one child from parent node and adding it to BaB tree
void
Brancher::add_node_with_new_data_index(const BabNode& parentNode, const unsigned int newDataIndex)
{
    // Mainly copy of parent node, with new index of dataset and marked as augmented
    BabNode child = BabNode(parentNode.get_pruning_score(), parentNode.get_lower_bounds(), parentNode.get_upper_bounds(), newDataIndex, _internalBranchAndBoundTree.get_valid_id(), parentNode.get_depth() + 1, true);

    _internalBranchAndBoundTree.add_node_anyway(this->_create_node_with_info_from_node(child, 0, BranchingHistoryInfo::BranchStatus::wasNotBranched, 0, 0, 0));
}
#endif // BABBASE_HAVE_GROWING_DATASETS


/////////////////////////////////////////////////////////////////////////////////////////////////
// Helper function for getting all nodes created during strong branching
std::vector<BabNode>
Brancher::get_all_nodes_from_strong_branching(const BabNode& parentNode, const std::vector<double>& relaxationSolutionPoint)
{
    std::vector<BabNode> returnedNodes;
    returnedNodes.reserve(parentNode.get_upper_bounds().size());
    for (unsigned i = 0; i < parentNode.get_upper_bounds().size(); i++) {
        unsigned branchVar = i;
        double branchVariableRelaxSolutionPoint;
        if (relaxationSolutionPoint.size() != parentNode.get_upper_bounds().size()) {
            branchVariableRelaxSolutionPoint = 0.5 * (parentNode.get_lower_bounds()[branchVar] + parentNode.get_upper_bounds()[branchVar]);
        }
        else {
            branchVariableRelaxSolutionPoint = relaxationSolutionPoint[branchVar];
        }
        std::pair<BabNodeWithInfo, BabNodeWithInfo> children = _create_children(branchVar, parentNode, branchVariableRelaxSolutionPoint);
        const BabNodeWithInfo& left                          = children.first;
        this->_nodesWaitingForResponse.push_back(std::make_tuple(left.get_ID(), left.get_pruning_score(), left.branchingInfo));
        const BabNodeWithInfo& right = children.second;
        this->_nodesWaitingForResponse.push_back(std::make_tuple(right.get_ID(), right.get_pruning_score(), right.branchingInfo));
        returnedNodes.push_back(std::move(children.first.node));
        returnedNodes.push_back(std::move(children.second.node));
    }
    return returnedNodes;
}


/////////////////////////////////////////////////////////////////////////////////////////////////
// Helper function for creating nodes from parent node once branch variable has been decided
std::pair<BabNodeWithInfo, BabNodeWithInfo>
Brancher::_create_children(unsigned branchVar, const BabNode& parentNode, double branchVariableRelaxSolutionPoint)
{
    // Child nodes inherit dataset of parent node
    const unsigned int parentIndexDataset = parentNode.get_index_dataset();

    // Simple rule for now, split dimension at midpoint
    const std::vector<double>& parentLowerBounds = parentNode.get_lower_bounds();
    const std::vector<double>& parentUpperBounds = parentNode.get_upper_bounds();

    std::vector<double> leftChildUpperBounds(parentUpperBounds);
    std::vector<double> rightChildLowerBounds(parentLowerBounds);
    double branchPoint = _calculate_branching_point(parentLowerBounds[branchVar], parentUpperBounds[branchVar], branchVariableRelaxSolutionPoint);

    enums::VT varType(this->_globalOptimizationVariables[branchVar].get_variable_type());
    switch (varType) {
        case enums::VT_CONTINUOUS:
            leftChildUpperBounds[branchVar]  = branchPoint;
            rightChildLowerBounds[branchVar] = branchPoint;
            break;
        case enums::VT_BINARY:
        case enums::VT_INTEGER:
            // round down continuous-valued upper bounds
            leftChildUpperBounds[branchVar]  = floor(branchPoint);
            rightChildLowerBounds[branchVar] = floor(branchPoint) + 1;
            break;
        default:
            throw(BranchAndBoundBaseException("Error in bab - creating branch nodes: unknown variable type"));
            break;
    }

    BabNode leftChild                  = BabNode(parentNode.get_pruning_score(), parentLowerBounds, leftChildUpperBounds, parentIndexDataset,
                                _internalBranchAndBoundTree.get_valid_id(), parentNode.get_depth() + 1, false);
    BabNode rightChild                 = BabNode(parentNode.get_pruning_score(), rightChildLowerBounds, parentUpperBounds, parentIndexDataset,
                                 _internalBranchAndBoundTree.get_valid_id(), parentNode.get_depth() + 1, false);
    BabNodeWithInfo leftChildWithInfo  = this->_create_node_with_info_from_node(leftChild, branchVar, BranchingHistoryInfo::BranchStatus::wasBranchedDown, branchVariableRelaxSolutionPoint, parentLowerBounds[branchVar], parentUpperBounds[branchVar]);
    BabNodeWithInfo rightChildWithInfo = this->_create_node_with_info_from_node(rightChild, branchVar, BranchingHistoryInfo::BranchStatus::wasBranchedUp, branchVariableRelaxSolutionPoint, parentLowerBounds[branchVar], parentUpperBounds[branchVar]);
    return std::make_pair(leftChildWithInfo, rightChildWithInfo);
}


////////////////////////////////////////////////////////////////////////////////////////
// Creates a node with added information.
BabNodeWithInfo
Brancher::_create_node_with_info_from_node(BabNode normalNode, unsigned branchedVariable, BranchingHistoryInfo::BranchStatus branchStatus, double variableRelaxationSolutionPoint, double parentLowerBound, double parentUpperBound) const
{
    double nodeSelectionScore = _node_score_calculating_function(normalNode, this->_globalOptimizationVariables);

    BabNodeWithInfo nodeWithInfo(normalNode, nodeSelectionScore);
    nodeWithInfo.branchingInfo.branchVar                                   = branchedVariable;
    nodeWithInfo.branchingInfo.branchStatus                                = branchStatus;
    nodeWithInfo.branchingInfo.parentLowerBound                            = parentLowerBound;
    nodeWithInfo.branchingInfo.parentUpperBound                            = parentUpperBound;
    nodeWithInfo.branchingInfo.relaxationSolutionPointForBranchingVariable = variableRelaxationSolutionPoint;
    return nodeWithInfo;
}


////////////////////////////////////////////////////////////////////////////////////////
// Decreases the pruning score threshold to the supplied value.
double
Brancher::decrease_pruning_score_threshold_to(const double newThreshold)
{
    if (_internalBranchAndBoundTree.get_pruning_score_threshold() > newThreshold) {
        return this->_internalBranchAndBoundTree.set_pruning_score_threshold(newThreshold);
    }
    else {
        return std::numeric_limits<double>::infinity();
    }
}


////////////////////////////////////////////////////////////////////////////////////////
// Returns the next BabNode to process according to the node selection strategy and node selection scores.
BabNode
Brancher::get_next_node()
{
    BabNodeWithInfo next = _internalBranchAndBoundTree.pop_next_node();

    this->_nodesWaitingForResponse.push_back(std::make_tuple(next.get_ID(), next.get_pruning_score(), next.branchingInfo));
    return std::move(next);
}


////////////////////////////////////////////////////////////////////////////////////////
// When the domain of a variable is branched on, this function decides at which point it is branched (only makes a difference for continous variables).
double
Brancher::_calculate_branching_point(double lowerBound, double upperBound, double relaxationValue) const
{
    return 0.5 * (lowerBound + upperBound);
}


////////////////////////////////////////////////////////////////////////////////////////
// Function for selecting the variable to branch on by choosing the one with the largest diameter
unsigned
babBase::select_branching_dimension_absdiam(const BabNode& parentNode,
                                            const std::vector<double>& relaxationSolutionPoint,
                                            const double relaxationSolutionObjValue,
                                            const std::vector<OptimizationVariable>& globalOptimizationVars)
{
    std::vector<double> lowerVarBounds = parentNode.get_lower_bounds();
    std::vector<double> upperVarBounds = parentNode.get_upper_bounds();
    unsigned branchVar                 = 0;
    double deltaBounds(0);
    double branchDimDistanceOfSolutionPointFromBounds = 0.0;

    for (unsigned i = 0; i < lowerVarBounds.size(); ++i) {
        double distanceOfSolutionPointFromBounds = 0.5;
        if (relaxationSolutionPoint.size() == lowerVarBounds.size()) {
            distanceOfSolutionPointFromBounds = relative_distance_to_closest_bound(relaxationSolutionPoint[i], lowerVarBounds[i], upperVarBounds[i], globalOptimizationVars[i]);
        }
        double scaledAbsoluteDiameter = (upperVarBounds[i] - lowerVarBounds[i]) * globalOptimizationVars[i].get_branching_priority();
        if ((scaledAbsoluteDiameter > deltaBounds) || (scaledAbsoluteDiameter == deltaBounds && distanceOfSolutionPointFromBounds > branchDimDistanceOfSolutionPointFromBounds)) {
            deltaBounds                                = scaledAbsoluteDiameter;
            branchVar                                  = i;
            branchDimDistanceOfSolutionPointFromBounds = distanceOfSolutionPointFromBounds;
        }
    }
    assert(deltaBounds > 0.0);    // make sure if statement was not always false (!)

    return branchVar;
}


////////////////////////////////////////////////////////////////////////////////////////
// Function for selecting the variable to branch on by choosing the one with the largest diameter relative to the original one
unsigned
babBase::select_branching_dimension_reldiam(const BabNode& parentNode,
                                            const std::vector<double>& relaxationSolutionPoint,
                                            const double relaxationSolutionObjValue,
                                            const std::vector<OptimizationVariable>& globalOptimizationVars)
{
    double deltaBounds(0);
    double relSizeDim(0);
    double branchDimDistanceOfSolutionPointFromBounds = 0.0;
    unsigned branchVar                                = 0;
    std::vector<double> lowerVarBounds                = parentNode.get_lower_bounds();
    std::vector<double> upperVarBounds                = parentNode.get_upper_bounds();
    for (unsigned i = 0; i < lowerVarBounds.size(); ++i) {
        relSizeDim = ((upperVarBounds[i] - lowerVarBounds[i]) > 0) ? ((upperVarBounds[i] - lowerVarBounds[i]) / (globalOptimizationVars[i].get_upper_bound() - globalOptimizationVars[i].get_lower_bound())) : 0.;    // need to account for the case where a variable was initially already fixed
        // TODO: relNodeSize = std::max(relSizeDim, relNodeSize); Need to add need toBranch Case
        double tmpdeltap(relSizeDim * globalOptimizationVars[i].get_branching_priority());
        double distanceOfSolutionPointFromBounds = 0.5;
        if (relaxationSolutionPoint.size() == lowerVarBounds.size()) {
            distanceOfSolutionPointFromBounds = relative_distance_to_closest_bound(relaxationSolutionPoint[i], lowerVarBounds[i], upperVarBounds[i], globalOptimizationVars[i]);
        }
        if ((tmpdeltap > deltaBounds) || (tmpdeltap == deltaBounds && distanceOfSolutionPointFromBounds > branchDimDistanceOfSolutionPointFromBounds)) {
            deltaBounds                                = tmpdeltap;
            branchVar                                  = i;
            branchDimDistanceOfSolutionPointFromBounds = distanceOfSolutionPointFromBounds;
        }
    }
    assert(deltaBounds > 0.0);    // make sure if statement was not always false (!)
    return branchVar;
}


////////////////////////////////////////////////////////////////////////////////////////
// How to select the dimension in which to branch when using pseudo costs
unsigned
Brancher::_select_branching_dimension_pseudo_costs(const BabNode& parentNode,
                                                   const std::vector<double>& relaxationSolutionPoint,
                                                   const double relaxationSolutionObjValue,
                                                   const std::vector<OptimizationVariable>& globalOptimizationVars) const
{
    // After: Branching and Bounds Tightening Techniques for Non-Convex MINLP from Pietro Belotti et. al

    double alpha                         = 0.15;
    unsigned bestVariableToBranchOnIndex = 0;
    double bestScore                     = 0;
    double dbest;
    for (unsigned variableIndex = 0; variableIndex < globalOptimizationVars.size(); variableIndex++) {

        double delta_i_minus = 0;
        double delta_i_plus  = 0;

        double relaxationSolutionPointAtVariableIndex;
        if (relaxationSolutionPoint.size() != parentNode.get_upper_bounds().size()) {
            relaxationSolutionPointAtVariableIndex = 0.5 * (parentNode.get_lower_bounds()[variableIndex] + parentNode.get_upper_bounds()[variableIndex]);
        }
        else {
            relaxationSolutionPointAtVariableIndex = relaxationSolutionPoint[variableIndex];
        }

        double branchingPoint = _calculate_branching_point(parentNode.get_lower_bounds()[variableIndex], parentNode.get_upper_bounds()[variableIndex], relaxationSolutionPointAtVariableIndex);

        std::tie(delta_i_minus, delta_i_plus) = calculate_pseudocost_multipliers_minus_and_plus(globalOptimizationVars[variableIndex].get_variable_type(), parentNode.get_lower_bounds()[variableIndex], parentNode.get_upper_bounds()[variableIndex], branchingPoint, relaxationSolutionPointAtVariableIndex);

        double estimatedImprovementUp   = _pseudocosts_up[variableIndex] * (delta_i_plus);
        double estimatedImprovementDown = _pseudocosts_down[variableIndex] * (delta_i_minus);

        //double score = globalOptimizationVars[variableIndex].get_branching_priority()*( alpha * std::max(estimatedImprovementUp, estimatedImprovementDown) + (1 - alpha)*std::min(estimatedImprovementUp, estimatedImprovementDown));
        double score = globalOptimizationVars[variableIndex].get_branching_priority() * ((std::max(estimatedImprovementUp, estimatedImprovementDown) + 1.0e-6) * (std::min(estimatedImprovementUp, estimatedImprovementDown) + 1.0e-6));
        if (score > bestScore) {
            bestScore                   = score;
            bestVariableToBranchOnIndex = variableIndex;
            dbest                       = delta_i_plus;
        }
        if (variableIndex == 0) {
            //std::cout << " 0 score " << score << " d" << delta_i_plus<< std::endl;
        }
    }
    //std::cout << "Branching on variable: " << bestVariableToBranchOnIndex << " with score of " << bestScore << "d: "<<dbest<<std::endl;
    // if(bestVariableToBranchOnIndex==0) std::cout << "Branching on variable: " << bestVariableToBranchOnIndex << " with score of " << bestScore << "d: " << dbest << std::endl;
    return bestVariableToBranchOnIndex;
}

//////////////////////////////////////////////////////////
// Calculate the multiplier for calculation of pseudocosts, the definition of the multipliers is for integer variables the change caused by rounding the relaxation solution point up or down
// For continous variables we follow the rb-int-br-rev strategy from Branching and Bounds Tightening Techniques for Non-Convex MINLP from Pietro Belotti et. al
std::pair<double, double>
babBase::calculate_pseudocost_multipliers_minus_and_plus(enums::VT varType, double lowerBound, double upperBound, double branchingPoint, double relaxationSolutionPoint)
{
    double delta_i_minus = 0;
    double delta_i_plus  = 0;
    if (varType == enums::VT_CONTINUOUS) {
        // using rb-int-br-rev for now
        delta_i_minus = upperBound - branchingPoint;
        delta_i_plus  = branchingPoint - lowerBound;
    }
    else {
        delta_i_minus = relaxationSolutionPoint - std::floor(relaxationSolutionPoint);
        delta_i_plus  = std::ceil(relaxationSolutionPoint) - relaxationSolutionPoint;
    }
    return std::make_pair(delta_i_minus, delta_i_plus);
}


////////////////////////////////////////////////////////////////////////////////////////
// Compute distance to closest bound
double
babBase::relative_distance_to_closest_bound(double pointValue, double bound1, double bound2, const babBase::OptimizationVariable& variable)
{
    return std::min(std::abs((pointValue - bound1) / (variable.get_upper_bound() - variable.get_lower_bound())),
                    std::abs((pointValue - bound2) / (variable.get_upper_bound() - variable.get_lower_bound())));
}


////////////////////////////////////////////////////////////////////////////////////////
// Auxiliary function for extracting the node with the lowest pruning score
double
babBase::low_pruning_score_first(const BabNode& candidate, const std::vector<OptimizationVariable>& globalVars)
{
    return -candidate.get_pruning_score();
}


////////////////////////////////////////////////////////////////////////////////////////
// Auxiliary function for extracting the node with the lowest id (i.e., oldest node)
double
babBase::low_id_first(const BabNode& candidate, const std::vector<OptimizationVariable>& globalVars)
{
    return -candidate.get_ID();
}


////////////////////////////////////////////////////////////////////////////////////////
// Auxiliary function for extracting the node with the highest id (i.e., newest node)
double
babBase::high_id_first(const BabNode& candidate, const std::vector<OptimizationVariable>& globalVars)
{
    return candidate.get_ID();
}