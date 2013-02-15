import sys
from Scanner import Scanner

class Parser(object):
    
    scanner = None
    lookahead = ''
    
    # Constructor
    def __init__(self, sourceFile):
        self.scanner = Scanner(sourceFile)

    def parse(self):    
        self.lookahead = self.scanner.getNextToken()
        self.systemGoal()

    def match(self, toMatch): 
        if(self.lookahead == toMatch):
            self.lookahead = self.scanner.getNextToken()
        else:
            self.error()
            
    
    def systemGoal(self):
        if self.lookahead is "MP_PROGRAM":                  # 1 SystemGoal -> Program eof
            self.program()
        else:
            self.error()
            
   
    def program(self):
        if self.lookahead is "MP_PROGRAM":                  # 2 Program -> ProgramHeading ";" Block "."
            self.programHeading()
            self.match("MP_SCOLON")
            self.block()
            self.match("MP_PERIOD")
        else:
            self.error()
    
    
    def programHeading(self):
        if self.lookahead is "MP_PROGRAM":                  # 3 ProgramHeading -> "program" ProgramIdentifier
            self.match("MP_PROGRAM")
            self.programIdentifier()
        else:
            self.error()
    
    
    def block(self):
        if self.lookahead is "MP_VAR":                      # 4 Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart
            self.variableDeclarationPart()
            self.procedureAndFunctionDeclarationPart()
            self.statementPart()
        else:
            self.error()
    
    
    
    def variableDeclarationPart(self):
        if self.lookahead is "MP_VAR":                      # 5 VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
            self.match("MP_VAR")
            self.variableDeclaration()
            self.match("MP_SCOLON")
            self.variableDeclarationTail()
        else:
            self.error()
    
    
    
    
    def variableDeclarationTail(self):
        if self.lookahead in ["MP_PROCEDURE", "MP_FUNCTION", "MP_BEGIN"]:  # 7 VariableDeclarationTail -> lambda
            return
        elif self.lookahead is "MP_IDENTIFIER":             # 6 VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail 
            self.variableDeclaration()
            self.match("MP_SCOLON")
            self.variableDeclarationTail()
        else:
            self.error()
    
    
    
    def variableDeclaration(self):
        if self.lookahead is "MP_IDENTIFIER":               # 8 VariableDeclaration -> Identifierlist ":" Type  
            self.identifierList()
            self.match("MP_SCOLON")
            self.type()
        else:
            self.error()
    
    
    
    
    def type(self):
        if self.lookahead is "MP_INTEGER":                  # 9   Type -> "Integer"
            self.match("MP_INTEGER")
        elif self.lookahead is "MP_FLOAT":                  # 10  Type -> "Float"
            self.match("MP_FLOAT")
        #TODO: Boolean rule #11
                                                            # 11  Type -> "Boolean"
        else:
            self.error()
    
    
    def procedureAndFunctionDeclarationPart(self):
        if self.lookahead is "MP_PROCEDURE":                # 12 ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
            self.procedureDeclaration()
            self.procedureAndFunctionDeclarationPart()
        elif self.lookahead is "MP_FUNCTION":               # 13 ProcedureAndFunctionDeclarationPart -> FunctionDeclaration ProcedureAndFunctionDeclarationPart
            self.functionDeclaration()
            self.procedureAndFunctionDeclarationPart()
        elif self.lookahead is "MP_BEGIN":                  # 14 ProcedureAndFunctionDeclarationPart -> lambda
            return
        else:
            self.error()

    
    def procedureDeclaration(self):
        if self.lookahead is "MP_PROCEDURE":                # 15 ProcedureDeclaration -> ProcedureHeading ";" Block ";"
            self.procedureHeading();
            self.match('MP_SCOLON')
            self.block()
            self.match('MP_SCOLON')
        else:
            self.error()
    
          
    def functionDeclaration(self):
        if self.lookahead is "MP_FUNCTION":                 # 16 FunctionDeclaration  -> FunctionHeading ";" Block ";" 
            self.functionHeading()
            self.match("MP_SCOLON");
        else:
            self.error()
    
    
    def procedureHeading(self):
        if self.lookahead is "MP_PROCEDURE":                # 17 ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
            self.match("MP_PROCEDURE")
            self.procedureIdentifier()
            self.optionalFormalParameterList()
        else:
            self.error()
    
    
    def functionHeading(self):
        if self.lookahead is "MP_FUNCTION":                 # 18 FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList ":" Type
            self.match("MP_FUNCTION")
            self.procedureIdentifier()
            self.optionalFormalParameterList()
            self.match("MP_COLON")
            self.type()
        else:
            self.error()
    
    
    
    def optionalFormalParameterList(self):
        if self.lookahead is 'MP_LPAREN':                   # 19 OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
            self.match('MP_LPAREN')
            self.formalParameterSection()
            self.formalParameterSectionTail()
        elif self.lookahead in ['MP_COLON', 'MP_SCOLON']:   # 20 OptionalFormalParameterList -> lambda
            return
        else:
            self.error
       
    
    def formalParameterSectionTail(self):
        if self.lookahead is "MP_SCOLON":                   # 21 FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
            self.match('MP_SCOLON')
            self.formalParameterSection()
            self.formalParameterSectionTail()
        elif self.lookahead is 'MP_LPAREN':                 # 22 FormalParameterSectionTail -> lambda
            return 
        else:
            self.error
    
    
    
    def formalParameterSection(self):
        if self.lookahead is 'MP_IDENTIFIER':               # 23 FormalParameterSection -> ValueParameterSection
            self.valueParameterSection()
        elif self.lookahead is 'MP_VAR':                    # 24 FormalParameterSection -> VariableParameterSection
            self.variableParameterSection()
        else:
            self.error()
    
    
    def valueParameterSection(self):
        if self.lookahead is 'MP_IDENTIFIER':               # 25 ValueParameterSection -> IdentifierList ":" Type
            self.identifierList()
            self.match('MP_COLON')
            self.type()
        else:
            self.error()
    
    # 26 VariableParameterSection -> "var" IdentifierList ":" Type
    def variableParameterSection(self): pass
    
    # 27 StatementPart -> CompoundStatement 
    def statementPart(self): pass
    
    # 28 CompoundStatement -> "begin" StatementSequence "end"
    def compoundStatement(self): pass
    
    # 29 StatementSequence -> Statement StatementTail
    def statementSequence(self): pass
    
    # 30 StatementTail -> ";" Statement StatementTail
    # 31 StatementTail -> lambda
    def statementTail(self): pass
    
    # 32 Statement -> EmptyStatement
    # 33 Statement -> CompoundStatement 
    # 34 Statement -> ReadStatement
    # 35 Statement -> WriteStatement
    # 36 Statement -> AssignmentStatement
    # 37 Statement -> IfStatement
    # 38 Statement -> WhileStatement
    # 39 Statement -> RepeatStatement
    # 40 Statement -> ForStatement
    # 41 Statement -> ProcedureStatement
    def statement(self): pass
    
    # 42 EmptyStatement -> lambda
    def emptyStatement(self): pass
    
    # 43 ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
    def readStatement(self): pass
    
    # 44 ReadParameterTail -> "," ReadParameter ReadParameterTail
    # 45 ReadParameterTail -> lambda
    def readParameterTail(self): pass
    
    # 46 ReadParameter -> VariableIdentifier   
    def readParameter(self): pass
    
    # 47 WriteStatement -> "write" "(" WriteParameter WriteParameterTail ")"
    def writeStatement(self): pass
    
    # 48 WriteParameterTail -> "," WriteParameter
    # 49 WriteParameterTail -> lambda
    def writeParameterTail(self): pass
    
    # 50 WriteParameter -> OrdinalExpression    
    def writeParameter(self): pass
    
    # 51 AssignmentStatement -> VariableIdentifier ":=" Expression
    # 52 AssignmentStatement -> FunctionIdentifier ":=" Expression  
    def assignmentStatement(self): pass
    
    # 53 IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
    def ifStatement(self): pass
    
    # 54 OptionalElsePart -> "else" Statement
    # 55 OptionalElsePart -> lambda 
    def optionalElsePart(self): pass
    
    # 56 RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression            
    def repeatStatement(self): pass
    
    # 57 WhileStatement -> "while" BooleanExpression "do" Statement   
    def whileStatement(self): pass
    
    # 58 ForStatement -> "for" ControlVariable ":=" InitialValue StepValue FinalValue "do" Statement
    def forStatement(self): pass
    
    # 59 ControlVariable -> VariableIdentifier
    def controlVariable(self): pass
    
    # 60 InitialValue -> OrdinalExpression
    def initialValue(self): pass
    
    # 61 StepValue -> "to"
    # 62 StepValue -> "downto"
    def stepValue(self): pass
    
    # 63 FinalValue -> OrdinalExpression
    def finalValue(self): pass
    
    # 64 ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
    def procedureStatement(self): pass
    
    # 65 OptionalActualParameterList -> "(" ActualParameter ActualParameterTail ")"    
    # 66 OptionalActualParameterList -> lambda
    def optionalActualParameterList(self): pass
    
    # 67 ActualParameterTail -> "," ActualParameter ActualParameterTail    
    # 68 ActualParameterTail -> lambda
    def actualParameterTail(self): pass
    
    # 69 ActualParameter -> OrdinalExpression
    def actualParameter(self): pass
    
    # 70 Expression -> SimpleExpression OptionalRelationalPart
    def expression(self): pass
    
    # 71 OptionalRelationalPart -> RelationalOperator SimpleExpression    
    # 72 OptionalRelationalPart -> lambda
    def optionalRelationalPart(self): pass
    
    # 73 RelationalOperator -> "="    
    # 74 RelationalOperator -> "<"    
    # 75 RelationalOperator -> ">"    
    # 76 RelationalOperator -> "<="    
    # 77 RelationalOperator -> ">="    
    # 78 RelationalOperator -> "<>"
    def relationalOperator(self): pass
    
    # 79 SimpleExpression -> OptionalSign Term TermTail
    def simpleExpression(self): pass
    
    # 80 TermTail -> AddingOperator Term TermTail    
    # 81 TermTail -> lambda
    def termTail(self): pass
    
    # 82 OptionalSign -> "+"    
    # 83 OptionalSign -> "-"    
    # 84 OptionalSign -> lambda
    def optionalSign(self): pass
    
    # 85 AddingOperator -> "+"    
    # 86 AddingOperator -> "-"   
    # 87 AddingOperator -> "or"
    def addingOperator(self): pass
    
    # 88 Term -> Factor FactorTail    
    def term(self): pass
    
    # 89 FactorTail -> MultiplyingOperator Factor FactorTail    
    # 90 FactorTail -> lambda
    def factorTail(self): pass
    
    # 91 MultiplyingOperator  -> "*"    
    # 92 MultiplyingOperator  -> "div"    
    # 93 MultiplyingOperator  -> "mod"    
    # 94 MultiplyingOperator  -> "and"
    def multiplyingOperator(self): pass
    
    # 95 Factor -> UnsignedInteger
    # 96 Factor -> VariableIdentifier
    # 97 Factor -> "not" Factor    
    # 98 Factor -> "(" Expression ")"    
    # 99 Factor -> FunctionIdentifier OptionalActualParameterList
    def factor(self): pass
    
    # 100 ProgramIdentifier -> Identifier
    def programIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):
            self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    # 101 VariableIdentifier -> Identifier
    def variableIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):
            self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    # 102 ProcedureIdentifier -> Identifier
    def procedureIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):
            self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    # 103 FunctionIdentifier -> Identifier   
    def functionIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):
            self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    # 104 BooleanExpression -> Expression
    def booleanExpression(self):
        if(self.lookahead in ["MP_LPAREN","MP_IDENTIFIER", "MP_PLUS", "MP_MINUS", "MP_NOT", "MP_FIXED"]):
            self.expression()
        else:
            self.error()
    
    # 105 OrdinalExpression -> Expression        
    def ordinalExpression(self): 
        if(self.lookahead in ["MP_LPAREN","MP_IDENTIFIER", "MP_PLUS", "MP_MINUS", "MP_NOT", "MP_FIXED"]):
            self.expression()
        else:
            self.error()
    
    # 106 IdentifierList -> Identifier IdentifierTail
    def identifierList(self): 
        if(self.lookahead == "MP_IDENTIFIER"):
            self.match("MP_IDENTIFIER")
            self.identifierTail()
        else:
            self.error()
    
    # 107 IdentifierTail -> "," Identifier IdentifierTail    
    # 108 IdentifierTail -> lambda
    def identifierTail(self): 
        if(self.lookahead == "MP_COMMA"):
            self.match("MP_COMMA")
            self.match("MP_IDENTIFIER")
            self.identifierTail()
        elif(self.lookahead == "MP_COLON"):
            return
        else:
            self.error()                               

    def error(self):
        print "Syntax error found on line " + str(self.scanner.getLineNumber()) + ", column " + str(self.scanner.getColumnNumber())
        sys.exit()