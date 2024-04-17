class GrammarAnalyzer:
    def __init__(self, grammar):
        self.grammar = grammar
        self.first_sets = {}
        self.follow_sets = {}
        self.prediction_sets = {}

    def calculate_first_sets(self):
        for non_terminal in self.grammar:
            self.first_sets[non_terminal] = self.calculate_first(non_terminal)

    def calculate_first(self, symbol):
        first_set = set()
        productions = self.grammar[symbol]
        for production in productions:
            first_symbol = production[0]
            if first_symbol not in self.grammar:
                first_set.add(first_symbol)
            elif first_symbol != symbol:
                first_set.update(self.calculate_first(first_symbol))
        return first_set

    def calculate_follow_sets(self):
        for non_terminal in self.grammar:
            self.follow_sets[non_terminal] = set()

        start_symbol = list(self.grammar.keys())[0]
        self.follow_sets[start_symbol].add('$')

        for non_terminal in self.grammar:
            self.calculate_follow(non_terminal)

    def calculate_follow(self, symbol):
        for non_terminal in self.grammar:
            productions = self.grammar[non_terminal]
            for production in productions:
                if symbol in production:
                    index = production.index(symbol)
                    if index < len(production) - 1:
                        next_symbol = production[index + 1]
                        if next_symbol in self.grammar:
                            follow_set = self.first_sets[next_symbol]
                            self.follow_sets[symbol].update(follow_set)
                    else:
                        if non_terminal != symbol:
                            follow_set = self.follow_sets[non_terminal]
                            self.follow_sets[symbol].update(follow_set)

    def calculate_prediction_sets(self):
        for non_terminal in self.grammar:
            self.prediction_sets[non_terminal] = {}
            productions = self.grammar[non_terminal]
            for production in productions:
                first_set = self.calculate_first_of_production(production)
                if 'epsilon' in first_set:
                    follow_set = self.follow_sets[non_terminal]
                    first_set.remove('epsilon')
                    first_set.update(follow_set)
                self.prediction_sets[non_terminal][production] = first_set

    def calculate_first_of_production(self, production):
        first_set = set()
        for symbol in production:
            if symbol in self.grammar:
                first_set.update(self.first_sets[symbol])
                if 'epsilon' not in self.first_sets[symbol]:
                    break
            else:
                first_set.add(symbol)
                break
        return first_set

    def is_ll1_grammar(self):
        for non_terminal in self.grammar:
            productions = self.grammar[non_terminal]
            prediction_sets = self.prediction_sets[non_terminal]
            for production in productions:
                for other_production in productions:
                    if production != other_production:
                        intersection = prediction_sets[production].intersection(prediction_sets[other_production])
                        if intersection:
                            return False
        return True

# Definir la gramática
grammar = {
    '<programa>': [('<sentencia>',)],
    '<sentencia>': [('<llamada_funcion>',)],
    '<llamada_funcion>': [('escribir', '(', '<cadena>', ')') ],
    '<cadena>': [('tkn_str',)]
}

test = {
    '<A>': [('a', 'b', '<B>'), ('<B>','b')],
    '<B>': [('b',), ('c',)]
}



# Crear instancia del analizador de gramática
analyzer = GrammarAnalyzer(grammar)

# Calcular conjuntos de primeros, siguientes y predicción
analyzer.calculate_first_sets()
analyzer.calculate_follow_sets()
analyzer.calculate_prediction_sets()

print("PRIMEROS: ",analyzer.first_sets)
print("SIGUIENTES: ",analyzer.follow_sets)
print("PREDICCION: ",analyzer.prediction_sets)

# Verificar si la gramática es LL(1)
is_ll1 = analyzer.is_ll1_grammar()
print("La gramática es LL(1):", is_ll1)
