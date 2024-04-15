from lexer import Lexer

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
    





















class SyntaxAnalyzer:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.errors = []

    def consume_token(self):
        self.current_token = self.lexer.tokenize()[0]  # Obtener el primer token después de tokenizar

    def match(self, token_type):
        if self.current_token.type == token_type:
            self.consume_token()
        else:
            self.report_error(self.current_token.value, [token_type])

    def report_error(self, found, expected):
        expected_str = ', '.join([f'"{symbol}"' for symbol in sorted(expected)])
        error_message = f"<{self.current_token.row}:{self.current_token.column}> Error sintactico: se encontro: {found}; se esperaba: {expected_str}"
        self.errors.append(error_message)

    def parse_program(self):
        self.consume_token()  # Obtener el primer token
        print(self.current_token.type)
        self.parse_statement()
        if not self.errors:
            print("El análisis sintáctico ha finalizado exitosamente.")
        else:
            print(self.errors[0])  # Reportar solo el primer error

    def programa(self):
        if(self.current_token.value == 'escribir'):
            sentencia()
            self.match(???)



source_code = """patata = 10
para (id en rango(10))
  bloque
fin"""

# Crear instancia del analizador léxico
lexer = Lexer(source_code)

grammar = {
    '<programa>': [('<sentencia>',)],
    '<sentencia>': [('<llamada_funcion>',)],
    '<llamada_funcion>': [('escribir', '(', '<cadena>', ')') ],
    '<cadena>': [('tkn_str',)]
}

# Crear instancia del analizador de gramática
analyzer = GrammarAnalyzer(grammar)

# Calcular conjuntos de primeros, siguientes y predicción
analyzer.calculate_first_sets()
analyzer.calculate_follow_sets()
analyzer.calculate_prediction_sets()

for i in analyzer.prediction_sets:
    print(i) ## Non terminal
    for j in analyzer.prediction_sets[i]:
        ## j is the production of the non terminal and analyzer.prediction_sets[i][j] is the prediction set
        print(j,analyzer.prediction_sets[i][j])

# # Crear instancia del analizador sintáctico y conectar con el léxico
# syntax_analyzer = SyntaxAnalyzer(lexer)

# # Analizar el programa
# syntax_analyzer.parse_program()
