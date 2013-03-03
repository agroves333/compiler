'''
Created on Mar 1, 2013

@author: adam
'''

class SymbolTableEntry(object):
    
    lexeme = ''
    type = ''
    
    def __init__(self, lexeme, vType):
        self.lexeme = lexeme
        self.type = vType