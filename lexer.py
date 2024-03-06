import re


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []

        # Define token dictionary
        self.token_definitions = {
            r'\d+': 'NUMERO',
            r'[a-zA-Z_]\w*': 'IDENTIFICADOR',
            r'\+': 'SUMA',
            r'-': 'RESTA',
            r'=': 'IGUAL'
        }

    def advance(self, steps=1):
        self.position += steps

    def tokenize(self):
        while self.position < len(self.code):
            current_char = self.code[self.position]

            # Ignore whitespace
            if current_char.isspace():
                self.advance()
                continue

            # Check for matches with regular expressions
            for pattern, token_type in self.token_definitions.items():
                match = re.match(pattern, self.code[self.position:])
                if match:
                    value = match.group(0)
                    self.add_token(token_type, value)
                    self.advance(len(value))
                    break
            else:
                print(f"Carácter no reconocido: {current_char}")
                self.advance()

        return self.tokens

    def add_token(self, type, value):
        self.tokens.append(Token(type, value))


# Example usage
source_code = """
variable = 5 + 3
resultado = variable - 2
"""
lexer = Lexer(source_code)
tokens = lexer.tokenize()

for token in tokens:
    print(f'Tipo: {token.type}, Valor: {token.value}')
