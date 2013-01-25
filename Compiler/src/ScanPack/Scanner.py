'''
Created on Jan 24, 2013

@author: david
'''
import sys

class Scanner():
    '''
    classdocs
    '''
    

    def __init__(self, fileName):
        '''
        Constructor
        '''
        self.fileName = fileName
        
    def scan(self):
        '''
        Main function to begin scanning process
        '''  
        try:
            file = open(self.fileName, 'r')          
                        
            print "I am scanning " + repr(self.fileName) + " for Tokens"  
            
            file.close
        except IOError:
            print "File not found"    

        
        