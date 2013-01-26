'''
Created on Jan 24, 2013

@author: david
'''

import sys

class Scanner(object):

    # Initialize vars
    lexeme = ""
    token = ""
    line = int(1)
    col = int(1)
    file = None

    # Constuctor 
    def __init__(self):
        pass
    
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
        if not self.file.read(1):
            return False
        else:
            self.file.seek(-1, 1)
            return True
    
    def getNextToken(self):

        nextChar = self.file.read(1)
 
        #skip space        
        if(nextChar == " "):

            self.col += 1

            self.getNextToken()

        #skip newline 
        if(nextChar == "\n"):

            self.line += 1

            self.col = 0

            self.getNextToken()

         
        #START DISPATCHER
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

        elif(nextChar in map(chr, range(65, 91)) + map(chr, range(97, 123))): self._scanId()

        elif(nextChar in map(chr, range(48, 58))): self._scanNumericLit()
        
        self.col += 1
        
        return self.token


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
        
    def _scanComma(self):
        self.token = "MP_COMMA" 
        self.lexeme = ","
 
    def _scanSemicolon(self):
        self.token = "MP_SCOLON" 
        self.lexeme = ";"
            
    def _scanLeftParen(self):
        self.token = "MP_LPAREN" 
        self.lexeme = "("
     
    def _scanRightParen(self):
        self.token = "MP_RPAREN" 
        self.lexeme = ")"
            
    def _scanEqual(self):
        self.token = "MP_EQUAL" 
        self.lexeme = "="

    def _scanPlus(self):
        self.token = "MP_PLUS" 
        self.lexeme = "+"
    
    def _scanMinus(self):
        self.token = "MP_MINUS" 
        self.lexeme = "-"
        
    def _scanTimes(self):
        self.token = "MP_TIMES" 
        self.lexeme = "*"
        
            
    def _scanColonOrAssignOp(self): pass
    
    def _scanId(self): pass
     
    def _scanNumericLit(self): pass
     
    def _scanEOF(self): pass

    def _scanError(self): pass

