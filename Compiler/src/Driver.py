'''
Created on Jan 24, 2013

@author: david
'''

import sys
from Scanner import Scanner

def main():
<<<<<<< HEAD
    fileName = sys.argv[1]
    
    scanner = Scanner()
    
    scanner.openFile(fileName)
    
    while(scanner.hasNext()):
        scanner.getToken()
        scanner.getLineNumber()
        scanner.getColumnNumber()
        scanner.getLexeme()
=======
    
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
        output = str(token) + " " + str(line) + " " + str(col) + " " + str(lexeme) + "\n"
        print output   
        outFile.write(output)
        
    scanner.closeFile()
>>>>>>> b66adfcae2d4449d6d1a5cfd211d69389fd36f9a
    
