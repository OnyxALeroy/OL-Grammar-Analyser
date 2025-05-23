from grammar import*
import re

class GrammarParser:
    def __init__(self):
        self.grammar = Grammar()

    def normalize_symbol(self, symbol):
        if symbol == r'\"':
            return '"'
        elif symbol.startswith('"') and symbol.endswith('"'):
            return symbol[1:-1]
        else:
            return symbol

    def tokenize_rhs(self, rhs) -> List[str]:
        tokens = re.findall(r'\\"|"[^"]*"|[^\s|]+', rhs)
        return [self.normalize_symbol(token) for token in tokens]

    def parse_line(self, line, lineno):
        # Removing comments
        line = line.split('#', 1)[0].strip()
        if not line:
            return

        # Match the pattern: LHS -> RHS
        match = re.match(r'^(".*?"|[^"\s]+)\s*->\s*(.+)$', line)
        if not match:
            raise SyntaxError(f"Syntax error on line {lineno}: {line}")

        # Left part
        lhs = self.normalize_symbol(match.group(1))
        left_side = NonTerminal(lhs)

        rhs = match.group(2)
        alternatives = [alt.strip() for alt in rhs.split('|')]

        for alt in alternatives:
            # We add everything as terminals
            # If they're not, the'll be changed later
            prods: List[Terminal]
            if alt == '€':
                prods = [Terminal('€')]
            else:
                prods = []
                productions = self.tokenize_rhs(alt)
                for p in productions:
                    prods.append(Terminal(p))

            self.grammar.add_rule(left_side, prods)

    def parse_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                self.parse_line(line, lineno)

# --- Main program ---

if __name__ == "__main__":
    path = "../grammars/test_grammar.txt"
    parser = GrammarParser()
    try:
        parser.parse_file(path)
        parser.grammar.print()
    except Exception as e:
        print(f"Error: {e}")
