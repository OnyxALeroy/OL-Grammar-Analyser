#ifndef GRAMMAR_HPP
#define GRAMMAR_HPP

#define DEFAULT_AXIOM -1

#include <algorithm>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

// FIXME: remove this
#include <iostream>

class Grammar {
   public:
    std::string getAxiomName() const;
    std::unordered_map<int, std::string> getAllNonTerminals() const {
        return m_nonTerminals;
    }
    std::unordered_map<int, std::string> getAllTerminals() const {
        return m_terminals;
    }
    int getAxiom() const { return m_axiom; }
    void setAxiom(int axiom) { m_axiom = axiom; }
    std::unordered_map<int, std::vector<std::vector<int>>> getRules() const {
        return m_rules;
    }

    std::optional<int> getNonTerminal(std::string) const;
    std::optional<int> getTerminal(std::string) const;
    std::optional<std::vector<std::vector<int>>> getProductionFromNonTerminal(
        std::string name) const;

    // Parsing
    void addProduction(std::string left, std::string right);

   private:
    // NOTE: terminals are positively indexed, while non-terminals are
    // negatively indexed (0 not being any of them)
    std::unordered_map<int, std::string> m_nonTerminals = {};
    std::unordered_map<int, std::string> m_terminals = {};
    int m_axiom = DEFAULT_AXIOM;

    std::unordered_map<int, std::vector<std::vector<int>>> m_rules = {};

    void addTokenToProduction(std::string token, std::vector<int> production);
};

#endif