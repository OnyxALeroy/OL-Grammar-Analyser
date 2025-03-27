#include "grammar_parser.hpp"

std::string openFile(const std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        throw std::runtime_error("Failed to open file: " + filename);
    }
    std::stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

int main() {
    // Prompt the user for the filename
    std::string filename;
    std::cout << "Please enter the filename to parse (in the 'input' folder): ";
    std::cin >> filename;
    std::string input = "./input/" + filename;
    // Check if the file exists
    if (!std::filesystem::exists(input)) {
        std::cerr << "Error: File \"" << input << "\" does not exist!"
                  << std::endl;
        return 1;
    }

    // Prompt the user for the delimiter
    std::string delimiter;
    std::cout << "Please enter the delimiter you used (default: '->'): ";
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::getline(std::cin, delimiter);
    delimiter.erase(std::remove(delimiter.begin(), delimiter.end(), ' '),
                    delimiter.end());
    if (delimiter.empty()) {
        delimiter = "->";
    }

    std::string content = openFile(input);
    std::cout << "Input file is: \"" << input << "\"" << std::endl;
    std::cout << "Delimiter used: \"" << delimiter << "\"" << std::endl;
    std::cout << "Content of the file:\n" << content << std::endl;

    std::cout << "\nParsing grammar..." << std::endl;
    Grammar grammar = parseGrammar(content, delimiter);
    std::cout << "Parsing completed successfully!\n" << std::endl;

    // Print the parsed grammar
    std::cout << "Grammar Details" << std::endl;
    std::cout << "\tAxiom: \"" << grammar.getAxiomName() << "\"" << std::endl;
    std::cout << "\tNon-Terminals:" << std::endl;
    for (const auto& [id, name] : grammar.getAllNonTerminals()) {
        std::cout << "\t\tID: " << id << ", Name: \"" << name << "\""
                  << std::endl;
    }
    std::cout << "\tTerminals:" << std::endl;
    for (const auto& [id, name] : grammar.getAllTerminals()) {
        std::cout << "\t\tID: " << id << ", Name: \"" << name << "\""
                  << std::endl;
    }

    return 0;
}
