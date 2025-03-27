#include "grammar.hpp"

std::optional<int> Grammar::getNonTerminal(std::string name) const {
    for (const auto &pair : this->m_nonTerminals) {
        if (pair.second == name) {
            return pair.first;
        }
    }
    return std::nullopt;
}

std::optional<int> Grammar::getTerminal(std::string name) const {
    for (const auto &pair : this->m_terminals) {
        if (pair.second == name) {
            return pair.first;
        }
    }
    return std::nullopt;
}

std::optional<std::vector<std::vector<int>>>
Grammar::getProductionFromNonTerminal(std::string name) const {
    auto nonTerminal = getNonTerminal(name);
    if (nonTerminal.has_value()) {
        for (const auto &pair : this->m_rules) {
            if (pair.first == nonTerminal) {
                return pair.second;
            }
        }
    }
    return std::nullopt;
}

// ------------------------------------------------------------------------------------------------

void Grammar::addTokenToProduction(std::string token,
                                   std::vector<int> production) {
    // Empty productions are ignored
    if (!token.empty()) {
        // NOTE: by default, a token will be added as a Terminal
        auto terminal = getNonTerminal(token);
        if (terminal.has_value()) {
            production.push_back(*terminal);
        } else {
            auto nonTerminal = getTerminal(token);
            if (!nonTerminal.has_value()) {
                int id = this->m_terminals.size() + 1;
                this->m_terminals[id] = token;
                nonTerminal = id;
            }
            production.push_back(*nonTerminal);
        }
    }
}

void Grammar::addProduction(std::string left, std::string right) {
    auto nonTerminal = getNonTerminal(left);
    int leftside;
    if (!nonTerminal.has_value()) {
        // Maybe the Non-Terminal was previously added as a Terminal
        auto terminal = getTerminal(left);
        if (terminal.has_value()) {
            // If so, we need to remove it from Terminals
            this->m_terminals.erase(*terminal);
        }

        // Adding the leftside to the Non-Terminals
        int id = -this->m_nonTerminals.size() - 1;
        this->m_nonTerminals[id] = left;
        leftside = id;
    } else {
        leftside = *nonTerminal;
    }

    // Parsing
    std::vector<std::vector<int>> allProductions;
    std::vector<int> currentProduction;
    std::string token = "";
    for (char c : right) {
        if (c == ' ') {
            // Adding the token to the current production
            addTokenToProduction(token, currentProduction);
            token = "";
        } else if (c == '|') {
            // Adding the token to the current production, then adding it to the
            // "all productions" vector
            addTokenToProduction(token, currentProduction);
            allProductions.push_back(currentProduction);
            currentProduction.clear();
            token = "";
        } else {
            token += c;
        }
    }

    // Adding the last token to the current production
    addTokenToProduction(token, currentProduction);
    allProductions.push_back(currentProduction);

    // Adding the production to the Rules
    this->m_rules[leftside] = allProductions;
}