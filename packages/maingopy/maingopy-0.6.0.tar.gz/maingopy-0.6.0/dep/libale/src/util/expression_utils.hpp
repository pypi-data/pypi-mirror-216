/**********************************************************************************
 * Copyright (c) 2023 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 **********************************************************************************/

#pragma once

#include <map>

#include "visitor_utils.hpp"
#include "evaluator.hpp"
#include "symbol_table.hpp"

namespace ale {

    /**
     * Get shape of symbol
     * 
     * Returns an empty vector if the symbol is 0-dimensional
     * In case the parameter is a 0-dimensional set, a flattened list of shapes of its entries is returned (see get_set_shape)
     * Throws an error if the symbol cannot be found in symbol_table
     */
    std::vector<size_t> get_parameter_shape(const std::string& name, symbol_table& symbols);

    /**
     * Get shape of set parameter
     * Throws if the symbol cannot be found in the symbol_table
     */
    std::vector<std::vector<size_t>> get_set_shape(const std::string& name, symbol_table& symbols);

    /**
     * Get shape of expression
     * 
     * This is a more efficient way of getting evaluate_expression(expr).shape()
     * If the return type is 0-dimensional an empty vector is returned
     * 
     * Note: for efficiency it is not checked if
     *  - the index in entry_nodes is actually valid
     *  - the children of tensor_nodes have the same shape
     *  - the shapes of arguments in function_nodes match
     * 
     * For the usage in function_node evaluation this is fine since these conditions
     * will be checked by the calling evaluator.
     */
    std::vector<size_t> get_expression_shape(value_node_variant expr, symbol_table& symbols);

    /**
     * Returns if the tree with root node is constant.
     */
    bool is_tree_constant(value_node_variant node, symbol_table& symbols);

    //
    // get_subtree_value
    //

    /**
     * If the tree starting with node is constant return its evaluation.
     */
    template <typename TType>
    std::optional<owning_ref<TType>> get_subtree_value(value_node<TType>* node, symbol_table& symbols) {
        // if node is constant evaluate it with an empty symbol table and return the value
        if (is_tree_constant(node, symbols)) {
            return util::evaluate_expression(node, symbols);
        }

        // return nothing
        return {};
    }

    /**
     * Replaces all constant subtrees in expr
     */
    void replace_constant_subtrees(value_node_ptr_variant expr, symbol_table& symbols);

    /**
     * Find all parameters with the given name in the expression
     */
    std::vector<value_node_ptr_variant> find_parameter(const std::string& parameter_name, value_node_ptr_variant expr);

    /**
     * Replace any parameter in the expression with a name contained in the map with the corresponding value_node.
     * If the types do not match an error will be thrown.
     */
    void replace_parameters(value_node_ptr_variant node, const std::map<std::string, value_node_variant>& arg_map);

    /**
     * Replace any parameter in the expression with a name contained in the map with the corresponding value_node.
     * If the types do not match an error will be thrown.
     */
    template <typename TType>
    void replace_parameters(expression<TType>& expr, const std::map<std::string, value_node_variant>& arg_map) {
        replace_parameters(expr.get_root(), arg_map);
    }

}
