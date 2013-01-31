import sys

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
        self.__hashReserved()
    
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
        
            self.__discard_whitespace()
      
            nextChar = self.file.read(1)
            
            self.file.seek(-1, 1)
         
            #BEGINNING OF DISPATCHER
            if(nextChar == "."): self.__scanPeriod()
        
            elif(nextChar == ","): self.__scanComma()
        
            elif(nextChar == ";"): self.__scanSemicolon()
        
            elif(nextChar == "("): self.__scanLeftParen()

            elif(nextChar == ")"): self.__scanRightParen()

            elif(nextChar == "="): self.__scanEqual()
        
            elif(nextChar == "+"): self.__scanPlus()
        
            elif(nextChar == "-"): self.__scanMinus()
        
            elif(nextChar == "*"): self.__scanTimes()

            elif(nextChar == ":"): self.__scanColonOrAssignOp()
            
            elif(nextChar == ">"): self.__scanGthanOrGequal()
            
            elif(nextChar == "<"): self.__scanLthanOrLequalorNequal()
            
            elif(nextChar == "{"): self.__scanComment()

            elif(nextChar == "'"): self.__scanString()

            elif(self.__isLetter(nextChar) or (nextChar == "_")): self.__scanId()

            elif(self.__isDigit(nextChar)): self.__scanNumericLit()
                
            else:
                self.__scanError()
                self.col += 1
                self.lexeme= nextChar
                self.file.read(1)
        
        return self.token

    def getLexeme(self):
        return self.lexeme

    def getLineNumber(self):
        return self.line

    def getColumnNumber(self):
        return self.col


    #Private functions

    def __discard_whitespace(self):
        nextChar = self.file.read(1)
        while(nextChar in [" ", "\n"]):
            if(nextChar == " "):
                self.col += 1
            elif(nextChar == "\n"):
                self.line += 1
                self.col = 0
            nextChar = self.file.read(1)
        self.file.seek(-1, 1)

    def __isLetter(self, nextChar):
        return nextChar in map(chr, range(65, 91)) + map(chr, range(97, 123))

    def __isDigit(self, nextChar):
        return nextChar in map(chr, range(48, 58))

    def __scanPeriod(self):
        self.token = "MP_PERIOD"
        self.lexeme = "."
        self.col += 1
        self.file.read(1)

    def __scanComma(self):
        self.token = "MP_COMMA"
        self.lexeme = ","
        self.col += 1
        self.file.read(1)

    def __scanSemicolon(self):
        self.token = "MP_SCOLON"
        self.lexeme = ";"
        self.col += 1
        self.file.read(1)

    def __scanLeftParen(self):
        self.token = "MP_LPAREN"
        self.lexeme = "("
        self.col += 1
        self.file.read(1)

    def __scanRightParen(self):
        self.token = "MP_RPAREN"
        self.lexeme = ")"
        self.col += 1
        self.file.read(1)

    def __scanEqual(self):
        self.token = "MP_EQUAL"
        self.lexeme = "="
        self.col += 1
        self.file.read(1)

    def __scanPlus(self):
        self.token = "MP_PLUS"
        self.lexeme = "+"
        self.col += 1
        self.file.read(1)

    def __scanMinus(self):
        self.token = "MP_MINUS"
        self.lexeme = "-"
        self.col += 1
        self.file.read(1)

    def __scanTimes(self):
        self.token = "MP_TIMES"
        self.lexeme = "*"
        self.col += 1
        self.file.read(1)


    def __scanColonOrAssignOp(self):
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

    def __scanGthanOrGequal(self):
        state = 0
        done = False
        self.lexeme = ""

        while not done:
            if (state == 0):
                nextChar = self.file.read(1)
                if(nextChar == ">"):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
            elif (state == 1):
                nextChar = self.file.read(1)
                if(nextChar == "="):
                    state = 2
                    self.lexeme = self.lexeme + nextChar
                else:
                    self.token = 'MP_GTHAN'
                    self.col += 1
                    done = True
                    self.file.seek(-1, 1)
            elif (state == 2):
                self.token = 'MP_GEQUAL'
                self.col += 1
                done = True

    def __scanLthanOrLequalorNequal(self):
        state = 0
        done = False
        self.lexeme = ""

        while not done:
            if (state == 0):
                nextChar = self.file.read(1)
                if(nextChar == "<"):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
            elif (state == 1):
                nextChar = self.file.read(1)
                if(nextChar == "="):
                    state = 2
                    self.lexeme = self.lexeme + nextChar
                elif(nextChar == ">"):
                    state = 3
                    self.lexeme = self.lexeme + nextChar
                else:
                    self.token = 'MP_LTHAN'
                    self.col += 1
                    done = True
                    self.file.seek(-1, 1)
            elif (state == 2):
                self.token = 'MP_LEQUAL'
                self.col += 1
                done = True
            elif (state == 3):
                self.token = 'MP_NEQUAL'
                self.col += 1
                done = True

    def __scanId(self):
        state = 0
        done = False

        while not done:
            if (state == 0):
                nextChar = self.file.read(1)
                if(self.__isLetter(nextChar)):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                elif (nextChar == "_"):
                    state = 2
                    self.lexeme = self.lexeme + nextChar
            if (state == 1):
                nextChar = self.file.read(1)
                if(self.__isLetter(nextChar)):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                elif (nextChar == "_"):
                    state = 2
                    self.lexeme = self.lexeme + nextChar
                elif (self.__isDigit(nextChar)):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                else:
                    done = True
                    if nextChar:
                        self.file.seek(-1,1)
                    # Check to see if identifier is a reserved word
                    self.__checkReserved()                  
            if (state == 2):
                nextChar = self.file.read(1)
                if(self.__isLetter(nextChar)):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                elif (self.__isDigit(nextChar)):
                    state = 1
                    self.lexeme = self.lexeme + nextChar
                else:
                    self.__scanError()
                    done = True
                    self.file.seek(-1, 1)    
                    
     
    def __scanNumericLit(self): 
        state = 0
        done = False
        self.lexeme = ""
        
        while not done:
            if (state == 0):
                nextChar = self.file.read(1)
                if (self.__isDigit(nextChar)):           # if nextChar is digit
                    state = 1
                    self.lexeme += nextChar
                    
            if (state == 1):
                nextChar = self.file.read(1)
                if (self.__isDigit(nextChar)):
                    state = 1
                    self.lexeme += nextChar
                elif (nextChar == "."):                             # if "." don't append to lememe until digit is read in state 2
                    state = 2
                elif (nextChar in ["e", "E"]):                      # if "e" or "E" don't append to lexeme until digit is read in state 4
                    state = 4
                    
                else:
                    if nextChar:                                    # check if nextChar exist, if not, then the file pointer isn't rewound.
                        self.file.seek(-1, 1)                       #    this ensures that the MP_EOF token is passed (getNextToken fails).
                    self.token = 'MP_INTEGER_LIT'                   #    the same check happens on all other state's else clause (other char)
                    done = True
                    
            if (state == 2):
                nextChar = self.file.read(1)
                if (self.__isDigit(nextChar)):
                    state = 3
                    self.lexeme = self.lexeme + "." + nextChar      # if digit, then append "." and digit. This prevents the "." from appending
                else:                                               #    when nextChar isn't a digit which would return MP_INTEGER_LIT but with 
                    if nextChar:                                    #    the lexeme including the "." on the end. 
                        self.file.seek(-2, 1)
                    else: 
                        self.file.seek(-1, 1)
                    self.token = 'MP_INTEGER_LIT'
                    done = True
                    
            if (state == 3):
                nextChar = self.file.read(1)
                if (self.__isDigit(nextChar)):
                    state = 3
                    self.lexeme += nextChar
                elif (nextChar in ["e", "E"]):                      # if "e" or "E" don't append to lexeme until digit is read in state 4
                    state = 4
                else:
                    if nextChar:
                        self.file.seek(-1, 1)
                    self.token = 'MP_FIXED_LIT'
                    done = True
                    
            if (state == 4):
                nextChar = self.file.read(1)
                if (nextChar in ['+', '-']):                        # if "+/-" , don't append to lexeme until digit is read in state 5
                    state = 5
                elif (self.__isDigit(nextChar)):         # if digit is read, append "e" or "E" to the lexeme depending on what was read
                    state = 6                                       #    to get to state 4 (rewind file pointer by 2). This is possible b/c the only way
                    self.file.seek(-2, 1)                           #    to get to state 4 is by reading an "e" or "E"
                    e = self.file.read(1)
                    self.lexeme = self.lexeme + e + nextChar
                    self.file.seek(1, 1)
                else:
                    if nextChar:
                        self.file.seek(-2, 1)
                    else:
                        self.file.seek(-1, 1)
                        
                    self.token = 'MP_FIXED_LIT'
                    done = True

            if (state == 5):
                nextChar = self.file.read(1)
                if (self.__isDigit(nextChar)):               # If digit is read, append "e" or "E" to the lexeme depending on what was read
                    state = 6                                           #   along with appending the "+/-" to the lemexe. 
                    self.file.seek(-2, 1)                               # Get the sign which is ensured to be the previous char since the only way to 
                    sign = self.file.read(1)                            #   get to state 5 is by reading a "+/-"
                    if (sign in ["e", "E"]):                            # If "e/E" is read as the sign, no polarity is being used so append "e/E", and 
                        self.lexeme = self.lexeme + sign + nextChar     #    the digit read to the lexeme
                    elif(sign in ["+", "-"]):                           # Else if "+/-" is read as sign, then append "+/-" , "e/E" and digit to lexeme
                        self.file.seek(-2, 1)
                        e = self.file.read(1)
                        self.lexeme = self.lexeme + e + sign + nextChar
                        self.file.seek(1, 1)
                        
                    self.file.seek(1, 1)
                else:
                    if nextChar:
                        self.file.seek(-3, 1)
                    else:
                        self.file.seek(-2, 1)
                            
                    self.token = 'MP_FIXED_LIT'
                    done = True
                    
            if (state == 6):
                nextChar = self.file.read(1)
                if (self.__isDigit(nextChar)):
                    state = 6
                    self.lexeme += nextChar
                else:
                    if nextChar:
                        self.file.seek(-1, 1)
                    self.token = 'MP_FLOAT_LIT'
                    done = True
                
    def __scanString(self):
        state = 0
        done = False
        self.lexeme = ""
        self.file.read(1) #discard first char, which is '

        while not done:
            if state == 0:
                nextChar = self.file.read(1)
                if nextChar == "\n":
                    self.token = "MP_RUN_STRING"
                    done = True
                elif nextChar == "'":
                    state = 1
                else:
                    self.lexeme += nextChar
            if state == 1:
                nextChar = self.file.read(1)
                if nextChar == "'":
                    self.lexeme += nextChar
                    state = 0
                else:
                    self.token = "MP_STRING_LIT"
                    self.file.seek(-1, 1)
                    done = True
    
    def __scanComment(self):
        self.lexeme = ""
        nextChar = self.file.read(1)
        
        while not (nextChar == "}"):
            if not self.file.read(1):
                self.token = "MP_RUN_COMMENT"
                return
            else:
                self.file.seek(-1, 1)
                nextChar = self.file.read(1)
                
        self.getNextToken()

    def __scanError(self): 
        self.token = "MP_ERROR"
    
    def __checkReserved(self): 
        try:
            self.token = self.reserved[self.lexeme.lower()]
        except KeyError:
            self.token = "MP_IDENTIFIER"
    
    def __hashReserved(self):
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

