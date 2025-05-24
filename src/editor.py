from .grammar import*

# -------------------------------------------------------------------------------------------------

def inf_reduce_grammar(g: Grammar) -> Grammar:
    non_terminals = g.non_terminals.copy()
    terminals = g.terminals # No need for copy, these won't be edited

    # Determine E, the limit of the E_i
    E_i = None
    E_j = set() # E_0
    while (E_i != E_j):
        E_i = E_j
        for non_terminal in non_terminals:
            rules = g.rules[non_terminal]
            for rule in rules:
                product = ""
                for element in rule:
                    product += element.symbol
                print(product)

            if True:
                E_j.add(non_terminal)

    result = Grammar()
    result.duplicate(g)
    return result

# -------------------------------------------------------------------------------------------------

def edit_grammar(original_grammar: Grammar) -> Grammar:
    # Reducing the grammar (inferior then superior)
    ir_grammar = inf_reduce_grammar(original_grammar)
    return ir_grammar

# -------------------------------------------------------------------------------------------------