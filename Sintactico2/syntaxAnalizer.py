from lexer import Lexer
from collections import deque


class SyntaxAnalyzer:
    def __init__(self, lexer, root, grammar):
        self.lexer = lexer
        self.predictionSet = set()
        self.derivationStack = deque(root[0])
        self.match = False
        self.grammar = grammar

    def parse_program(self):
        tokens = self.get_tokens()
        error = False

        for token in tokens:
            while not self.match:
                current_element = self.derivationStack.pop()
                
                if current_element[0].isupper():
                    rule = self.lookForMatch(current_element, token)
                    if rule == 'error':
                        error = True
                        self.report_error(token)
                    else:
                        for i in reversed(rule):
                            if i != 'empty':
                                self.derivationStack.append(i)
                else:
                    self.predictionSet.add(current_element)
                    if current_element == token.value or current_element == token.type:
                        self.match = True
                        self.predictionSet.clear()
                    else:
                        error = True
                        self.report_error(token)
            self.match = False  # Reset match for the next token
            if error:
                break
        if not error:
            print('El analisis sintactico ha finalizado exitosamente.')

    def lookForMatch(self, current_element, token):
        match = 'error'
        for rule in self.grammar[current_element]:
            for i in rule:
                if i[0].isupper():
                    if i == current_element:
                        continue
                    possible = self.lookForMatch(i, token)
                    if possible != 'error':
                        match = rule
                        return match
                elif i == 'empty':
                    return rule
                elif i == token.value or i == token.type :
                    return rule
                else:
                    self.predictionSet.add(i)
        return match


    def get_tokens(self):
        self.lexer.tokenize()
        return self.lexer.tokens

    def report_error(self, token ):
        
        founded = f"\"{token.value}\"" if token.type == 'tkn_str' else token.value

        
        sorted_prediction_set = sorted(self.predictionSet)

       
        expected = ', '.join(f'"{item if item != "tkn_str" else "cadena_de_caracteres"}"' for item in sorted_prediction_set)

        error_message = f"<{token.row}:{token.column}> Error sintactico: se encontro: {founded}; se esperaba: {expected}"
        print(error_message)


source_code = """pan_danes pan_danes"""

lexer = Lexer(source_code)

grammar = {
    'PROGRAMA': [['SENTENCIA']],
    'SENTENCIA': [['LLAMADA_FUNCION']],
    'LLAMADA_FUNCION': [['escribir', '(', 'CADENA', ')']],
    'CADENA': [['tkn_str',]]
}

grammarTest = {
    "S": [["D", "A", "EOF"],],
    "D": [["pan_danes", "C", "pan_danes"], ["empty"],],
    "A": [["pan_ajo", "C", "pan_ajo"],],
    "C": [["lechuga", "C"], ["tomate", "C"], ["cebolla", "C"], ["jamon", "C"],["empty"]],
}

syntax_analyzer = SyntaxAnalyzer(lexer, "S", grammarTest)

syntax_analyzer.parse_program()
