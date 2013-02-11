'''
Created on Feb 7, 2013

@author: david
'''
from Scanner import Scanner

class MyClass(object):
    
    scanner = Scanner()
    lookahead = ''
    
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
    
    def programHeading(self): pass
    
    def block(self): pass
    
    def variableDeclarationPart(self): pass
    
    def variableDeclarationTail(self): pass
    
    def variableDeclaration(self): pass
    
    def type(self): pass
    
    def procedureDeclaration(self): pass
    
    def functionDeclaration(self): pass
    
    def optionalFormalParameterList(self): pass
    
    def formalParameterSectionTail(self): pass
    
    def formalParameterSection(self): pass
    
    def valueParameterSection(self): pass
    
    def variableParameterSection(self): pass
    
    def statementPart(self): pass
    
    def compoundStatement(self): pass
    
    def statementSequence(self): pass
    
    def statementTail(self): pass
    
    def statement(self): pass
    
    def emptyStatement(self): pass
    
    def readStatement(self): pass
    
    def readParameterTail(self): pass
    
    def writeStatement(self): pass
    
    def writeParameterTail(self): pass
    
    def writeParameter(self): pass
    
    def assignmentStatement(self): pass
    
    def ifStatement(self): pass
    
    def optionalElsePart(self): pass
    
    def repeatStatement(self): pass
    
    def whileStatement(self): pass
    
    def forStatement(self): pass
    
    def controlVariable(self): pass
    
    def initialValue(self): pass
    
    def stepValue(self): pass
    
    def finalValue(self): pass
    
    def procedureStatement(self): pass
    
    def optionalActualParameterList(self): pass
    
    def actualParameterTail(self): pass
    
    def actualParameter(self): pass
    
    def expression(self): pass
    
    def optionalRelationalPart(self): pass
    
    def relationalOperator(self): pass
    
    def simpleExpression(self): pass
    
    def termTail(self): pass
    
    def optionalSign(self): pass
    
    def addingOperator(self): pass
    
    def term(self): pass
    
    def factorTail(self): pass
    
    def multiplyingOperator(self): pass
    
    def factor(self): pass
    
    def programIdentifier(self): pass
    
    def variableIdentifier(self): pass
    
    def procedureIdentifier(self): pass
    
    def functionIdentifier(self): pass
    
    def booleanExpression(self): pass
    
    def ordinalExpression(self): pass
    
    def identifierList(self): pass
    
    def identifierTail(self): pass
    
     
    def error(self):
        print "A parse error has been encountered"        