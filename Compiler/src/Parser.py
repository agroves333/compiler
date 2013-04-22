import sys
# import inspect

from SymbolTable import SymbolTable
from Scanner import Scanner

class Parser(object):

    scanner = None
    analyzer = None
    sourceFile = None
    symbolTableStack = []
    lookahead = ''
    label = 0
    
    
    # Constructor
    def __init__(self, fileName):
        try:
            self.sourceFile = open(fileName, 'r')
        except IOError:
            sys.exit("Source file not found")

        self.scanner = Scanner(self.sourceFile)
        self.analyzer = Analyzer(fileName)

    def parse(self):
        self.lookahead = self.scanner.getNextToken()
        self.systemGoal()
        print "Parsing Successful"
        self.sourceFile.close()

    def match(self, toMatch):
        lexeme = self.scanner.lexeme
        if(self.lookahead == toMatch):
            self.lookahead = self.scanner.getNextToken()            
            return lexeme
        else:
            # print the caller
#            print inspect.stack()[1][3]
            self.matchError(toMatch)
           
    def systemGoal(self):
        if self.lookahead is "MP_PROGRAM":  # 1 SystemGoal -> Program eof
            self.program()
        else:
            self.error()
            
    
    def program(self):
        if self.lookahead is "MP_PROGRAM":  # 2 Program -> ProgramHeading ";" Block "."
            self.programHeading()
            self.match("MP_SCOLON")
            self.block()
            self.match("MP_PERIOD")
        else:
            self.error()
    
    
    def programHeading(self):
        if self.lookahead is "MP_PROGRAM":  # 3 ProgramHeading -> "program" ProgramIdentifier
            self.match("MP_PROGRAM")
            self.programIdentifier()
            self.push('Main')
            self.analyzer.genBranch(self.label)
            self.label = self.label + 1
        else:
            self.error()
    
    
    def block(self):
        if self.lookahead in ["MP_VAR", "MP_BEGIN", "MP_FUNCTION", "MP_PROCEDURE"]:  # 4 Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart
            self.variableDeclarationPart()
            self.procedureAndFunctionDeclarationPart()
            self.statementPart()
        else:
            self.error()
    
    
    def variableDeclarationPart(self):
        if self.lookahead is "MP_VAR":  # 5 VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
            self.match("MP_VAR")
            self.variableDeclaration()
            self.match("MP_SCOLON")
            self.variableDeclarationTail()

        elif self.lookahead in ["MP_BEGIN", "MP_FUNCTION", "MP_PROCEDURE"]:
            return
        else:
            self.error()
    
    
    def variableDeclarationTail(self):
        if self.lookahead in ["MP_PROCEDURE", "MP_FUNCTION", "MP_BEGIN"]:  # 7 VariableDeclarationTail -> lambda
            return
        elif self.lookahead is "MP_IDENTIFIER":  # 6 VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail 
            self.variableDeclaration()
            self.match("MP_SCOLON")
            self.variableDeclarationTail()
        else:
            self.error()
    
    
    
    def variableDeclaration(self):
        if self.lookahead is "MP_IDENTIFIER":  # 8 VariableDeclaration -> IdentifierList ":" Type  
            idList = self.identifierList()
            self.match("MP_COLON")
            varType = self.type()
            for name in idList:
                self.insertEntry(name, 'var', varType)
        else:
            self.error()
    
    
    def type(self):
        if self.lookahead is "MP_INTEGER":  # 9   Type -> "Integer"
            self.match("MP_INTEGER")
            return 'Integer'
        elif self.lookahead is "MP_FLOAT":  # 108  Type -> "Float"
            self.match("MP_FLOAT")
            return 'Float'
        elif self.lookahead is "MP_STRING":  # 109  Type -> "String"
            self.match("MP_STRING")
            return 'String'
        elif self.lookahead is "MP_BOOLEAN":  # 110  Type -> "Boolean"
            self.match("MP_BOOLEAN")
            return 'Boolean'
        else:
            self.error()
    
    
    def procedureAndFunctionDeclarationPart(self):
        if self.lookahead is "MP_PROCEDURE":  # 10 ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
            self.procedureDeclaration()
            self.procedureAndFunctionDeclarationPart()
        elif self.lookahead is "MP_FUNCTION":  # 11 ProcedureAndFunctionDeclarationPart -> FunctionDeclaration ProcedureAndFunctionDeclarationPart
            self.functionDeclaration()
            self.procedureAndFunctionDeclarationPart()
        elif self.lookahead is "MP_BEGIN":  # 12 ProcedureAndFunctionDeclarationPart -> lambda
            return
        else:
            self.error()

    
    def procedureDeclaration(self):
        if self.lookahead is "MP_PROCEDURE":  # 13 ProcedureDeclaration -> ProcedureHeading ";" Block ";"
            self.procedureHeading();
            self.match('MP_SCOLON')
            self.block()
            self.match('MP_SCOLON')
        else:
            self.error()
    
          
    def functionDeclaration(self):
        if self.lookahead is "MP_FUNCTION":  # 14 FunctionDeclaration  -> FunctionHeading ";" Block ";"
            self.functionHeading()
            self.match("MP_SCOLON");
            self.block()
            self.match("MP_SCOLON")
        else:
            self.error()
    
    
    def procedureHeading(self):
        if self.lookahead is "MP_PROCEDURE":  # 15 ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
            self.match("MP_PROCEDURE")
            name = self.procedureIdentifier()
            self.insertEntry(name, 'procedure')
            self.push(name)
            self.analyzer.genLabel(self.label)
            self.label = self.label + 1
            self.optionalFormalParameterList()
        else:
            self.error()
    
    
    def functionHeading(self):
        if self.lookahead is "MP_FUNCTION":  # 16 FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList ":" Type
            self.match("MP_FUNCTION")
            name = self.functionIdentifier()
            self.insertEntry(name, 'function')
            self.push(name)
            self.optionalFormalParameterList()
            self.match("MP_COLON")
            self.type()
        else:
            self.error()
    
    
    
    def optionalFormalParameterList(self):
        if self.lookahead is 'MP_LPAREN':  # 17 OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
            self.match('MP_LPAREN')
            self.formalParameterSection()
            self.formalParameterSectionTail()
            self.match('MP_RPAREN')
            
        elif self.lookahead in ['MP_COLON', 'MP_SCOLON', 'MP_INTEGER', 'MP_FLOAT', 'MP_BOOLEAN', 'MP_STRING']:  # 18 OptionalFormalParameterList -> lambda
            return
        else:
            self.error
       
    
    def formalParameterSectionTail(self):
        if self.lookahead is "MP_SCOLON":  # 19 FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
            self.match('MP_SCOLON')
            self.formalParameterSection()
            self.formalParameterSectionTail()
        elif self.lookahead is 'MP_RPAREN':  # 20 FormalParameterSectionTail -> lambda
            return 
        else:
            self.error
    
    
    
    def formalParameterSection(self):
        if self.lookahead is 'MP_IDENTIFIER':  # 21 FormalParameterSection -> ValueParameterSection
            self.valueParameterSection()
        elif self.lookahead is 'MP_VAR':  # 22 FormalParameterSection -> VariableParameterSection
            self.variableParameterSection()
        else:
            self.error()
    
    
    def valueParameterSection(self):
        if self.lookahead is 'MP_IDENTIFIER':  # 23 ValueParameterSection -> IdentifierList ":" Type
            identList = []
            identList = self.identifierList();
            self.match('MP_COLON')
            varType = self.type()
            for name in identList:
                self.insertEntry(name, 'var', varType)
        else:
            self.error()
    
    
    def variableParameterSection(self):
        if self.lookahead is 'MP_VAR':  # 24 VariableParameterSection -> "var" IdentifierList ":" Type
            self.match('MP_VAR')
            identList = []
            identList = self.identifierList();
            self.match('MP_COLON')
            varType = self.type()
            for name in identList:
                self.insertEntry(name, 'var', varType)
            
        else:
            self.error()
    
    
    def statementPart(self):
        if self.lookahead is 'MP_BEGIN':  # 25 StatementPart -> CompoundStatement
            self.compoundStatement()
        else:
            self.error()
        
    
    def compoundStatement(self):
        if self.lookahead is 'MP_BEGIN':  # 26 CompoundStatement -> "begin" StatementSequence "end"
            self.match('MP_BEGIN')
            self.analyzer.genIncreaseStack(self.symbolTableStack[-1].size)
            self.statementSequence()
            self.match('MP_END')
#             self.printTableStack()
            self.analyzer.genDecreaseStack(self.symbolTableStack[-1].size)
            self.symbolTableStack.pop()
        else:
            self.error()
    
    
    def statementSequence(self):
        if self.lookahead in ['MP_SCOLON', 'MP_IDENTIFIER',  # 27 StatementSequence -> Statement StatementTail
                              'MP_BEGIN', 'MP_END', 'MP_READ',
                              'MP_WRITE', 'MP_IF', 'MP_ELSE',
                              'MP_REPEAT', 'MP_UNTIL', 'MP_WHILE',
                              'MP_FOR', 'MP_WRITELN']:
            self.statement()
            self.statementTail()
        else:
            self.error()
    
    
    def statementTail(self):
        if self.lookahead is 'MP_SCOLON':  # 28 StatementTail -> ";" Statement StatementTail
            self.match('MP_SCOLON')
            self.statement()
            self.statementTail()
        elif self.lookahead in ['MP_END', 'MP_UNTIL']:  # 29 StatementTail -> lambda
            return
        else:
            self.error()
    
    
    def statement(self):
        if self.lookahead in ['MP_SCOLON', 'MP_END', 'MP_ELSE', 'MP_UNTIL']:  # 30 Statement -> EmptyStatement
            self.emptyStatement()
        elif self.lookahead is 'MP_BEGIN':  # 31 Statement -> CompoundStatement
            self.compoundStatement()
        elif self.lookahead is 'MP_READ':  # 32 Statement -> ReadStatement
            self.readStatement()
        elif self.lookahead in ['MP_WRITE', 'MP_WRITELN']:  # 33 Statement -> WriteStatement
            self.writeStatement()
        elif self.lookahead is 'MP_IDENTIFIER':  # 39 Statement -> ProcedureStatement   OR  # 34 Statement -> AssignmentStatement
            # if MP_ASSIGN is second lookahead, go to AssignStatement, else go to ProcedureStatement
            second_lookahead = self.scanner.peekNextToken()
            if second_lookahead is 'MP_ASSIGN':
                self.assignmentStatement()
            else:
                self.procedureStatement()
        elif self.lookahead is 'MP_IF':  # 35 Statement -> IfStatement
            self.ifStatement()
        elif self.lookahead is 'MP_WHILE':  # 36 Statement -> WhileStatement
            self.whileStatement()
        elif self.lookahead is 'MP_REPEAT':  # 37 Statement -> RepeatStatement
            self.repeatStatement()
        elif self.lookahead is 'MP_FOR':  # 28 Statement -> ForStatement
            self.forStatement()
        else:
            self.error()
    
    
    
    def emptyStatement(self):
        if self.lookahead in ['MP_SCOLON', 'MP_END',  # 40 EmptyStatement -> lambda
                              'MP_ELSE', 'MP_UNTIL']:
            return
        else:
            self.error()
    
    
    def readStatement(self):
        if self.lookahead is 'MP_READ':  # 41 ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
            self.match('MP_READ')
            self.match('MP_LPAREN')
            self.readParameter()
            self.readParameterTail()
            self.match('MP_RPAREN')
        else:
            self.error()
            
    
    def readParameterTail(self):
        if self.lookahead is 'MP_COMMA':  # 42 ReadParameterTail -> "," ReadParameter ReadParameterTail
            self.match('MP_COMMA')
            self.readParameter()
            self.readParameterTail()
        elif self.lookahead is 'MP_RPAREN':  # 43 ReadParameterTail -> lambda
            return
        else:
            self.error()
    
    
    def readParameter(self):
        if self.lookahead is 'MP_IDENTIFIER':  # 44 ReadParameter -> VariableIdentifier
            id = self.variableIdentifier()
            identRec = self.analyzer.processId(id)
            self.analyzer.genRead(identRec)
        else:
            self.error()
            
    
    def writeStatement(self):
        if self.lookahead is 'MP_WRITE':  # 45 WriteStatement -> "write" "(" WriteParameter WriteParameterTail ")"
            self.match('MP_WRITE')
            self.match('MP_LPAREN')
            self.writeParameter()
            self.writeParameterTail()          
            self.match('MP_RPAREN')
        elif self.lookahead is 'MP_WRITELN': # 111 WriteStatement -> writeln "(" WriteParameter WriteParameterTail ")"
            self.match('MP_WRITELN')
            self.match('MP_LPAREN')
            self.writeParameter()
            self.writeParameterTail()
            self.analyzer.genWriteln()
            self.match('MP_RPAREN')
        else:
            self.error()
      
    
    def writeParameterTail(self):
        if self.lookahead is 'MP_COMMA':  # 46 WriteParameterTail -> "," WriteParameter
            self.match('MP_COMMA')
            self.writeParameter()
        elif self.lookahead is 'MP_RPAREN':  # 47 WriteParameterTail -> lambda
            return
        else:
            self.error()
    
    
    def writeParameter(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',  # 48 WriteParameter -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            self.ordinalExpression()
            self.analyzer.genWrite()
        else:
            self.error()
    
    
    def assignmentStatement(self):
        # semantic records
        expressionRec = {"type":''}
        identRec = {"name":''}
        
        if self.lookahead is 'MP_IDENTIFIER':  # 49 AssignmentStatement -> VariableIdentifier ":=" Expression  OR
            
            id = self.variableIdentifier()
            identRec = self.analyzer.processId(id)
            self.match('MP_ASSIGN')
            expressionRec["type"] = self.expression()
            self.analyzer.genAssign(identRec, expressionRec)
            
        # This doesn't change parsing functionality
        # elif self.lookahead is 'MP_IDENTIFIER':   # 50 AssignmentStatement -> FunctionIdentifier ":=" Expression
        #    self.functionIdentifier()
        #    self.match('MP_ASSIGN')
        #    self.expression()
        else:
            self.error()
            
            
    
    def ifStatement(self):
        if self.lookahead is 'MP_IF':  # 51 IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
            self.match('MP_IF')
            self.booleanExpression()
            self.match('MP_THEN')
            self.statement()
            self.optionalElsePart()
        else:
            self.error()
    
    
   
   
    def optionalElsePart(self):
        #TODO: Table says else is ambiguous? haven't looked at it yet
        if self.lookahead is 'MP_ELSE':  # 52 OptionalElsePart -> "else" Statement
            self.match('MP_ELSE')
            self.statement()
        elif self.lookahead in ['MP_SCOLON', 'MP_END', 'MP_UNTIL']:  # 53 OptionalElsePart -> lambda
            return
        else:
            self.error()
            
    
                
    def repeatStatement(self):
        if self.lookahead is 'MP_REPEAT':  # 54 RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression
            self.match('MP_REPEAT')
            self.statementSequence()
            self.match('MP_UNTIL')
            self.booleanExpression()
        else:
            self.error()
            
    
    
    def whileStatement(self):
        if self.lookahead is 'MP_WHILE':  # 55 WhileStatement -> "while" BooleanExpression "do" Statement
            self.match('MP_WHILE')
            self.booleanExpression()
            self.match('MP_DO')
            self.statement()
        else:
            self.error()
            
    
    
    def forStatement(self):
        if self.lookahead is 'MP_FOR':  # 56 ForStatement -> "for" ControlVariable ":=" InitialValue StepValue FinalValue "do" Statement
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
        if self.lookahead is 'MP_IDENTIFIER':  # 57 ControlVariable -> VariableIdentifier
            self.variableIdentifier()
        else:
            self.error()

    
    def initialValue(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',  # 58 InitialValue -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            self.ordinalExpression()
        else:
            self.error()
    
    
    
    def stepValue(self):
        if self.lookahead is 'MP_TO':  # 59 StepValue -> "to"
            self.match('MP_TO')
        elif self.lookahead is 'MP_DOWNTO':  # 60 StepValue -> "downto"
            self.match('MP_DOWNTO')
        else:
            self.error()
        
    
    
    def finalValue(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',  # 61 FinalValue -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT'
                              'MP_NOT', 'MP_INTEGER_LIT'
                              'MP_TRUE', 'MP_FALSE']:
            self.ordinalExpression()
        else:
            self.error()
            
    
    
    def procedureStatement(self):
        if self.lookahead is 'MP_IDENTIFIER':  # 62 ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
            self.procedureIdentifier()
            self.optionalActualParameterList()
        else:
            self.error()
    
    
    
    def optionalActualParameterList(self):
        if self.lookahead is 'MP_LPAREN':  # 63 OptionalActualParameterList -> "(" ActualParameter ActualParameterTail ")"
            self.match('MP_LPAREN')
            self.actualParameter()
            self.actualParameterTail()
            self.match('MP_RPAREN')
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', 'MP_END', 'MP_COMMA',  # 64 OptionalActualParameterList -> lambda
                                'MP_THEN', 'MP_ELSE', 'MP_UNTIL', 'MP_TO',
                                'MP_DO', 'MP_DOWNTO', 'MP_EQUAL', 'MP_LTHAN',
                                'MP_GTHAN', 'MP_LEQUAL', 'MP_GEQUAL', 'MP_NEQUAL',
                                'MP_PLUS', 'MP_MINUS', 'MP_OR', 'MP_TIMES',
                                'MP_DIV', 'MP_MOD', 'MP_AND', 'MP_SLASH']:
            return
        else:
            self.error()
            
    
    
    def actualParameterTail(self):
        if self.lookahead is 'MP_COMMA':  # 65 ActualParameterTail -> "," ActualParameter ActualParameterTail
            self.match('MP_COMMA')
            self.actualParameter()
            self.actualParameterTail()
        elif self.lookahead is 'MP_RPAREN':  # 66 ActualParameterTail -> lambda
            return
        else:
            self.error()
    
    
   
    def actualParameter(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',   # 67 ActualParameter -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            self.ordinalExpression()
        else:
            self.error()
            
    
    
    def expression(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',   # 68 Expression -> SimpleExpression OptionalRelationalPart
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            self.simpleExpression()
            self.optionalRelationalPart()
#             return self.mapTokenToType(self.lookahead)
        else:
            self.error()
         
    
    
    def optionalRelationalPart(self):
        if self.lookahead in ['MP_EQUAL', 'MP_LTHAN',  # 69 OptionalRelationalPart -> RelationalOperator SimpleExpression
                              'MP_GTHAN', 'MP_LEQUAL',
                              'MP_GEQUAL', 'MP_NEQUAL']:
            self.relationalOperator()
            self.simpleExpression()
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', # 70 OptionalRelationalPart -> lambda
                                'MP_END', 'MP_COMMA',
                                'MP_THEN', 'MP_ELSE',
                                'MP_UNTIL','MP_DO', 
                                'MP_TO', 'MP_DOWNTO']:
            return
        else:
            self.error()    
        
    
       
    def relationalOperator(self):
        if self.lookahead is 'MP_EQUAL':  # 71 RelationalOperator -> "="
            self.match('MP_EQUAL')
        elif self.lookahead is 'MP_LTHAN':  # 72 RelationalOperator -> "<"
            self.match('MP_LTHAN')
        elif self.lookahead is 'MP_GTHAN':  # 73 RelationalOperator -> ">"
            self.match('MP_GTHAN')
        elif self.lookahead is 'MP_LEQUAL':  # 74 RelationalOperator -> "<="
            self.match('MP_LEQUAL')
        elif self.lookahead is 'MP_GEQUAL':  # 75 RelationalOperator -> ">="
            self.match('MP_GEQUAL')
        elif self.lookahead is 'MP_NEQUAL':  # 76 RelationalOperator -> "<>"
            self.match('MP_NEQUAL')
        else:
            self.error()
            
    
    
    def simpleExpression(self):
        # semantic records
        termRec = {}
        termTailRec = {}
        
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',   # 77 SimpleExpression -> OptionalSign Term TermTail
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            
            self.optionalSign()
            termRec = self.term()
            termTailRec = termRec
#             print termTailRec
            termTailRec["type"] = self.termTail(termTailRec)
            expressionRec = termTailRec     # This seems absolutely retarded but it's what Rocky suggested
            return expressionRec
        else:
            self.error()
            
    
    
    def termTail(self, termTailRec = {}):
        # Semantic Records
        addopRec = {}
        termRec = {}
        
        if self.lookahead in ['MP_PLUS', 'MP_MINUS', 'MP_OR']:  # 78 TermTail -> AddingOperator Term TermTail
            addopRec["lexeme"] = self.addingOperator()
            termRec = self.term()
            print termTailRec
#             print addopRec
#             print termRec 
            resultRec = self.analyzer.genArithmetic(termTailRec, addopRec, termRec)
            
            self.termTail(resultRec)
            termTailRec = resultRec
            
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', 'MP_END',  # 79 TermTail -> lambda
                                'MP_COMMA', 'MP_THEN', 'MP_ELSE',
                                'MP_UNTIL', 'MP_DO', 'MP_TO',
                                'MP_DOWNTO', 'MP_EQUAL', 'MP_LTHAN',
                                'MP_GTHAN', 'MP_LEQUAL', 'MP_GEQUAL',
                                'MP_NEQUAL']:
            return
        else:
            self.error()
            
    
    
    def optionalSign(self):
        if self.lookahead is 'MP_PLUS':  # 80 OptionalSign -> "+"
            self.match('MP_PLUS')
        elif self.lookahead is 'MP_MINUS':  # 81 OptionalSign -> "-"
            self.match('MP_MINUS')
        elif self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',  # 82 OptionalSign -> lambda
                                'MP_NOT', 'MP_INTEGER_LIT',
                                'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                                'MP_TRUE', 'MP_FALSE']:
            return
        else:
            self.error()
    
    
    
    def addingOperator(self):
        if self.lookahead is 'MP_PLUS':  # 83 AddingOperator -> "+"
            return self.match('MP_PLUS')
        elif self.lookahead is 'MP_MINUS':  # 84 AddingOperator -> "-"
            return self.match('MP_MINUS')
        elif self.lookahead is 'MP_OR':  # 85 AddingOperator -> "or"
            return self.match('MP_OR')
        else:
            self.error()
            
    
    
    def term(self):
        termRec = {}
        
        if self.lookahead in ['MP_LPAREN',  # 86 Term -> Factor FactorTail
                           'MP_IDENTIFIER', 'MP_NOT',
                           'MP_INTEGER_LIT', 'MP_FLOAT_LIT', 'MP_FIXED_LIT',
                           'MP_STRING_LIT', 'MP_TRUE',
                           'MP_FALSE']:
            
            termRec["type"] = self.factor()
            self.factorTail()
            return termRec
#             return self.mapTokenToType(self.lookahead)
        else:
            self.error()
            
            
    
    def factorTail(self):
        if self.lookahead in ['MP_TIMES', 'MP_DIV',  # 87 FactorTail -> MultiplyingOperator Factor FactorTail
                              'MP_MOD', 'MP_AND', 'MP_SLASH']:
            self.multiplyingOperator()
            self.factor()
            self.factorTail()
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', 'MP_END',  # 88 FactorTail -> lambda
                                'MP_COMMA', 'MP_THEN', 'MP_ELSE',
                                'MP_UNTIL', 'MP_DO', 'MP_TO', 'MP_DOWNTO',
                                'MP_EQUAL', 'MP_LTHAN', 'MP_GTHAN',
                                'MP_LEQUAL', 'MP_GEQUAL', 'MP_NEQUAL',
                                'MP_PLUS', 'MP_MINUS', 'MP_OR']:
            return
        else:
            self.error()
            
            
            
    def multiplyingOperator(self): 
        if self.lookahead is 'MP_TIMES':    # 89 MultiplyingOperator  -> "*"
            self.match('MP_TIMES')
        elif self.lookahead is 'MP_DIV':    # 90 MultiplyingOperator  -> "div"
            self.match('MP_DIV')
        elif self.lookahead is 'MP_MOD':    # 91 MultiplyingOperator  -> "mod"
            self.match('MP_MOD')
        elif self.lookahead is 'MP_AND':    # 92 MultiplyingOperator  -> "and"
            self.match('MP_AND')
        elif self.lookahead is 'MP_SLASH':  # 112 MultiplyingOperator -> "/"
            self.match('MP_SLASH')
        else:
            self.error()
            
    
    
    def factor(self):
        # semntic record
        identRec = {}
        
        if self.lookahead in ['MP_INTEGER_LIT']:  # 93 Factor -> UnsignedInteger
            integer = self.match('MP_INTEGER_LIT')
            self.analyzer.genPushInt(integer)
            return "Integer"
        elif self.lookahead is 'MP_IDENTIFIER':  # 94 Factor -> VariableIdentifier  OR  # 97 Factor -> FunctionIdentifier OptionalActualParameterList
            id_kind = self.analyzer.processId(self.scanner.lexeme)["kind"]
            if id_kind == "function":
                id = self.functionIdentifier()
            elif id_kind == "var":
                id = self.variableIdentifier()
                
                identRec["lexeme"] = id
                self.analyzer.genPushId(identRec)
                
            self.optionalActualParameterList()
            return self.analyzer.processId(id)["type"]
        
        elif self.lookahead is 'MP_NOT':  # 95 Factor -> "not" Factor
            self.match('MP_NOT');
            self.factor()
        elif self.lookahead is 'MP_LPAREN':  # 96 Factor -> "(" Expression ")"
            self.match('MP_LPAREN')
            self.expression()
            self.match('MP_RPAREN')
        elif self.lookahead in ['MP_FLOAT_LIT']:  # 113 Factor -> UnsignedFloat
            float = self.match('MP_FLOAT_LIT')
            self.analyzer.genPushFloat(float)
            return "Float"
        elif self.lookahead in ['MP_FIXED_LIT']:  # 113 Factor -> UnsignedFloat
            fixed = self.match('MP_FIXED_LIT')
            self.analyzer.genPushFloat(fixed)
        elif self.lookahead in ['MP_STRING_LIT']:  # 114 Factor -> StringLiteral
            string = self.match('MP_STRING_LIT')
            self.analyzer.genPushString(string)
        elif self.lookahead in ['MP_TRUE']:  # 115 Factor -> "True"
            self.match('MP_TRUE')
        elif self.lookahead in ['MP_FALSE']:  # 116 Factor -> "False"
            self.match('MP_FALSE')


    def programIdentifier(self):
        if(self.lookahead == "MP_IDENTIFIER"):  # 98 ProgramIdentifier -> Identifier
            return self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    
    def variableIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 99 VariableIdentifier -> Identifier
            return self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    
    def procedureIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 100 ProcedureIdentifier -> Identifier
            return self.match("MP_IDENTIFIER")
        else:
            self.error()
    
    
    def functionIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 101 FunctionIdentifier -> Identifier
            return self.match("MP_IDENTIFIER")
        else:
            self.error()
    
   
    def booleanExpression(self):
        if(self.lookahead in ["MP_LPAREN", "MP_IDENTIFIER",   # 102 BooleanExpression -> Expression
                              "MP_PLUS", "MP_MINUS",
                              "MP_NOT", "MP_INTEGER_LIT",
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT',
                              'MP_STRING_LIT', 'MP_TRUE',
                              'MP_FALSE']):
            self.expression()
        else:
            self.error()
    
      
    def ordinalExpression(self):
        if(self.lookahead in ["MP_LPAREN", "MP_IDENTIFIER",   # 103 OrdinalExpression -> Expression
                              "MP_PLUS", "MP_MINUS",
                              "MP_NOT", "MP_INTEGER_LIT",
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT',
                              'MP_STRING_LIT', 'MP_TRUE',
                              'MP_FALSE']):
            self.expression()
        else:
            self.error()
    
    
    def identifierList(self):
        if(self.lookahead == "MP_IDENTIFIER"):  # 104 IdentifierList -> Identifier IdentifierTail
            ident = []
            ident.append(self.scanner.lexeme)
            self.match("MP_IDENTIFIER")
            self.identifierTail(ident)
            return ident
        else:
            self.error()
    
     
     
    def identifierTail(self,ident): 
        if(self.lookahead == "MP_COMMA"):  # 105 IdentifierTail -> "," Identifier IdentifierTail
            self.match("MP_COMMA")
            ident.append(self.scanner.lexeme)
            self.match("MP_IDENTIFIER")
            self.identifierTail(ident)
        elif(self.lookahead == "MP_COLON"):  # 106 IdentifierTail -> lambda
            return
        else:
            self.error()                               

    def error(self):
        print "Syntax error found on line " + str(self.scanner.getLineNumber()) + ", column " + str(self.scanner.getColumnNumber())
        # print the caller
#         print inspect.stack()[1][3]
        sys.exit()
        
    def matchError(self, expected):
        print "Match error found on line " + str(self.scanner.getLineNumber()) + ", column " + str(self.scanner.getColumnNumber()) + " lexeme: " + self.scanner.lexeme
        print "Found " + self.lookahead + " when expected " + expected
        # print the caller
        sys.exit()
        
 
    
    def printTableStack(self):
        table = self.symbolTableStack[len(self.symbolTableStack)-1]
        print '{0:1s}{1:=<67}{0:1s}'.format('+', '=')
        print '{0:<1s} {1:10s} {2:10s} {3:<10s} {4:32s} {0:>1s}'.format('|', table.name +"  "+ table.label, 'Nest: '+ str(table.nest), 'Size: '+ str(table.size), 'Next-> '+ str(table.next))
        print '{0:1s}{1:=<67}{0:1s}'.format('+', '=')
        print '{0:<1s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {0:<1s}'.format('|', 'Name', 'Kind', 'Type', 'Size', 'Offset', 'Label')
        print '{0:1s}{1:-<67}{0:1s}'.format('+', '-')
        for entry in table.entries:
            print '{0:<1s} {1:10s} {2:10s} {3:10s} {4:<10d} {5:<10d} {6:10s} {0:<1s}'.format('|', entry['name'], entry['kind'], entry['type'], entry['size'], entry['offset'], entry['label'])
        print '{0:1s}{1:-<67}{0:1s}'.format('+', '-')+"\n"
                       

    def push(self, name, nest=0, size=0, next=None):
        stack = self.symbolTableStack
        nest = len(stack)
        next = stack[-1].name if len(stack) > 0 else None
        stack.append(SymbolTable(name, nest, size, next))
        
    def insertEntry(self, name, kind, type = "", size= 0, offset = 0, label = ""):
        table = self.symbolTableStack[-1]
        
        if kind == 'var':
            if type == 'Integer':
                size = 4
            elif type == 'Float':
                size = 8
            elif type == 'Character':
                size = 1
        
        
            if len(table.entries) > 0:
                previous_size = table.entries[-1]['size']
                previous_offset = table.entries[-1]['offset']
                offset = previous_size + previous_offset
  
        table.insert(name, kind, type, size, offset, label)     
   

from Analyzer import Analyzer       
