

class Parser(object):
    
    scanner = None
    lookahead = ''
    
    # Constructor
    def __init__(self, scanner):
        self.scanner = scanner

    def parse(self):    
        self.lookahead = self.scanner.getNextToken()
        self.systemGoal()

    def match(self, toMatch): 
        if(self.lookahead == toMatch):
            self.lookahead = self.scanner.getNextToken()
        else:
            self.error()
            
    # 1 SystemGoal -> Program eof
    def systemGoal(self):
        if self.lookahead is "MP_PROGRAM":
            self.program()
        else:
            self.error()
            
    # 2 Program -> ProgramHeading ";" Block "."
    def program(self):
        if self.lookahead is "MP_PROGRAM":
            self.programHeading()
            self.match("MP_SCOLON")
            self.block()
            self.match("MP_PERIOD")
        else:
            self.error()
    
    # 3 ProgramHeading -> "program" ProgramIdentifier
    def programHeading(self):
        if self.lookahead is "MP_PROGRAM":
            self.match("MP_PROGRAM")
            self.programIdentifier()
        else:
            self.error()
    
    # 4 Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart
    def block(self):
        if self.lookahead is "MP_VAR":
            self.variableDeclarationPart()
            self.procedureAndFunctionDeclarationPart()
            self.statementPart()
        else:
            self.error()
    
    
    # 5 VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
    def variableDeclarationPart(self):
        if self.lookahead is "MP_VAR":
            self.match("MP_VAR")
            self.variableDeclaration()
            self.match("MP_SCOLON")
            self.variableDeclarationTail()
        else:
            self.error()
    
    
    # 6 VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail 
    # 7 VariableDeclarationTail -> lambda
    def variableDeclarationTail(self):
        if self.lookahead in ["MP_PROCEDURE", "MP_FUNCTION", "MP_BEGIN"]:  # 7
            return
        elif self.lookahead is "MP_IDENTIFIER":  # 6
            self.variableDeclaration()
            self.match("MP_SCOLON")
            self.variableDeclarationTail()
        else:
            self.error()
    
    
    # 8 VariableDeclaration -> Identifierlist ":" Type  
    def variableDeclaration(self):
        if self.lookahead is "MP_IDENTIFIER":
            self.identifierList()
            self.match("MP_SCOLON")
            self.type()
        else:
            self.error()
    
    # 9   Type -> "Integer"
    # 10  Type -> "Float"
    # 11  Type -> "Boolean"
    def type(self):
        if self.lookahead is "MP_INTEGER":
            self.match("MP_INTEGER")
        elif self.lookahead is "MP_FLOAT":
            self.match("MP_FLOAT")
        #TODO: Boolean rule #11
        else:
            self.error()
    
    
    # 12 ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
    # 13 ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
    # 14 ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
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

    
    # 15 ProcedureDeclaration -> ProcedureHeading ";" Block ";"
    def procedureDeclaration(self): pass
    
    # 16 FunctionDeclaration  -> FunctionHeading ";" Block ";"       
    def functionDeclaration(self): pass
    
    # 17 ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
    def procedureHeading(self): pass
    
    # 18 FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList ":" Type
    def functionHeading(self): pass
    
    # 19 OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
    # 20 OptionalFormalParameterList -> lambda
    # 21 FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
    # 22 FormalParameterSectionTail -> lambda
    def optionalFormalParameterList(self): pass
    
    # 21 FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
    # 22 FormalParameterSectionTail -> lambda
    def formalParameterSectionTail(self): pass
    
    # 23 FormalParameterSection -> ValueParameterSection
    # 24 FormalParameterSection -> VariableParameterSection
    def formalParameterSection(self): pass
    
    # 25 ValueParameterSection -> IdentifierList ":" Type
    def valueParameterSection(self): pass
    
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
    def programIdentifier(self): pass
    
    # 101 VariableIdentifier -> Identifier
    def variableIdentifier(self): pass
    
    # 102 ProcedureIdentifier -> Identifier
    def procedureIdentifier(self): pass
    
    # 103 FunctionIdentifier -> Identifier   
    def functionIdentifier(self): pass
    
    # 104 BooleanExpression -> Expression
    def booleanExpression(self): pass
    
    # 105 OrdinalExpression -> Expression        
    def ordinalExpression(self): pass
    
    # 106 IdentifierList -> Identifier IdentifierTail
    def identifierList(self): pass
    
    # 107 IdentifierTail -> "," Identifier IdentifierTail    
    # 108 IdentifierTail -> lambda
    def identifierTail(self): pass

    def error(self):
        print "A parse error has been encountered"        
