'''
Created on Feb 13, 2013

@author: david
'''
import sys
from Parser import Parser

def main():    
    fileName = sys.argv[1]
    
    try:
        sourceFile = open(fileName, 'r')
    except IOError:
        sys.exit("Source file not found")

    parser = Parser(sourceFile)
    
    parser.parse()
    
    sourceFile.close()
    
if __name__ == '__main__':
    main()