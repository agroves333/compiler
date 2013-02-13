'''
Created on Feb 13, 2013

@author: david
'''
import sys
from Scanner import Scanner
from Parser import Parser

def main():    
    fileName = sys.argv[1]
    
    try:
        sourceFile = open(fileName, 'r')
    except IOError:
        sys.exit("Source file not found")
        
    scanner = Scanner(sourceFile)
    parser = Parser(scanner)
    
    parser.parse()
    
    file.close()
    
if __name__ == '__main__':
    main()