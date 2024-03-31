import re

class Token:
    def __init__(self, type, value, row, column):
        self.type = type
        self.value = value
        self.row = row
        self.column = column


class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.row = 1
        self.column = 1
        self.tokens = []

        self.keywords_singletkns = {
            # Keywords
            r'\bcaso\b': 'caso',
            r'\bcierto\b': 'cierto',
            r'\bverdadero\b': 'verdadero',
            r'\bdefecto\b': 'defecto',
            r'\botro\b': 'otro',
            r'\bdesde\b': 'desde',
            r'\belegir\b': 'elegir',
            r'\berror\b': 'error',
            r'\bescribir\b': 'escribir',
            r'\bimprimir\b': 'imprimir',
            r'\bponer\b': 'poner',
            r'\bfalso\b': 'falso',
            r'\bfin\b': 'fin',
            r'\bfuncion\b': 'funcion',
            r'\bfun\b': 'fun',
            r'\bhasta\b': 'hasta',
            r'\bimprimirf\b': 'imprimirf',
            r'\bmientras\b': 'mientras',
            r'\bnulo\b': 'nulo',
            r'\bosi\b': 'osi',
            r'\brepetir\b': 'repetir',
            r'\bretorno\b': 'retorno',
            r'\bretornar\b': 'retornar',
            r'\bret\b': 'ret',
            r'\bromper\b': 'romper',
            r'\bsi\b': 'si',
            r'\bsino\b': 'sino',
            r'\btipo\b': 'tipo',
            r'\brango\b': 'rango',
            r'\ben\b': 'en',
            r'\bpara\b': 'para',
            r'\bleer\b': 'leer',
            # built-int
            r'\bacadena\b': 'acadena',
            r'\balogico\b': 'alogico',
            r'\banumero\b': 'anumero',
            r'\bimprimir\b': 'imprimir',
            r'\bescribir\b': 'escribir',
            r'\bponer\b': 'poner',
            r'\bimprimirf\b': 'imprimirf',
            r'\bincluir\b': 'incluir',
            r'\bleer\b': 'leer',
            r'\blimpiar\b': 'limpiar',
            r'\btipo\b': 'tipo',
            # Logical
            r'!=': 'tkn_neq',
            r'~=': 'tkn_regex',
            r'\+\+': 'tkn_increment',
            r'--': 'tkn_decrement',
            r'<=': 'tkn_leq',
            r'>=': 'tkn_geq',
            r'==': 'tkn_equal',
            r'&&': 'tkn_and',
            r'\|\|': 'tkn_or',
            r'\.\.': 'tkn_concat',
            r'%=': 'tkn_mod_assign',
            r'/=': 'tkn_div_assign',
            r'\*=': 'tkn_times_assign',
            r'-=': 'tkn_minus_assign',
            r'\+=': 'tkn_plus_assign',
            r'\+': 'tkn_plus',
            r'-': 'tkn_minus',
            r'=': 'tkn_assign',
            r'<': 'tkn_less',
            r'>': 'tkn_greater',
            r'\*': 'tkn_times',
            r'/': 'tkn_div',
            r'\^': 'tkn_power',
            r'%': 'tkn_mod',
            r'!': 'tkn_not',
            # Other
            r'\.': 'tkn_period',
            r',': 'tkn_comma',
            r'\(': 'tkn_opening_par',
            r'\)': 'tkn_closing_par',
            r';': 'tkn_semicolon',
            r':': 'tkn_colon',
            r'{': 'tkn_opening_key',
            r'}': 'tkn_closing_key',
            r'\[': 'tkn_opening_bra',
            r'\]': 'tkn_closing_bra',

        }

        self.other_tkns = {
            # General
            r'[a-zA-Z_]\w*': 'id',
            r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'': 'tkn_str',
            r'\d+(\.\d+)?': 'tkn_real',

        }

        # Define token dictionary
        self.token_definitions = {
            **self.keywords_singletkns, **self.other_tkns, }
        

    def printTokens(self):
        if self.tokens:
            for token in self.tokens:
                if token.type in self.keywords_singletkns.values():
                    print(f'<{token.type},{token.row},{token.column}>')
                else:
                    print(f'<{token.type},{token.value},{token.row},{token.column}>')

    def advance(self, steps=1):
        for i in range(steps):
            if self.code[self.position] == '\n':
                self.row += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1

    def tokenize(self):
        while self.position < len(self.code):
            current_char = self.code[self.position]

            # Ignore whitespace
            if current_char.isspace():
                self.advance()
                continue

            # Check for single-line comments
            if current_char == '#' or (current_char == '/' and self.code[self.position + 1] == '/'):
                self.skip_comment()
                continue

            # Check for multi-line comments
            if current_char == '/' and self.code[self.position + 1] == '*':
                open_multiComment_row = self.row
                open_multiComment_col = self.column
                if not self.skip_multi_line_comment():
                    self.printTokens()
                    print(
                        f">>> Error lexico (linea: {open_multiComment_row}, posicion: {open_multiComment_col})")
                    return
                continue

            token_row = self.row
            token_column = self.column

            # Check for matches with regular expressions
            match_found = False
            for pattern, token_type in self.token_definitions.items():
                match = re.match(pattern, self.code[self.position:])
                if match:
                    value = match.group(0)
                    if token_type == 'tkn_str':
                        newValue = value.replace('\n', '\\n')
                        newValue = value[1:-1]
                        self.add_token(token_type, newValue,
                                       token_row, token_column)
                    else:
                        self.add_token(token_type, value,
                                       token_row, token_column)
                    self.advance(len(value))
                    match_found = True
                    break

            if not match_found:
                self.printTokens()
                print(
                    f">>> Error lexico (linea: {self.row}, posicion: {self.column})")
                return

        return self.tokens

    def add_token(self, type, value, row, column):
        self.tokens.append(Token(type, value, row, column))

    def skip_comment(self):
        while self.position < len(self.code) and self.code[self.position] != '\n':
            self.advance()

    def skip_multi_line_comment(self):
        while self.position < len(self.code) - 1 and not (self.code[self.position] == '*' and self.code[self.position + 1] == '/'):
            self.advance() if self.code[self.position] == '\n' else self.advance()
        if self.position >= len(self.code) - 1:
            return False  # Comment is not closed
        self.advance(2)  # Skip the closing '*/' characters
        return True

    def get_keywords_singletkns(self):
        return self.keywords_singletkns