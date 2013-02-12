
from Scanner import Scanner

class Parser(object):
    
    scanner = Scanner()
    lookahead = ''
    
    # Constructor
    def __init__(self):
        pass

    def parse(self):
        
        self.lookahead = self.scanner.getNextToken()

    def match(self, toMatch): pass
        
    #1
    def systemGoal(self):
        if self.lookahead is "MP_PROGRAM":
            self.program()
        else:
            self.error()
    #2
    def program(self):
        if self.lookahead is "MP_PROGRAM":
            self.programHeading()
            self.match(';')
            self.block()
            self.match('.')
        else:
            self.error()
    
    #3
    def programHeading(self):
        if self.lookahead is "MP_PROGRAM":
            self.match("program")
            self.programIdentifier()
        else:
            self.error()
    
    #4
    def block(self):
        if self.lookahead is "MP_VAR":
            self.variableDeclarationPart()
            self.procedureAndFunctionDeclarationPart()
            self.statementPart()
        else:
            self.error()
    
    #5
    def variableDeclarationPart(self):
        if self.lookahead is "MP_VAR":
            self.match("var")
            self.variableDeclaration()
            self.match(';')
            self.variableDeclarationTail()
        else:
            self.error()
    
    #6 #7
    def variableDeclarationTail(self):
        if self.lookahead in ["MP_PROCEDURE", "MP_FUNCTION", "MP_BEGIN"]:
            return
        elif self.lookahead is "MP_IDENTIFIER":
            self.variableDeclaration()
            self.match(';')
            self.variableDeclarationTail()
        else:
            self.error()
    
    #8
    def variableDeclaration(self):
        if self.lookahead is "MP_IDENTIFIER":
            self.identifierList()
            self.match(':')
            self.type()
        else:
            self.error()
    
    #9 #10 #11
    def type(self):
        if self.lookahead is "MP_INTEGER":
            self.match("integer")
        elif self.lookahead is "MP_FLOAT":
            self.match("float")
        #TODO: Boolean rule #11
        else:
            self.error()
    
    #12 #13 #14
    def procedureAndFunctionDeclarationPart(self):
        if self.lookahead is "MP_PROCEDURE":
            self.procedureDeclaration()
            self.procedureAndFunctionDeclarationPart()
        elif self.lookahead is "MP_FUNCTION":
            self.functionDeclaration()
            self.procedureAndFunctionDeclarationPart()
        elif self.lookahead is "MP_BEGIN":
            return
        else:
            self.error()

    #15
    def procedureDeclaration(self): pass
    
    #16
    def functionDeclaration(self): pass
    
    #17
    def procedureHeading(self): pass
    
    #18
    def functionHeading(self): pass
    
    #19 #20
    def optionalFormalParameterList(self): pass
    
    #21 #22
    def formalParameterSectionTail(self): pass
    
    #23 #24
    def formalParameterSection(self): pass
    
    #25
    def valueParameterSection(self): pass
    
    #26
    def variableParameterSection(self): pass
    
    #27
    def statementPart(self): pass
    
    #28
    def compoundStatement(self): pass
    
    #29
    def statementSequence(self): pass
    
    #30 #31
    def statementTail(self): pass
    
    #32 - #41
    def statement(self): pass
    
    #42
    def emptyStatement(self): pass
    
    #
    def readStatement(self): pass
    
    #
    def readParameterTail(self): pass
    
    #
    def readParameter(self): pass
    
    #
    def writeStatement(self): pass
    
    #
    def writeParameterTail(self): pass
    
    #
    def writeParameter(self): pass
    
    #
    def assignmentStatement(self): pass
    
    #
    def ifStatement(self): pass
    
    #
    def optionalElsePart(self): pass
    
    #
    def repeatStatement(self): pass
    
    #
    def whileStatement(self): pass
    
    #
    def forStatement(self): pass
    
    #
    def controlVariable(self): pass
    
    #
    def initialValue(self): pass
    
    #
    def stepValue(self): pass
    
    #
    def finalValue(self): pass
    
    #
    def procedureStatement(self): pass
    
    #
    def optionalActualParameterList(self): pass
    
    #
    def actualParameterTail(self): pass
    
    #
    def actualParameter(self): pass
    
    #
    def expression(self): pass
    
    #
    def optionalRelationalPart(self): pass
    
    #
    def relationalOperator(self): pass
    
    #
    def simpleExpression(self): pass
    
    #
    def termTail(self): pass
    
    #
    def optionalSign(self): pass
    
    #
    def addingOperator(self): pass
    
    #
    def term(self): pass
    
    #
    def factorTail(self): pass
    
    #
    def multiplyingOperator(self): pass
    
    #
    def factor(self): pass
    
    #
    def programIdentifier(self): pass
    
    #
    def variableIdentifier(self): pass
    
    #
    def procedureIdentifier(self): pass
    
    #
    def functionIdentifier(self): pass
    
    #
    def booleanExpression(self): pass
    
    #
    def ordinalExpression(self): pass
    
    #
    def identifierList(self): pass
    
    #
    def identifierTail(self): pass
    
     
    def error(self):
        print "A parse error has been encountered"        