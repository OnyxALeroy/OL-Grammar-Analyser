#ifndef GRAMMAR_HPP
#define GRAMMAR_HPP

#include <optional>
#include <string>
#include <unordered_map>
#include <vector>

class Grammar {
   public:
    std::unordered_map<int, std::string> getAllNonTerminals() const {
        return m_nonTerminals;
    }
    std::unordered_map<int, std::string> getAllTerminals() const {
        return m_terminals;
    }
    int getAxiom() const { return m_axiom; }
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
    std::unordered_map<int, std::string> m_nonTerminals;
    std::unordered_map<int, std::string> m_terminals;
    int m_axiom;

    std::unordered_map<int, std::vector<std::vector<int>>> m_rules;

    void addTokenToProduction(std::string token, std::vector<int> production);
};

#endif