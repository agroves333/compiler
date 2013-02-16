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
        print "The input program parses!"

    def match(self, toMatch): 
        if(self.lookahead == toMatch):
            self.lookahead = self.scanner.getNextToken()
        else:
            self.matchError(toMatch)
            
    
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
            self.match("MP_COLON")
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
    
    
    def variableParameterSection(self):
        if self.lookahead is 'MP_VAR':                      # 26 VariableParameterSection -> "var" IdentifierList ":" Type
            self.match('MP_VAR')
            self.identifierList();
            self.match('MP_COLON')
            self.type()
        else:
            self.error()
    
    
    def statementPart(self):
        if self.lookahead is 'MP_BEGIN':                    # 27 StatementPart -> CompoundStatement 
            self.compoundStatement()
        else:
            self.error()
        
    
    def compoundStatement(self):
        if self.lookahead is 'MP_BEGIN':                    # 28 CompoundStatement -> "begin" StatementSequence "end"
            self.match('MP_BEGIN')
            self.statementSequence()
            self.match('MP_END')
        else:
            self.error()
    
    
    def statementSequence(self):
        if self.lookahead in ['MP_SCOLON', 'MP_IDENTIFIER', # 29 StatementSequence -> Statement StatementTail
                              'MP_BEGIN', 'MP_END', 'MP_READ',
                              'MP_WRITE', 'MP_IF', 'MP_ELSE', 
                              'MP_REPEAT', 'MP_UNTIL', 'MP_WHILE', 
                              'MP_FOR']:
            self.statement()
            self.statementTail()
        else:
            self.error()
    
    
    def statementTail(self):
        if self.lookahead is 'MP_SCOLON':               # 30 StatementTail -> ";" Statement StatementTail
            self.match('MP_SCOLON')
            self.statement()
            self.statementTail()
        elif self.lookahead in ['MP_END', 'MP_UNTIL']:  # 31 StatementTail -> lambda
            return
        else:
            self.error()
    
    
    def statement(self):
        if self.lookahead in ['MP_SCOLON', 'MP_END', 'MP_ELSE']:    # 32 Statement -> EmptyStatement
            self.emptyStatement()
        elif self.lookahead is 'MP_BEGIN':                          # 33 Statement -> CompoundStatement 
            self.compoundStatement()
        elif self.lookahead is 'MP_READ':                           # 34 Statement -> ReadStatement
            self.readStatement()
        elif self.lookahead is 'MP_WRITE':                          # 35 Statement -> WriteStatement
            self.writeStatement()
        elif self.lookahead is 'MP_IDENTIFIER':                     # 36 Statement -> AssignmentStatement   OR  # 41 Statement -> ProcedureStatement
            self.assignmentStatement()
#            self.procedureStatement()
        elif self.lookahead is 'MP_IF':                             # 37 Statement -> IfStatement
            self.ifStatement()
        elif self.lookahead is 'MP_WHILE':                          # 38 Statement -> WhileStatement
            self.whileStatement()
        elif self.lookahead is 'MP_REPEAT':                         # 39 Statement -> RepeatStatement
            self.repeatStatement()
        elif self.lookahead is 'MP_FOR':                            # 40 Statement -> ForStatement
            self.forStatement()
        elif self.lookahead is 'MP_IDENTIFIER':                     # 41 Statement -> ProcedureStatement   OR  # 36 Statement -> AssignmentStatement
            self.procedureStatement()  
#            self.assignmentStatement()
        else:
            self.error()
    
    
    
    def emptyStatement(self):
        if self.lookahead in ['MP_SCOLON', 'MP_END',        # 42 EmptyStatement -> lambda
                              'MP_ELSE', 'MP_UNTIL']:
            return
        else:
            self.error()
    
    
    def readStatement(self):
        if self.lookahead is 'MP_READ':          # 43 ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
            self.match('MP_READ')
            self.match('MP_LPAREN')
            self.readParameter()
            self.readParameterTail()
            self.match('MP_RPAREN')
        else:
            self.error()
            
    
    def readParameterTail(self):
        if self.lookahead is 'MP_COMMA':        # 44 ReadParameterTail -> "," ReadParameter ReadParameterTail
            self.match('MP_COMMA')
            self.readParameter()
            self.readParameterTail()
        elif self.lookahead is 'MP_RPAREN':     # 45 ReadParameterTail -> lambda
            return
        else:
            self.error()
    
    
    def readParameter(self):
        if self.lookahead is 'MP_IDENTIFIER':   # 46 ReadParameter -> VariableIdentifier   
            self.variableIdentifier()
        else:
            self.error()
            
    
    def writeStatement(self):
        if self.lookahead is 'MP_WRITE':        # 47 WriteStatement -> "write" "(" WriteParameter WriteParameterTail ")"
            self.match('MP_WRITE')
            self.match('MP_LPAREN')
            self.writeParameter()
            self.writeParameterTail()
            self.match('MP_RPAREN')
        else:
            self.error()
      
    
    def writeParameterTail(self):
        if self.lookahead is 'MP_COMMA':        # 48 WriteParameterTail -> "," WriteParameter
            self.match('MP_COMMA')
            self.writeParameter()
        elif self.lookahead is 'MP_RPAREN':     # 49 WriteParameterTail -> lambda
            return
        else:
            self.error()
    
    
    def writeParameter(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',  # 50 WriteParameter -> OrdinalExpression    
                              'MP_PLUS', 'MP_MINUS',
                              'MP_NOT', 'MP_INTEGER_LIT']:
            self.ordinalExpression()
        else:
            self.error()
    
    
    def assignmentStatement(self):
        if self.lookahead is 'MP_IDENTIFIER':   # 51 AssignmentStatement -> VariableIdentifier ":=" Expression  OR
            self.variableIdentifier()
            self.match('MP_ASSIGN')
            self.expression()
        #This doesn't change parsing functionality
        #elif self.lookahead is 'MP_IDENTIFIER':   # 52 AssignmentStatement -> FunctionIdentifier ":=" Expression  
        #    self.functionIdentifier()
        #    self.match('MP_ASSIGN')
        #    self.expression()
        else:
            self.error()
            
            
    
    def ifStatement(self):
        if self.lookahead is 'MP_IF':           # 53 IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
            self.match('MP_IF')
            self.booleanExpression()
            self.match('MP_THEN')
            self.statement()
            self.optionalElsePart()
        else:
            self.error()
    
    
   
   
    def optionalElsePart(self):
        if self.lookahead is 'MP_ELSE':                               # 54 OptionalElsePart -> "else" Statement
            self.match('MP_ELSE')
            self.statement()
        elif self.lookahead in ['MP_SCOLON', 'MP_END', 'MP_UNTIL']:   # 55 OptionalElsePart -> lambda 
            return
        else:
            self.error()
            
    
                
    def repeatStatement(self):
        if self.lookahead is 'MP_REPEAT':           # 56 RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression
            self.match('MP_REPEAT')
            self.statementSequence()
            self.match('MP_UNTIL')
            self.booleanExpression()
        else:
            self.error()
            
    
    
    def whileStatement(self):
        if self.lookahead is 'MP_WHILE':            # 57 WhileStatement -> "while" BooleanExpression "do" Statement   
            self.match('MP_WHILE')
            self.booleanExpression()
            self.match('MP_DO')
            self.statement()
        else:
            self.error()
            
    
    
    def forStatement(self):
        if self.lookahead is 'MP_FOR':              # 58 ForStatement -> "for" ControlVariable ":=" InitialValue StepValue FinalValue "do" Statement
            self.match('MP_FOR')
            self.controlVariable()
            self.match('MP_ASSIGN')
            self.initialValue()
            self.stepValue()
            self.finalValue()
            self.match('MP_DO')
            self.statement()
        else:
            self.error()
            
    
    
    def controlVariable(self):
        if self.lookahead is 'MP_IDENTIFIER':       # 59 ControlVariable -> VariableIdentifier
            self.variableIdentifier()
        else:
            self.error()
            
    
    
    def initialValue(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',     # 60 InitialValue -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS',
                              'MP_NOT', 'MP_INTEGER_LIT']:
            self.ordinalExpression()
        else:
            self.error()
    
    
    
    def stepValue(self):
        if self.lookahead is 'MP_TO':               # 61 StepValue -> "to"
            self.match('MP_TO')
        elif self.lookahead is 'MP_DOWNTO':         # 62 StepValue -> "downto"
            self.match('MP_DOWNTO')
        else:
            self.error()
        
    
    
    def finalValue(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',     # 63 FinalValue -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS', 'MP_NOT',
                              'MP_INTEGER_LIT']:
            self.ordinalExpression()
        else:
            self.error()
            
    
    
    def procedureStatement(self):
        if self.lookahead is 'MP_IDENTIFIER':           # 64 ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
            self.procedureIdentifier()
            self.optionalActualParameterList()
        else:
            self.error()
    
    
    
    def optionalActualParameterList(self):
        if self.lookahead is 'MP_LPAREN':   # 65 OptionalActualParameterList -> "(" ActualParameter ActualParameterTail ")"    
            self.match('MP_LPAREN')
            self.actualParameter()
            self.actualParameterTail()
            self.match('MP_RPAREN')
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', 'MP_END', 'MP_COMMA',     # 66 OptionalActualParameterList -> lambda
                                'MP_THEN', 'MP_ELSE', 'MP_UNTIL', 'MP_TO',
                                'MP_DO', 'MP_DOWNTO', 'MP_EQUAL', 'MP_LTHAN',
                                'MP_GTHAN', 'MP_LEQUAL', 'MP_GEQUAL', 'MP_NEQUAL',
                                'MP_PLUS', 'MP_MINUS', 'MP_OR', 'MP_TIMES',
                                'MP_DIV', 'MP_MOD', 'MP_AND']:
            return
        else:
            self.error()
            
    
    
    
    def actualParameterTail(self):
        if self.lookahead is 'MP_COMMA':            # 67 ActualParameterTail -> "," ActualParameter ActualParameterTail    
            self.match('MP_COMMA')
            self.actualParameter()
            self.actualParameterTail()
        elif self.lookahead is 'MP_RPAREN':         # 68 ActualParameterTail -> lambda
            return
        else:
            self.error()
    
    
   
    def actualParameter(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',          # 69 ActualParameter -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS', 'MP_NOT', 
                              'MP_INTEGER_LIT']:
            self.ordinalExpression()
        else:
            self.error()
            
    
    
    def expression(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',          # 70 Expression -> SimpleExpression OptionalRelationalPart
                              'MP_PLUS', 'MP_MINUS', 'MP_NOT', 
                              'MP_INTEGER_LIT']:
            self.simpleExpression()
            self.optionalRelationalPart()
        else:
            self.error()
         
    
    
    def optionalRelationalPart(self):
        if self.lookahead in ['MP_EQUAL', 'MP_LTHAN',               # 71 OptionalRelationalPart -> RelationalOperator SimpleExpression    
                              'MP_GTHAN', 'MP_LEQUAL',
                              'MP_GEQUAL', 'MP_NEQUAL']:
            self.relationalOperator()
            self.simpleExpression()
        elif self.lookahead in ['MP_RPAREN', 'MP_END',              # 72 OptionalRelationalPart -> lambda
                                'MP_COMMA', 'MP_THEN',
                                'MP_ELSE', 'MP_UNTIL',
                                'MP_DO', 'MP_TO', 'MP_DOWNTO']:
            return
        else:
            self.error()    
        
    
       
    def relationalOperator(self):
        if self.lookahead is 'MP_EQUAL':        # 73 RelationalOperator -> "=" 
            self.match('MP_EQUAL')
        elif self.lookahead is 'MP_LTHAN':      # 74 RelationalOperator -> "<"
            self.match('MP_LTHAN')
        elif self.lookahead is 'MP_GTHAN':      # 75 RelationalOperator -> ">"    
            self.match('MP_GTHAN')
        elif self.lookahead is 'MP_LEQUAL':     # 76 RelationalOperator -> "<="  
            self.match('MP_LEQUAL')
        elif self.lookahead is 'MP_GEQUAL':     # 77 RelationalOperator -> ">="    
            self.match('MP_GEQUAL')
        elif self.lookahead is 'MP_NEQUAL':     # 78 RelationalOperator -> "<>"
            self.match('MP_NEQUAL')
        else:
            self.error()
            
    
    
    def simpleExpression(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',          # 79 SimpleExpression -> OptionalSign Term TermTail
                              'MP_PLUS', 'MP_MINUS', 'MP_NOT', 
                              'MP_INTEGER_LIT']:
            self.optionalSign()
            self.term()
            self.termTail()
        else:
            self.error()
            
    
     
    
    def termTail(self):
        if self.lookahead in ['MP_PLUS', 'MP_MINUS', 'MP_OR']:          # 80 TermTail -> AddingOperator Term TermTail   
            self.addingOperator()
            self.term()
            self.termTail()
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', 'MP_END',     # 81 TermTail -> lambda
                                'MP_COMMA', 'MP_THEN', 'MP_ELSE',
                                'MP_UNTIL', 'MP_DO', 'MP_TO',
                                'MP_DOWNTO', 'MP_EQUAL', 'MP_LTHAN',
                                'MP_GTHAN', 'MP_LEQUAL', 'MP_GEQUAL',
                                'MP_NEQUAL']:
            return
        else:
            self.error()
            
    
    
    def optionalSign(self):
        if self.lookahead is 'MP_PLUS':                         # 82 OptionalSign -> "+"  
            self.match('MP_PLUS')
        elif self.lookahead is 'MP_MINUS':                      # 83 OptionalSign -> "-"   
            self.match('MP_MINUS')
        elif self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',   # 84 OptionalSign -> lambda
                                'MP_NOT', 'MP_INTEGER_LIT']:
            return
        else:
            self.error()
    
    
    
    def addingOperator(self):
        if self.lookahead is 'MP_PLUS':     # 85 AddingOperator -> "+" 
            self.match('MP_PLUS')
        elif self.lookahead is 'MP_MINUS':  # 86 AddingOperator -> "-"   
            self.match('MP_MINUS')
        elif self.lookahead is 'MP_OR':     # 87 AddingOperator -> "or"
            self.match('MP_OR')
        else:
            self.error()
            
    
    
    def term(self):
        if self.lookahead in ['MP_SCOLON', 'MP_RPAREN',     # 88 Term -> Factor FactorTail    
                           'MP_IDENTIFIER', 'MP_NOT',
                           'MP_INTEGER_LIT']:
            self.factor()
            self.factorTail()
        else:
            self.error()
            
            
    
    def factorTail(self):
        if self.lookahead in ['MP_TIMES', 'MP_DIV',                     # 89 FactorTail -> MultiplyingOperator Factor FactorTail    
                              'MP_MOD', 'MP_AND']:
            self.multiplyingOperator()
            self.factor()
            self.factorTail()
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', 'MP_END',      # 90 FactorTail -> lambda
                                'MP_COMMA', 'MP_THEN', 'MP_ELSE', 
                                'MP_UNTIL', 'MP_DO', 'MP_TO', 'MP_DOWNTO',
                                'MP_EQUAL', 'MP_LTHAN', 'MP_GTHAN',
                                'MP_LEQUAL', 'MP_GEQUAL', 'MP_NEQUAL',
                                'MP_PLUS', 'MP_MINUS', 'MP_OR']:
            return
        else:
            self.error()
            
            
            
    def multiplyingOperator(self): 
        if self.lookahead is 'MP_TIMES':    # 91 MultiplyingOperator  -> "*"   
            self.match('MP_TIMES')
        elif self.lookahead is 'MP_DIV':    # 92 MultiplyingOperator  -> "div"    
            self.match('MP_DIV')
        elif self.lookahead is 'MP_MOD':    # 93 MultiplyingOperator  -> "mod"   
            self.match('MP_MOD')
        elif self.lookahead is 'MP_AND':    # 94 MultiplyingOperator  -> "and"
            self.match('MP_AND')
        else:
            self.error()
            
    
    
    def factor(self):
        if self.lookahead in ['MP_INTEGER_LIT']:    # 95 Factor -> UnsignedInteger
            self.match('MP_INTEGER_LIT')
        elif self.lookahead is 'MP_IDENTIFIER':     # 96 Factor -> VariableIdentifier  OR  # 99 Factor -> FunctionIdentifier OptionalActualParameterList
            self.variableIdentifier()
#            self.functionIdentifier()
#            self.optionalActualParameterList()
        elif self.lookahead is 'MP_NOT':            # 97 Factor -> "not" Factor    
            self.match('MP_NOT');
            self.factor()
        elif self.lookahead is 'MP_LPAREN':         # 98 Factor -> "(" Expression ")"  
            self.match('MP_LPAREN')
            self.expression()
            self.match('MP_RPAREN')
    
    
    
    def programIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 100 ProgramIdentifier -> Identifier
            self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    
    def variableIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 101 VariableIdentifier -> Identifier
            self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    
    def procedureIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 102 ProcedureIdentifier -> Identifier
            self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    
    def functionIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 103 FunctionIdentifier -> Identifier   
            self.match("MP_IDENTIFIER")
        else:
            self.error()
    
   
    def booleanExpression(self):
        if(self.lookahead in ["MP_LPAREN","MP_IDENTIFIER", "MP_PLUS", "MP_MINUS", "MP_NOT", "MP_INTEGER_LIT"]):  # 104 BooleanExpression -> Expression
            self.expression()
        else:
            self.error()
    
      
    def ordinalExpression(self): 
        if(self.lookahead in ["MP_LPAREN","MP_IDENTIFIER", "MP_PLUS", "MP_MINUS", "MP_NOT", "MP_INTEGER_LIT"]): # 105 OrdinalExpression -> Expression      
            self.expression()
        else:
            self.error()
    
    
    def identifierList(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 106 IdentifierList -> Identifier IdentifierTail
            self.match("MP_IDENTIFIER")
            self.identifierTail()
        else:
            self.error()
    
     
    
    def identifierTail(self): 
        if(self.lookahead == "MP_COMMA"):       # 107 IdentifierTail -> "," Identifier IdentifierTail   
            self.match("MP_COMMA")
            self.match("MP_IDENTIFIER")
            self.identifierTail()
        elif(self.lookahead == "MP_COLON"):     # 108 IdentifierTail -> lambda
            return
        else:
            self.error()                               

    def error(self):
        print "Syntax error found on line " + str(self.scanner.getLineNumber()) + ", column " + str(self.scanner.getColumnNumber())
        sys.exit()
        
    def matchError(self, expected):
        print "Match error found on line " + str(self.scanner.getLineNumber()) + ", column " + str(self.scanner.getColumnNumber())
        print "Found " + self.lookahead + " when expected " + expected
        sys.exit()
