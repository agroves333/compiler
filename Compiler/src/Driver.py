'''
Created on Jan 24, 2013

@author: david
'''
import sys
from ScanPack.Scanner import Scanner

def main():
    fileName = sys.argv[0]
    
    fileScanner = Scanner()
    
    fileScanner.openFile(fileName)
    
if __name__ == '__main__':
    main()