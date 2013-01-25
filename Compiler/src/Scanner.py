'''
Created on Jan 24, 2013

@author: david
'''

class Scanner(object):

    lexeme = ""

    token = ""

    line = int(1)

    col = int(1)

    file = None

     

    def __init__(self):
        pass
    
    def openFile(self, fileName):
        self.file = open(fileName, 'r')

    def getNextToken(self):

        while True:

            filePointer = self.file.tell()

            nextChar = self.file.read(1)

        
            #skip space
            
            if(nextChar == " "):

                self.col += 1

                continue

             
            if(nextChar == "\n"):

                self.line += 1

                self.col = 0

                continue

             
            #START DISPATCHER

            if(nextChar == "("): self._scanLeftParen()

            if(nextChar == ")"): self._scanRightParen()

            if(nextChar == ";"): self._scanSemicolon()

            if(nextChar == ":"): self._scanColonOrAssignOp()

            if(nextChar in map(chr, range(65, 91)) + map(chr, range(97, 123))): self._scanId()

            if(nextChar in map(chr, range(48, 58))): self._scanNumericLit()


            #break when EOF is reached

            if not nextChar: break

            #END DISPATCHER

             
            print nextChar

            self.file.close()



    def getLexeme(self): return self.lexeme

     

    def getLineNumber(self): return self.line

     

    def getColumnNumber(self): return self.col

     

     

    def _scanLeftParen(self): pass

     

    def _scanRightParen(self): pass

     

    def _scanSemicolon(self): pass

     

    def _scanColonOrAssignOp(self): pass

     

    def _scanId(self): pass

     

    def _scanNumericLit(self): pass

     

    def _scanEOF(self): pass

     

    def _scanError(self): pass

