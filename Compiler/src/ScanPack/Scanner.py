'''
Created on Jan 24, 2013

@author: david
'''
import sys

class Scanner():
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        
    def openFile(self, fileName):
        '''
        Main function to begin scanning process
        '''  
        try:
            file = open(fileName, 'r')          
                        
            print "I am scanning " + repr(fileName) + " for Tokens"  
            
            file.close
        except IOError:
            print "File not found"    

    def getToken(self):
        '''
        '''
        
    def getLexeme(self):
        '''
        '''
        
    def getLineNumber(self):
        '''
        '''
        