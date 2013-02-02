'''
Created on Jan 24, 2013

@author: david
'''

import sys
from Scanner import Scanner

def main():
    
    lexeme = ""
    token = ""
    line = 1
    col = 0
    
    fileName = sys.argv[1]
    
    scanner = Scanner()
    scanner.openFile(fileName)
    
    outFile = open('output.txt', 'w')
    
    output = '{0:16s} {1:4s} {2:4s} {3:15s}'.format('Token', 'Line', 'Column', 'Lexeme') + "\n--------------------------------------\n"
    print output
    outFile.write(output)
    
    while True:
        token = scanner.getNextToken()
        line = scanner.getLineNumber()
        col = scanner.getColumnNumber()
        lexeme = scanner.getLexeme() 
        
        #Write token info to output file
        if(token != ''):
            output = '{0:16s} {1:4d} {2:4d} {3:15s}'.format(token, line, col, "   " + str(lexeme)) + "\n"
            print output
            outFile.write(output)
        
        if not scanner.hasNext():
            break
      
    scanner.closeFile()


if __name__ == "__main__":
    main()