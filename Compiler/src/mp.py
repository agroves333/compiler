'''
Created on Feb 13, 2013

@author: david
'''
import sys
from Parser import Parser

def main():    
    fileName = sys.argv[1]

    parser = Parser(fileName)
    
    parser.parse()
    
if __name__ == '__main__':
    main()