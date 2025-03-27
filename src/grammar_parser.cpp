#include "grammar_parser.hpp"

std::tuple<std::string, std::string> split(std::string_view input,
                                           const std::string& delimiter) {
    size_t pos =
        input.find(delimiter);  // Search for the delimiter (multi-character)
    if (pos == std::string::npos) {
        // If the delimiter is not found, return the input and an empty string
        return {std::string(input), ""};
    }

    return {std::string(input.substr(0, pos)),
            std::string(input.substr(pos + delimiter.length()))};
}

Grammar parseGrammar(const std::string& input, const std::string& delimiter) {
    Grammar grammar;

    // Split the input into separate lines
    std::vector<std::string_view> lines;
    auto start = input.begin();
    for (auto it = input.begin(); it != input.end(); ++it) {
        if (*it == '\n' ||
            (*it == '\r' && (it + 1) != input.end() && *(it + 1) == '\n')) {
            if (*it == '\r') ++it;
            lines.push_back(
                std::string_view(&*start, std::distance(start, it)));
            start = it + 1;
        }
    }
    if (start != input.end()) {
        lines.push_back(
            std::string_view(&*start, std::distance(start, input.end())));
    }

    // Parse each line
    for (const auto& line : lines) {
        std::tuple<std::string, std::string> parsed_line =
            split(line, delimiter);
        std::string leftside = std::get<0>(parsed_line);
        leftside.erase(std::remove(leftside.begin(), leftside.end(), ' '),
                       leftside.end());
        std::string rightside = std::get<1>(parsed_line);
        grammar.addProduction(leftside, rightside);

        std::cout << "Parsed: " << leftside << " -> " << rightside << std::endl;
    }

    return grammar;
}
