'''
Created on Jan 24, 2013

@author: david
'''
import sys
from ScanPack.Scanner import Scanner

def main():
    fileName = sys.argv[1]
    
    scanner = Scanner()
    
    scanner.openFile(fileName)
    
    while(scanner.hasNext()):
        scanner.getToken()
        scanner.getLineNumber()
        scanner.getColumnNumber()
        scanner.getLexeme()
    
if __name__ == '__main__':
    main()