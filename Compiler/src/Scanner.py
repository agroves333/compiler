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
        self.file = open('program', 'r')

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
             if(nextChar == "("): self.scanLeftParen()
             if(nextChar == ")"): self.scanRightParen()
             if(nextChar == ";"): self.scanSemicolon()
             if(nextChar == ":"): self.scanColonOrAssignOp()
             if(nextChar in map(chr, range(65, 91)) + map(chr, range(97, 123))): self.scanId()
             if(nextChar in map(chr, range(48, 58))): self.scanNumericLit()
             
             #break when EOF is reached
             if not nextChar: break
             #END DISPATCHER
             
             print nextChar
    
         self.file.close()

     def getLexeme(self): return self.lexeme
     
     def getLineNumber(self): return self.line
     
     def getColumnNumber(self): return self.col
     
     
     def scanLeftParen(self): pass
     
     def scanRightParen(self): pass
     
     def scanSemicolon(self): pass
     
     def scanColonOrAssignOp(self): pass
     
     def scanId(self): pass
     
     def scanNumericLit(self): pass
     
     def scanEOF(self): pass
     
     def scanError(self): pass




