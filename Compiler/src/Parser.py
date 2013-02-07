'''
Created on Feb 7, 2013

@author: david
'''
from Scanner import Scanner

class MyClass(object):
    
    scanner = Scanner()
    
    # Constructor
    def __init__(self):
        pass
    
    
    def parse(self):
        
        self.lookahead = self.scanner.getNextToken()
        
    
    def systemGoal(self):
        if(self.lookahead == "MP_PROGRAM"):
            self.program()
        else:
            self.error()
    
    def program(self): pass
    
    def error(self):
        print "A parse error has been encountered"        