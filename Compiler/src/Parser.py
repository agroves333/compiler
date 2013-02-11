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
        
    #1
    def systemGoal(self):
        if(self.lookahead == "MP_PROGRAM"):
            self.program()
        else:
            self.error()
    #2
    def program(self): pass
    
    #3
    def programHeading(self): pass
    
    #4
    def block(self): pass
    
    #5
    def variableDeclarationPart(self): pass
    
    #6
    def variableDeclarationTail(self): pass
    
    #7
    def variableDeclaration(self): pass
    
    #8
    def type(self): pass
    
    #9
    def procedureAndFunctionDeclarationPart(self): pass
    
    #10
    def procedureDeclaration(self): pass
    
    #11
    def functionDeclaration(self): pass
    
    #12
    def procedureHeading(self): pass
    
    #13
    def functionHeading(self): pass
    
    #14
    def optionalFormalParameterList(self): pass
    
    #15
    def formalParameterSectionTail(self): pass
    
    #16
    def formalParameterSection(self): pass
    
    #17
    def valueParameterSection(self): pass
    
    #18
    def variableParameterSection(self): pass
    
    #19
    def statementPart(self): pass
    
    #20
    def compoundStatement(self): pass
    
    #21
    def statementSequence(self): pass
    
    #22
    def statementTail(self): pass
    
    #23
    def statement(self): pass
    
    #24
    def emptyStatement(self): pass
    
    #25
    def readStatement(self): pass
    
    #26
    def readParameterTail(self): pass
    
    #27
    def readParameter(self): pass
    
    #28
    def writeStatement(self): pass
    
    #29
    def writeParameterTail(self): pass
    
    #30
    def writeParameter(self): pass
    
    #31
    def assignmentStatement(self): pass
    
    #32
    def ifStatement(self): pass
    
    #33
    def optionalElsePart(self): pass
    
    #34
    def repeatStatement(self): pass
    
    #35
    def whileStatement(self): pass
    
    #36
    def forStatement(self): pass
    
    #37
    def controlVariable(self): pass
    
    #38
    def initialValue(self): pass
    
    #39
    def stepValue(self): pass
    
    #40
    def finalValue(self): pass
    
    #41
    def procedureStatement(self): pass
    
    #42
    def optionalActualParameterList(self): pass
    
    #43
    def actualParameterTail(self): pass
    
    #44
    def actualParameter(self): pass
    
    #45
    def expression(self): pass
    
    #46
    def optionalRelationalPart(self): pass
    
    #47
    def relationalOperator(self): pass
    
    #48
    def simpleExpression(self): pass
    
    #49
    def termTail(self): pass
    
    #50
    def optionalSign(self): pass
    
    #51
    def addingOperator(self): pass
    
    #52
    def term(self): pass
    
    #53
    def factorTail(self): pass
    
    #54
    def multiplyingOperator(self): pass
    
    #55
    def factor(self): pass
    
    #56
    def programIdentifier(self): pass
    
    #57
    def variableIdentifier(self): pass
    
    #58
    def procedureIdentifier(self): pass
    
    #59
    def functionIdentifier(self): pass
    
    #60
    def booleanExpression(self): pass
    
    #61
    def ordinalExpression(self): pass
    
    #62
    def identifierList(self): pass
    
    #63
    def identifierTail(self): pass
    
     
    def error(self):
        print "A parse error has been encountered"        