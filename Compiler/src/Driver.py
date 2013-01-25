'''
Created on Jan 24, 2013

@author: david
'''
from ScanPack.Scanner import Scanner

def main():
    fileName = raw_input('Enter an input filename: ')
    
    fileScanner = Scanner(fileName)
    
    fileScanner.scan()
    
if __name__ == '__main__':
    main()