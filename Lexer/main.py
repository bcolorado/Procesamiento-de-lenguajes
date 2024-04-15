from lexer import Lexer

source_code = """para i en rango(10)
  poner(i .. '\n')
fin"""

lexer = Lexer(source_code)
tokens = lexer.tokenize()
lexer.printTokens()
