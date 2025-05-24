import sys
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
if __name__ == "__main__":
    from grammar import Terminal, NonTerminal, Grammar
else:
    from .grammar import Terminal, NonTerminal, Grammar

@dataclass
class ParsedProduction:
    """Represents a parsed production rule"""
    left_side: str
    alternatives: List[str]

class BNFParser:
    def __init__(self):
        self.grammar = Grammar()
        self.symbol_cache: Dict[str, Union[Terminal, NonTerminal]] = {}
        self.auxiliary_counter = 0  # For generating auxiliary non-terminals
        
    def parse_file(self, filename: str) -> Optional[Grammar]:
        """
        Parse a BNF grammar file and return a Grammar instance
        
        Args:
            filename: Path to the BNF grammar file
            
        Returns:
            Grammar instance if parsing successful, None otherwise
        """
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content = file.read()
            return self._parse_content(content)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return None
        except Exception as e:
            print(f"Error reading file: {e}")
            return None
    
    def _parse_content(self, content: str) -> Optional[Grammar]:
        try:
            productions = self._parse_raw_productions(content)
            for production in productions:
                left_nt = self._get_or_create_symbol(production.left_side)
                if not isinstance(left_nt, NonTerminal):
                    raise ValueError(f"Left side must be a non-terminal: {production.left_side}")
                
                for alternative in production.alternatives:
                    processed_rules = self._process_alternative(alternative)
                    for rule in processed_rules:
                        self.grammar.add_rule(left_nt, rule)
            return self.grammar
            
        except Exception as e:
            print(f"Error parsing grammar: {e}")
            return None
    
    def _parse_raw_productions(self, content: str) -> List[ParsedProduction]:
        productions = []
        lines = content.split('\n')
        current_production = ""
        
        for line_num, line in enumerate(lines, 1):
            line = self._remove_comments(line).strip()
            if not line:
                continue
            if '::=' in line:
                if current_production:
                    productions.append(self._parse_single_production(current_production))
                current_production = line
            else:
                current_production += " " + line
        if current_production:
            productions.append(self._parse_single_production(current_production))
        return productions
    
    def _parse_single_production(self, production_line: str) -> ParsedProduction:
        if '::=' not in production_line:
            raise ValueError(f"Invalid production format: {production_line}")
        
        left, right = production_line.split('::=', 1)
        left = left.strip()
        right = right.strip()
        
        if not self._is_non_terminal_string(left):
            raise ValueError(f"Left side must be a non-terminal: {left}")
        alternatives = [alt.strip() for alt in right.split('|')]
        return ParsedProduction(left, alternatives)
    
    def _process_alternative(self, alternative: str) -> List[List[Union[Terminal, NonTerminal]]]:
        tokens = self._tokenize_alternative(alternative)
        return self._process_regex_tokens(tokens)
    
    def _tokenize_alternative(self, alternative: str) -> List[str]:
        tokens = []
        current_token = ""
        in_non_terminal = False
        
        i = 0
        while i < len(alternative):
            char = alternative[i]
            
            if char == '<':
                if current_token.strip():
                    tokens.append(current_token.strip())
                    current_token = ""
                in_non_terminal = True
                current_token += char
            elif char == '>':
                current_token += char
                if in_non_terminal:
                    tokens.append(current_token.strip())
                    current_token = ""
                    in_non_terminal = False
            elif char in ['*', '+'] and not in_non_terminal:
                if current_token.strip():
                    tokens.append(current_token.strip())
                    current_token = ""
                tokens.append(char)
            elif char.isspace() and not in_non_terminal:
                if current_token.strip():
                    tokens.append(current_token.strip())
                    current_token = ""
            else:
                current_token += char
            i += 1
        
        if current_token.strip():
            tokens.append(current_token.strip())
        
        return tokens
    
    def _process_regex_tokens(self, tokens: List[str]) -> List[List[Union[Terminal, NonTerminal]]]:
        if not tokens: return [[]]

        processed_tokens = []
        i = 0
        
        while i < len(tokens):
            token = tokens[i]
            if i + 1 < len(tokens) and tokens[i + 1] in ['*', '+']:
                operator = tokens[i + 1]
                if operator == '*':
                    # X* becomes: create auxiliary non-terminal A where A -> X A | ε
                    aux_rules = self._create_star_rules(token)
                    processed_tokens.extend(aux_rules)
                elif operator == '+':
                    # X+ becomes: create auxiliary non-terminal A where A -> X | X A
                    aux_rules = self._create_plus_rules(token)
                    processed_tokens.extend(aux_rules)
                
                i += 2  # Skip the operator
            else:
                symbol = self._get_or_create_symbol(token)
                processed_tokens.append(symbol)
                i += 1
        
        return [processed_tokens] if processed_tokens else [[]]
    
    def _create_star_rules(self, symbol_str: str) -> List[Union[Terminal, NonTerminal]]:
        aux_name = f"<{symbol_str.strip('<>')}_star_{self.auxiliary_counter}>"
        self.auxiliary_counter += 1
        aux_nt = self._get_or_create_symbol(aux_name)
        original_symbol = self._get_or_create_symbol(symbol_str)

        # Add rules: A -> X A | ε (empty rule)
        self.grammar.add_rule(aux_nt, [original_symbol, aux_nt])  # X A
        self.grammar.add_rule(aux_nt, [])  # ε (empty)
        
        return [aux_nt]
    
    def _create_plus_rules(self, symbol_str: str) -> List[Union[Terminal, NonTerminal]]:
        aux_name = f"<{symbol_str.strip('<>')}_plus_{self.auxiliary_counter}>"
        self.auxiliary_counter += 1
        aux_nt = self._get_or_create_symbol(aux_name)
        original_symbol = self._get_or_create_symbol(symbol_str)
        
        # Add rules: A -> X | X A
        self.grammar.add_rule(aux_nt, [original_symbol])  # X
        self.grammar.add_rule(aux_nt, [original_symbol, aux_nt])  # X A
        
        return [aux_nt]
    
    def _get_or_create_symbol(self, symbol_str: str) -> Union[Terminal, NonTerminal]:
        if symbol_str in self.symbol_cache:
            return self.symbol_cache[symbol_str]
        
        if self._is_non_terminal_string(symbol_str):
            symbol = NonTerminal(symbol_str)
        else:
            symbol = Terminal(symbol_str)
        
        self.symbol_cache[symbol_str] = symbol
        return symbol
    
    def _is_non_terminal_string(self, symbol: str) -> bool:
        return symbol.startswith('<') and symbol.endswith('>')
    
    def _remove_comments(self, line: str) -> str:
        comment_pos = len(line)
        for marker in ['//', '#']:
            pos = line.find(marker)
            if pos != -1:
                comment_pos = min(comment_pos, pos)
        return line[:comment_pos]

def create_sample_grammar_file():
    """Create a sample BNF file demonstrating regex operators"""
    sample_content = """// Sample BNF Grammar with Regex Operators
        // Arithmetic expressions with lists

        <expression> ::= <term> | <expression> + <term> | <expression> - <term>
        <term> ::= <factor> | <term> * <factor> | <term> / <factor>
        <factor> ::= <number> | ( <expression> ) | <variable>

        // Numbers with optional sign and multiple digits
        <number> ::= <sign>? <digit>+
        <sign> ::= + | -
        <digit> ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

        // Variables and identifiers
        <variable> ::= <letter> <alphanumeric>*
        <letter> ::= a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z
        <alphanumeric> ::= <letter> | <digit>

        // Statement lists
        <statement_list> ::= <statement> | <statement_list> ; <statement>
        <statement> ::= <assignment> | <expression>
        <assignment> ::= <variable> = <expression>
        """
    
    with open('sample_grammar.txt', 'w') as f:
        f.write(sample_content)
    print("Created sample_grammar.txt with regex operators")


def main():
    """Main function"""
    if len(sys.argv) == 1:
        print("Usage: python enhanced_bnf_parser.py <grammar_file.txt>")
        print("       python enhanced_bnf_parser.py --create-sample")
        print("\nSupported regex operators:")
        print("  X*  - Zero or more occurrences of X")
        print("  X+  - One or more occurrences of X")
        print("\nExample enhanced BNF:")
        print("  <number> ::= <digit>+")
        print("  <identifier> ::= <letter> <alphanumeric>*")
        print("  <optional_sign> ::= <sign>?")
        return 1

    if sys.argv[1] == '--create-sample':
        create_sample_grammar_file()
        return 0
    
    filename = sys.argv[1]
    parser = BNFParser()
    
    print(f"Parsing enhanced BNF grammar from: {filename}")
    print("=" * 60)
    
    grammar = parser.parse_file(filename)
    
    if grammar:
        print("✓ Grammar parsed successfully!")
        print()
        parser.print_grammar_info()
        return 0
    else:
        print("✗ Failed to parse grammar file.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
