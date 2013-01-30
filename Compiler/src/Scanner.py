'''
Created on Jan 24, 2013

@author: david
'''

import sys
#from fysom import Fysom

class Scanner(object):

    # Initialize vars
    lexeme = ""
    token = ""
    line = 1
    col = 0 # hasn't read in a char yet
    file = None
    reserved = None

    # Constuctor
    def __init__(self):
        self._hashReserved()
    
    # Open the input file
    def openFile(self, fileName):
        try:
            self.file = open(fileName, 'r')
        except IOError:
            sys.exit("Source file not found")
    
    # Close the input file        
    def closeFile(self):
        self.file.close()
    
    # Check for more data in file    
    def hasNext(self):
        if (self.token == "MP_EOF"):
            return False
        else:
            return True
    
    def getNextToken(self):
        self.token = ""
        self.lexeme = ""
        nextChar = ""

        if not self.file.read(1):
            self.token = "MP_EOF"
        else:
            self.file.seek(-1, 1) 
        
            self._discard_whitespace()
      
            nextChar = self.file.read(1)
            self.file.seek(-1, 1)
         
            #BEGINNING OF DISPATCHER
            if(nextChar == "."): self._scanPeriod()
        
            elif(nextChar == ","): self._scanComma()
        
            elif(nextChar == ";"): self._scanSemicolon()
        
            elif(nextChar == "("): self._scanLeftParen()

            elif(nextChar == ")"): self._scanRightParen()

            elif(nextChar == "="): self._scanEqual()
        
            elif(nextChar == "+"): self._scanPlus()
        
            elif(nextChar == "-"): self._scanMinus()
        
            elif(nextChar == "*"): self._scanTimes()

            elif(nextChar == ":"): self._scanColonOrAssignOp()

            elif(nextChar in map(chr, range(65, 91)) + map(chr, range(97, 123)) or
                 (nextChar == "_")): self._scanId()

            #elif(nextChar in map(chr, range(48, 58))): self._scanNumericLit()

            else:
                self.token = "Not Done"
                self.col += 1
                self.lexeme= nextChar
                self.file.read(1)
        
        return self.token

    def _discard_whitespace(self):

        nextChar = self.file.read(1)

        while(nextChar == ' ' or nextChar == '\n'):
            if(nextChar == " "):
                self.col += 1

            elif(nextChar == "\n"):
                self.line += 1
                self.col = 0
            nextChar = self.file.read(1)

        #rewind file pointer
        self.file.seek(-1, 1)

    def getLexeme(self): 
        return self.lexeme

     
    def getLineNumber(self): 
        return self.line

     
    def getColumnNumber(self): 
        return self.col

         
    #Private functions
    def _scanPeriod(self):
        self.token = "MP_PERIOD" 
        self.lexeme = "."
        self.col += 1
        self.file.read(1)
        
    def _scanComma(self):
        self.token = "MP_COMMA" 
        self.lexeme = ","
        self.col += 1
        self.file.read(1)
 
    def _scanSemicolon(self):
        self.token = "MP_SCOLON" 
        self.lexeme = ";"
        self.col += 1
        self.file.read(1)
            
    def _scanLeftParen(self):
        self.token = "MP_LPAREN" 
        self.lexeme = "("
        self.col += 1
        self.file.read(1)
     
    def _scanRightParen(self):
        self.token = "MP_RPAREN" 
        self.lexeme = ")"
        self.col += 1
        self.file.read(1)
            
    def _scanEqual(self):
        self.token = "MP_EQUAL" 
        self.lexeme = "="
        self.col += 1
        self.file.read(1)

    def _scanPlus(self):
        self.token = "MP_PLUS" 
        self.lexeme = "+"
        self.col += 1
        self.file.read(1)
    
    def _scanMinus(self):
        self.token = "MP_MINUS" 
        self.lexeme = "-"
        self.col += 1
        self.file.read(1)
        
    def _scanTimes(self):
        self.token = "MP_TIMES" 
        self.lexeme = "*"
        self.col += 1
        self.file.read(1)
        
            
    def _scanColonOrAssignOp(self):
        state = 0
        done = False
        self.lexeme = ""

        while not done:
            if (state == 0):
                nextChar = self.file.read(1)
                if(nextChar == ":"):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
            elif (state == 1):
                nextChar = self.file.read(1)
                if(nextChar == "="):
                    state = 2
                    self.lexeme = self.lexeme + nextChar
                else:
                    self.token = 'MP_COLON'
                    self.col += 1
                    done = True
                    self.file.seek(-1, 1)
            elif (state == 2):
                self.token = 'MP_ASSIGN'
                self.col += 1
                done = True

  
    def _scanId(self): 
        state = 0
        done = False
        
        while not done:
            if (state == 0):
                nextChar = self.file.read(1)
                if(nextChar in map(chr, range(65, 91)) + map(chr, range(97, 123))):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                elif (nextChar == "_"):
                    state = 2
                    self.lexeme = self.lexeme + nextChar
            if (state == 1):
                nextChar = self.file.read(1)
                if(nextChar in map(chr, range(65, 91)) + map(chr, range(97, 123))):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                elif (nextChar == "_"):
                    state = 2
                    self.lexeme = self.lexeme + nextChar
                elif (nextChar in map(chr, range(48, 58))):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                else:
                    done = True
                    self.file.seek(-1, 1)
                    # Check to see if identifier is a reserved word
                    self._checkReserved()                  
            if (state == 2):
                nextChar = self.file.read(1)
                if(nextChar in map(chr, range(65, 91)) + map(chr, range(97, 123))):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                elif (nextChar in map(chr, range(48, 58))):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                else:
                    self._scanError()
                    done = True
                    self.file.seek(-1, 1)    
                    
     
    def _scanNumericLit(self): pass

    def _scanError(self): 
        self.token = "MP_ERROR"
    
    def _checkReserved(self): 
        try:
            self.token = self.reserved[self.lexeme]
        except KeyError:
            self.token = "MP_IDENTIFIER"
    
    def _hashReserved(self):
        # Hash reserved words in dictionary
        self.reserved = {'and':'MP_AND',
                    'begin':'MP_BEGIN',
                    'div':'MP_DIV',
                    'do':'MP_DO',
                    'downto':'MP_DOWNTO',
                    'else':'MP_ELSE',
                    'end':'MP_END',
                    'fixed':'MP_FIXED', 
                    'float':'MP_FLOAT',
                    'for':'MP_FOR',
                    'function':'MP_FUNCTION',
                    'if':'MP_IF',
                    'integer':'MP_INTEGER',
                    'mod':'MP_MOD',
                    'not':'MP_NOT',
                    'or':'MP_OR',
                    'procedure':'MP_PROCEDURE',
                    'program':'MP_PROGRAM',
                    'read':'MP_READ',
                    'repeat':'MP_REPEAT',
                    'then':'MP_THEN',
                    'to':'MP_TO',
                    'until':'MP_UNTIL',
                    'var':'MP_VAR',
                    'while':'MP_WHILE',
                    'write':'MP_WRITE'}

