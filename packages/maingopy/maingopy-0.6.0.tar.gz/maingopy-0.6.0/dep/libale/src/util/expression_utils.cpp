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

#include "expression_utils.hpp"

#include "util/visitor_utils.hpp"

namespace ale {

    /** 
     * Sets the member shape to the shape of the first visited symbol.
     */
    struct get_parameter_shape_visitor {
        get_parameter_shape_visitor(symbol_table& symbols): symbols(symbols) {}

        template <typename TType>
        void operator()(function_symbol<TType>* sym) {
            throw std::invalid_argument("shape of function_symbol cannot be known. Tried to retrieve shape of function_symbol \"" + sym->m_name + "\"");
        }

        template <typename TType>
        void operator()(expression_symbol<TType>* sym) {
            shape = get_expression_shape(sym->m_value.get(), symbols);
        }

        template <typename TType>
        void operator()(parameter_symbol<TType>* sym) {
            if constexpr (get_node_dimension<TType> == 0) {
                if constexpr (is_set_node<TType>) {
                    if constexpr (get_node_dimension<element_type<TType>> == 0) {
                        shape = {};
                        for (const auto& x: sym->m_value) {
                            shape.push_back(0);
                        }
                    } else {
                        shape = {};
                        for (const auto& x: sym->m_value) {
                            auto subshape = x.shape();
                            shape.insert(shape.end(), subshape.begin(), subshape.end());
                        }
                    }
                } else {
                    shape = {};
                }
            } else {
                // convert shape to vector
                auto sym_shape = sym->m_value.shape();
                shape.resize(sym_shape.size());
                std::copy_n(sym_shape.begin(), sym_shape.size(), shape.begin());
            }
        }

        template <typename TType>
        void operator()(variable_symbol<TType>* sym) {
            if constexpr (get_node_dimension<TType> == 0) {
                shape = {};
            } else {
                // convert shape to vector
                auto sym_shape = sym->shape();
                shape.resize(sym_shape.size());
                std::copy_n(sym_shape.begin(), sym_shape.size(), shape.begin());
            }
        }

        std::vector<size_t> shape;
        symbol_table& symbols;
    };

    std::vector<size_t> get_parameter_shape(const std::string& name, symbol_table& symbols) {
        // try to find symbol
        base_symbol* sym = symbols.resolve(name);
        if (sym != nullptr) {
            // get shape of symbol and return it
            get_parameter_shape_visitor visitor(symbols);
            call_visitor(visitor, sym);

            return visitor.shape;
        }
        throw std::invalid_argument("Could not retrieve parameter shape of variable \"" + name + "\" because it does not exist in symbol_table");
    }

    struct get_element_dimension {
        template <typename TType>
        size_t operator()(value_symbol<TType>* node) {
            throw std::invalid_argument("only 0-dimensional sets expected");
        }

        template <typename TType>
        size_t operator()(function_symbol<TType>* node) {
            throw std::invalid_argument("only 0-dimensional sets expected");
        }

        template <typename TType>
        size_t operator()(parameter_symbol<set<TType, 0>>* node) {
            return get_node_dimension<TType>;
        }
    };

    std::vector<std::vector<size_t>> get_set_shape(const std::string& name, symbol_table& symbols) {
        auto dim = call_visitor(get_element_dimension{}, symbols.resolve(name));
        auto flattened_shape = get_parameter_shape(name, symbols);

        if (flattened_shape.size() % dim != 0) {
            throw std::invalid_argument("shape entries not a multiple of entry dimension");
        }

        std::vector<std::vector<size_t>> shape;
        for (int i = 0; i < flattened_shape.size() / dim; i++) {
            for (int j = 0; j < dim; j++) {
                std::vector<size_t> subshape(flattened_shape.begin() + i * dim, flattened_shape.begin() + (i + 1) * dim);
                shape.push_back(subshape);
            }
        }

        return shape;
    }

    class expression_shape_visitor {
    public:
        expression_shape_visitor(symbol_table& symbols): symbols(symbols) {}

        template <typename TType>
        std::vector<size_t> operator()(constant_node<TType>* node) {
            std::vector<size_t> shape;
            
            if constexpr (get_node_dimension<TType> != 0) {
                for (auto k: node->value.shape()) {
                    shape.push_back(k);
                }
            }

            return shape;
        }

        template <typename TType>
        std::vector<size_t> operator()(value_node<TType>* node) {
            if constexpr (get_node_dimension<TType> == 0) {
                return {};
            } else {
                throw std::invalid_argument("any node with non-scalar return type should be overloaded");
            }
        }

        template <typename TType>
        std::vector<size_t> operator()(parameter_node<TType>* node) {
            return get_parameter_shape(node->name, symbols);
        }

        template <unsigned IDim>
        std::vector<size_t> operator()(attribute_node<real<IDim>>* node) {
            variable_symbol<real<IDim>>* sym = cast_variable_symbol<real<IDim>>(symbols.resolve(node->variable_name));
            if (!sym) {
                throw std::invalid_argument("symbol " + node->variable_name + " has unexpected type in attribute call within expression shape visitor");
            }
            return get_parameter_shape(node->variable_name, symbols);
        }

        template <typename TType>
        std::vector<size_t> operator()(entry_node<TType>* node) {
            auto child_shape = call_visitor(*this, node->template get_child<0>());
            return std::vector<size_t>{child_shape.begin() + 1, child_shape.end()};
        }

        template <typename TType>
        std::vector<size_t> operator()(function_node<TType>* node) {
            auto* sym = cast_function_symbol<TType>(symbols.resolve(node->name));
            if (sym == nullptr) {
                throw std::invalid_argument("functionsymbol " + node->name + " is ill-defined");
            }

            std::map<std::string, value_node_variant> arg_map;
            auto args = extract_function_arguments(node);
            for (int i = 0; i < args.size(); ++i) {
                arg_map.emplace(sym->arg_names.at(i), args.at(i));
            }

            auto expr_copy = sym->expr;
            replace_parameters(expr_copy, arg_map);

            return call_visitor(*this, expr_copy);
        }

        template <typename TType>
        std::vector<size_t> operator()(tensor_node<TType>* node) {
            if (node->children.size() == 0) {
                throw std::invalid_argument("tensor_node without children encountered");
            }

            // assume all children have equal shape
            auto child_shape = call_visitor(*this, node->children.front());
            child_shape.insert(child_shape.begin(), node->children.size());
            return child_shape;
        }

        template <typename TType>
        std::vector<size_t> operator()(index_shift_node<TType>* node) {
            auto child_shape = call_visitor(*this, node->template get_child<0>());
            std::rotate(child_shape.begin(), child_shape.begin() + 1, child_shape.end());
            return child_shape;
        }

        template <typename TType>
        std::vector<size_t> operator()(vector_node<TType>* node) {
            throw std::invalid_argument("vector_node should not be encountered");
        }

    private:
        symbol_table& symbols;
    };

    std::vector<size_t> get_expression_shape(value_node_variant expr, symbol_table& symbols) {
        return call_visitor(expression_shape_visitor{symbols}, expr);
    }

    /**
     * Checks if a tree contains any parameter_nodes
     */
    struct is_tree_constant_visitor {
        is_tree_constant_visitor(symbol_table& symbols): symbols(symbols) {}

        template <typename TType>
        void operator()(value_node<TType>* node) {
            traverse_children(*this, node, symbols);
        }

        template <typename TType>
        void operator()(function_node<TType>* node) {
            auto* sym = cast_function_symbol<TType>(symbols.resolve(node->name));
            if (sym == nullptr) {
                throw std::invalid_argument("functionsymbol " + node->name + " is ill-defined");
            }

            std::map<std::string, value_node_variant> arg_map;
            auto args = extract_function_arguments(node);
            for (int i = 0; i < args.size(); ++i) {
                arg_map.emplace(sym->arg_names.at(i), args.at(i));
            }

            auto expr_copy = sym->expr;
            replace_parameters(expr_copy, arg_map);

            return call_visitor(*this, expr_copy);
        }

        template <typename TType>
        void operator()(parameter_node<TType>* node) {
            auto* sym = symbols.resolve(node->name);
            call_visitor(*this, sym);
        }

        template <typename TType>
        void operator()(parameter_symbol<TType>* sym) {
            if (sym->m_is_placeholder) {
                is_constant = false;
            }
        }

        template <typename TType>
        void operator()(variable_symbol<TType>* sym) {
            is_constant = false;
        }

        template <typename TType>
        void operator()(expression_symbol<TType>* sym) {
            call_visitor(*this, sym->m_value);
        }

        template <typename TType>
        void operator()(function_symbol<TType>* sym) {
            throw std::invalid_argument("function_symbol should not be encountered");
        }

        bool is_constant = true;
        symbol_table& symbols;
    };

    bool is_tree_constant(value_node_variant node, symbol_table& symbols) {
        is_tree_constant_visitor visitor(symbols);
        call_visitor(visitor, node);

        return visitor.is_constant;
    }

    /**
     * replaces all constant subtrees with their evaluation
     */
    class replace_constant_subtrees_visitor {
    public:
        replace_constant_subtrees_visitor(symbol_table& symbols, value_node_ptr_variant root): symbols(symbols), current_node(root) {}

        template <typename TType>
        void operator()(value_node<TType>* node) {
            // get optional value of subtree
            auto tree_value = get_subtree_value(node, symbols);

            if (tree_value) {
                // create new constant node
                auto new_const = new constant_node<TType>(*tree_value);

                // replace node and if it cannot be replaced throw an error
                reset_value_node_ptr_variant(current_node, new_const);
            } else {
                // call this visitor on children as they could be constant
                traverse_children(*this, node, {}, current_node);
            }
        }

    private:
        symbol_table& symbols;
        value_node_ptr_variant current_node;
    };

    /**
     * Replaces all constant subtrees in expr
     */
    void replace_constant_subtrees(value_node_ptr_variant expr, symbol_table& symbols) {
        replace_constant_subtrees_visitor visitor(symbols, expr);
        call_visitor(visitor, expr);
    }

    class find_parameter_visitor {
    public:
        find_parameter_visitor(const std::string& parameter_name, value_node_ptr_variant root): parameter_name(parameter_name), current_node(root) {}

        template <typename TType>
        void operator()(value_node<TType>* node) {
            traverse_children(*this, node, {}, current_node);
        }

        template <typename TType>
        void operator()(parameter_node<TType>* node) {
            if (node->name == parameter_name) {
                found_parameters.push_back(current_node);
            }
        }

        std::vector<value_node_ptr_variant> get_found_parameters() {
            return found_parameters;
        }

    private:
        std::string parameter_name;
        std::vector<value_node_ptr_variant> found_parameters{};
        value_node_ptr_variant current_node;
    };

    std::vector<value_node_ptr_variant> find_parameter(const std::string& parameter_name, value_node_ptr_variant expr) {
        find_parameter_visitor visitor(parameter_name, expr);
        call_visitor(visitor, expr);
        return visitor.get_found_parameters();
    }

    void replace_parameters(value_node_ptr_variant node, const std::map<std::string, value_node_variant>& arg_map) {
        for (const auto& [arg_name, arg_value]: arg_map) {
            auto parameters = find_parameter(arg_name, node);
            for (const auto& par: parameters) {
                reset_value_node_ptr_variant(par, clone_value_node_variant(arg_value));
            }
        }
    }
}