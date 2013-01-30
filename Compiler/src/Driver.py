'''
Created on Jan 24, 2013

@author: david
'''

import sys
from Scanner import Scanner

def main():
    
    # Define vars
    lexeme = ""
    token = ""
    line = 1
    col = 1
    
    fileName = sys.argv[1]
    
    scanner = Scanner()
    scanner.openFile(fileName)
    
    outFile = open('output.txt', 'w')
    
    while True:
        token = scanner.getNextToken()
        line = scanner.getLineNumber()
        col = scanner.getColumnNumber()
        lexeme = scanner.getLexeme() 
        
        #Write token info to output file
        if(token != ""):
            output = str(token) + " " + str(line) + " " + str(col) + " " + str(lexeme) + "\n"
            print output
            outFile.write(output)
        
        if not scanner.hasNext():
            break
        
    scanner.closeFile()


if __name__ == "__main__":
    main()