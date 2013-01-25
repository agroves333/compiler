'''
Created on Jan 24, 2013

@author: david
'''
import sys
from Scanner import Scanner

def main():
    
    lexeme = ""

    token = ""

    line = int(1)

    col = int(1)
    
    fileName = sys.argv[1]
    
    scanner = Scanner()
    
    scanner.openFile(fileName)
    
    outFile = open('output.txt', 'w')
    
    while(scanner.hasNext()):
        token = scanner.getNextToken()
        line = scanner.getLineNumber()
        col = scanner.getColumnNumber()
        lexeme = scanner.getLexeme() 
        
        #Write token info to output file
        output = str(token) + " " + str(line) + " " + str(col) + " " + str(lexeme)    
        outFile.write(output)
        
    scanner.closeFile()
    
if __name__ == '__main__':
    main()