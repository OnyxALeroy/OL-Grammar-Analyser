from typing import List, Dict, Set, Union

class Terminal:
    def __init__(self, symbol: str):
        self.symbol: str = symbol
        pass
    def is_terminal(self) -> bool:
        return True
    def __eq__(self, value: Union["Terminal", "NonTerminal"]) -> bool:
        return self.symbol == value.symbol
    def __ne__(self, value: Union["Terminal", "NonTerminal"]) -> bool:
        return not self.__eq__(value)
    def __hash__(self):
        return hash(self.symbol)

class NonTerminal:
    def __init__(self, symbol: str):
        self.symbol: str = symbol
        pass
    def is_terminal(self) -> bool:
        return False
    def __hash__(self):
        return hash(self.symbol)
    def __eq__(self, value: Union["Terminal", "NonTerminal"]) -> bool:
        return self.symbol == value.symbol
    def __ne__(self, value: Union["Terminal", "NonTerminal"]) -> bool:
        return not self.__eq__(value)

# -------------------------------------------------------------------------------------------------

class Grammar:
    def __init__(self):
        self.axiom: NonTerminal = None
        self.symbols: Set[Terminal | NonTerminal] = set()
        self.terminals: Set[Terminal] = set()
        self.non_terminals: Set[NonTerminal] = set()
        self.rules: Dict[NonTerminal, List[ List[NonTerminal, Terminal] ]] = {}
        pass
    def set_axiom(self, axiom: NonTerminal) -> None:
        self.axiom = axiom
        pass
    def add_rule(self, left_side: NonTerminal, rule: List[NonTerminal | Terminal]) -> None:
        # Setting the axiom
        if self.axiom is None:
            self.axiom = left_side
        
        # Adding the rule
        if not left_side in self.rules.keys():
            self.rules[left_side] = []
        if rule in self.rules[left_side]:
            # If it's already there, show a warning (but proceed without duplicates)
            rule_str = ""
            for rule_element in rule:
                rule_str += rule_element.symbol + " "
            print(f"\033[103m[WARNING]\033[0m\033[93m The rule '{left_side.symbol} -> {rule_str[:-1]}' is duplicated in your grammar! It will be considered once.\033[0m")
        else:
            self.rules[left_side].append(rule)
        self.symbols.add(left_side)
        self.non_terminals.add(left_side)
        self.terminals.discard(left_side)
        for element in rule:
            self.symbols.add(element)
            if element not in self.non_terminals:
                self.terminals.add(element)
        pass

    def print(self) -> None:
        print("\033[104m=========== Grammar ===========\033[0m")
        
        # Axiom
        print(f"\033[94mAxiom: {self.axiom.symbol if self.axiom else 'None'}")

        # Terminals
        print("\nTerminals:")
        if self.terminals:
            print("\t" + ", ".join(sorted([t.symbol for t in self.terminals])))
        else:
            print("\tNone")

        # Non-Terminals
        print("\nNon-Terminals:")
        if self.non_terminals:
            print("\t" + ", ".join(sorted([nt.symbol for nt in self.non_terminals])))
        else:
            print("\tNone")

        # Symbols
        print("\nAll Symbols:")
        if self.symbols:
            print("\t" + ", ".join(sorted([s.symbol for s in self.symbols])))
        else:
            print("\tNone")

        # Rules
        print("\nRules:")
        if self.rules:
            for left, right_list in self.rules.items():
                for right in right_list:
                    right_str = " ".join(sym.symbol for sym in right)
                    print(f"\t{left.symbol} -> {right_str}")
        else:
            print("\tNone")

        print("\033[0m")
        print("\033[104m===============================\033[0m")
        pass

# -------------------------------------------------------------------------------------------------
