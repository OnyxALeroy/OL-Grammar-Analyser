from src.parser import BNFParser
from src.editor import edit_grammar

# -------------------------------------------------------------------------------------------------

# Ask for input file
file_path = input("\033[42m[INPUT]\033[0m\033[32m Enter the path to the file to parse:\033[0m\t")

# Parse the file
parser = BNFParser()
parser.parse_file(file_path)
grammar = parser.grammar
grammar.print()

# Ask if reworking grammar is authorized
print("\033[42m[INPUT]\033[0m\033[32m Your grammar may be edited (to remove unused non-terminals and rules, or remove left recursion).")
can_edit = input("\033[42m[=====]\033[0m\033[32m Do you authorize editing your grammar?(y/n, default y)\033[0m\t")
if can_edit != 'n':
    edit_grammar(grammar)

# Analyse it...