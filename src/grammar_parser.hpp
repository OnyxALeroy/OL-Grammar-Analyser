#ifndef GRAMMAR_PARSER_HPP
#define GRAMMAR_PARSER_HPP

#include <tuple>

#include "grammar.hpp"

Grammar parseGrammar(const std::string& input, const std::string& delimiter);

#endif