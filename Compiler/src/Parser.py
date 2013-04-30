import sys
# import inspect

from SymbolTable import SymbolTableStack
from Scanner import Scanner

class Parser(object):

    scanner = None
    analyzer = None
    sourceFile = None
    symbolTableStack = None
    lookahead = ''
    firstIdFlag = False
    
    # Constructor
    def __init__(self, fileName):
        try:
            self.sourceFile = open(fileName, 'r')
        except IOError:
            sys.exit("Source file not found")

        self.scanner = Scanner(self.sourceFile)
        self.symbolTableStack = SymbolTableStack()
        self.analyzer = Analyzer(fileName, self.symbolTableStack)

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
            self.error("MP_PROGRAM")
            
    
    def program(self):
        if self.lookahead is "MP_PROGRAM":  # 2 Program -> ProgramHeading ";" Block "."
            self.programHeading()
            self.match("MP_SCOLON")
            self.block()
            self.match("MP_PERIOD")
        else:
            self.error("MP_PROGRAM")
    
    
    def programHeading(self):
        if self.lookahead is "MP_PROGRAM":  # 3 ProgramHeading -> "program" ProgramIdentifier
            self.match("MP_PROGRAM")
            self.programIdentifier()
            self.symbolTableStack.addTable('Main', self.analyzer.getLabel())
            self.analyzer.genBranch(self.analyzer.getLabel())
        else:
            self.error("MP_PROGRAM")
    
    
    def block(self):
        if self.lookahead in ["MP_VAR", "MP_BEGIN", "MP_FUNCTION", "MP_PROCEDURE"]:  # 4 Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart
            self.variableDeclarationPart()
            self.procedureAndFunctionDeclarationPart()
            self.statementPart()
        else:
            self.error('"MP_VAR", "MP_BEGIN", "MP_FUNCTION", "MP_PROCEDURE"')
    
    
    def variableDeclarationPart(self):
        
        if self.lookahead is "MP_VAR":  # 5 VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
            self.match("MP_VAR")
            self.firstIdFlag = True
            self.variableDeclaration()
            self.match("MP_SCOLON")
            self.variableDeclarationTail()

        elif self.lookahead in ["MP_BEGIN", "MP_FUNCTION", "MP_PROCEDURE"]:
            return
        else:
            self.error('"MP_VAR", "MP_BEGIN", "MP_FUNCTION", "MP_PROCEDURE"')
    
    
    def variableDeclarationTail(self):
        if self.lookahead in ["MP_PROCEDURE", "MP_FUNCTION", "MP_BEGIN"]:  # 7 VariableDeclarationTail -> lambda
            return
        elif self.lookahead is "MP_IDENTIFIER":  # 6 VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail 
            self.variableDeclaration()
            self.match("MP_SCOLON")
            self.variableDeclarationTail()
        else:
            self.error('"MP_PROCEDURE", "MP_FUNCTION", "MP_BEGIN", "MP_IDENTIFIER", "MP_SCOLON"')
    
    
    
    def variableDeclaration(self):
        if self.lookahead is "MP_IDENTIFIER":  # 8 VariableDeclaration -> IdentifierList ":" Type  
            idList = self.identifierList()
            self.match("MP_COLON")
            varType = self.type()
            for name in idList:
                self.symbolTableStack.getCurrentTable().insertEntry(name, 'var', varType, '', self.firstIdFlag)
            self.firstIdFlag = False
        else:
            self.error("MP_IDENTIFIER")
    
    
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
            self.error("Integer, Float, String, Boolean")
    
    
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
            self.error("Procedure, Function, Begin")

    
    def procedureDeclaration(self):
        if self.lookahead is "MP_PROCEDURE":  # 13 ProcedureDeclaration -> ProcedureHeading ";" Block ";"
            self.procedureHeading();
            self.match('MP_SCOLON')
            self.block()
            self.match('MP_SCOLON')
        else:
            self.error("Procedure")
    
          
    def functionDeclaration(self):
        if self.lookahead is "MP_FUNCTION":  # 14 FunctionDeclaration  -> FunctionHeading ";" Block ";"
            self.functionHeading()
            self.match("MP_SCOLON")
            self.block()
            self.match("MP_SCOLON")
        else:
            self.error("Function")
    
    
    def procedureHeading(self):
        if self.lookahead is "MP_PROCEDURE":  # 15 ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
            self.match("MP_PROCEDURE")
            name = self.procedureIdentifier()
            label = self.analyzer.incrementLabel()
            self.symbolTableStack.getCurrentTable().insertEntry(name, 'procedure', label=label)
            self.symbolTableStack.addTable(name, label)
            self.optionalFormalParameterList()
        else:
            self.error("Procedure")
    
    
    def functionHeading(self):
        if self.lookahead is "MP_FUNCTION":  # 16 FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList ":" Type
            self.match("MP_FUNCTION")
            name = self.functionIdentifier()
            label = self.analyzer.incrementLabel()
            self.symbolTableStack.getCurrentTable().insertEntry(name, 'function', label=label)
            self.symbolTableStack.addTable(name, label)
            self.optionalFormalParameterList()
            self.match("MP_COLON")
            self.type()
        else:
            self.error("Function")
    
    
    
    def optionalFormalParameterList(self):
        if self.lookahead is 'MP_LPAREN':  # 17 OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
            self.match('MP_LPAREN')
            self.firstIdFlag = True
            self.formalParameterSection()
            self.formalParameterSectionTail()
            self.match('MP_RPAREN')
            
        elif self.lookahead in ['MP_COLON', 'MP_SCOLON', 'MP_INTEGER', 'MP_FLOAT', 'MP_BOOLEAN', 'MP_STRING']:  # 18 OptionalFormalParameterList -> lambda
            return
        else:
            self.error("(, :, ;, Integer, Float, Boolean, String")
       
    
    def formalParameterSectionTail(self):
        if self.lookahead is "MP_SCOLON":  # 19 FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
            self.match('MP_SCOLON')
            self.formalParameterSection()
            self.formalParameterSectionTail()
        elif self.lookahead is 'MP_RPAREN':  # 20 FormalParameterSectionTail -> lambda
            return 
        else:
            self.error(";, )")
    
    
    
    def formalParameterSection(self):
        if self.lookahead is 'MP_IDENTIFIER':  # 21 FormalParameterSection -> ValueParameterSection
            self.valueParameterSection()
        elif self.lookahead is 'MP_VAR':  # 22 FormalParameterSection -> VariableParameterSection
            self.variableParameterSection()
        else:
            self.error("Identifier, Var")
    
    
    def valueParameterSection(self):
        if self.lookahead is 'MP_IDENTIFIER':  # 23 ValueParameterSection -> IdentifierList ":" Type
            identList = []
            identList = self.identifierList();
            self.match('MP_COLON')
            varType = self.type()
            for name in identList:
                self.symbolTableStack.getCurrentTable().insertEntry(name, 'param', varType, '', self.firstIdFlag)
                self.firstIdFlag = False
        else:
            self.error("Identifier")
    
    
    def variableParameterSection(self):
        if self.lookahead is 'MP_VAR':  # 24 VariableParameterSection -> "var" IdentifierList ":" Type
            self.match('MP_VAR')
            identList = []
            identList = self.identifierList();
            self.match('MP_COLON')
            varType = self.type()
            for name in identList:
                self.symbolTableStack.getCurrentTable().insertEntry(name, 'param', varType, '', self.firstIdFlag)
            self.firstIdFlag = False
        else:
            self.error("Var")
    
    
    def statementPart(self):
        if self.lookahead is 'MP_BEGIN':  # 25 StatementPart -> CompoundStatement
            self.analyzer.genLabel(self.symbolTableStack.getCurrentTable().label)
            self.compoundStatement()
            self.symbolTableStack.getCurrentTable().printTable()
            self.analyzer.endProcOrFunc(self.symbolTableStack.getCurrentTable())
            self.symbolTableStack.popTable()
        else:
            self.error("Begin")
        
    
    def compoundStatement(self):
        if self.lookahead is 'MP_BEGIN':  # 26 CompoundStatement -> "begin" StatementSequence "end"
            self.match('MP_BEGIN')
            self.analyzer.finishProcOrFuncAR()         
            self.statementSequence()
            self.match('MP_END')          
        else:
            self.error("begin")
    
    
    def statementSequence(self):
        if self.lookahead in ['MP_SCOLON', 'MP_IDENTIFIER',  # 27 StatementSequence -> Statement StatementTail
                              'MP_BEGIN', 'MP_END', 'MP_READ',
                              'MP_WRITE', 'MP_IF', 'MP_ELSE',
                              'MP_REPEAT', 'MP_UNTIL', 'MP_WHILE',
                              'MP_FOR', 'MP_WRITELN']:
            self.statement()
            self.statementTail()
        else:
            self.error("'MP_SCOLON', 'MP_IDENTIFIER', 'MP_BEGIN', 'MP_END', 'MP_READ',\
                            'MP_WRITE', 'MP_IF', 'MP_ELSE', 'MP_REPEAT', 'MP_UNTIL', 'MP_WHILE',\
                            'MP_FOR', 'MP_WRITELN'")
    
    
    def statementTail(self):
        if self.lookahead is 'MP_SCOLON':  # 28 StatementTail -> ";" Statement StatementTail
            self.match('MP_SCOLON')
            self.statement()
            self.statementTail()
        elif self.lookahead in ['MP_END', 'MP_UNTIL']:  # 29 StatementTail -> lambda
            return
        else:
            self.error(";, end, until")
    
    
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
            self.error(";, end, else, until, begin, read, write, writeln, identifier, :=, if, while, repeat, for")
    
    
    
    def emptyStatement(self):
        if self.lookahead in ['MP_SCOLON', 'MP_END',  # 40 EmptyStatement -> lambda
                              'MP_ELSE', 'MP_UNTIL']:
            return
        else:
            self.error(";, end, else, until")
    
    
    def readStatement(self):
        if self.lookahead is 'MP_READ':  # 41 ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
            self.match('MP_READ')
            self.match('MP_LPAREN')
            self.readParameter()
            self.readParameterTail()
            self.match('MP_RPAREN')
        else:
            self.error("read")
            
    
    def readParameterTail(self):
        if self.lookahead is 'MP_COMMA':  # 42 ReadParameterTail -> "," ReadParameter ReadParameterTail
            self.match('MP_COMMA')
            self.readParameter()
            self.readParameterTail()
        elif self.lookahead is 'MP_RPAREN':  # 43 ReadParameterTail -> lambda
            return
        else:
            self.error("comma, )")
    
    
    def readParameter(self):
        if self.lookahead is 'MP_IDENTIFIER':  # 44 ReadParameter -> VariableIdentifier
            id = self.variableIdentifier()
            identRec = self.analyzer.processId(id)
            self.analyzer.genRead(identRec)
        else:
            self.error("identifier")
            
    
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
            self.error("write, writeln")
      
    
    def writeParameterTail(self):
        if self.lookahead is 'MP_COMMA':  # 46 WriteParameterTail -> "," WriteParameter
            self.match('MP_COMMA')
            self.writeParameter()
            self.writeParameterTail()
        elif self.lookahead is 'MP_RPAREN':  # 47 WriteParameterTail -> lambda
            return
        else:
            self.error("comma, )")
    
    
    def writeParameter(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',  # 48 WriteParameter -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            self.ordinalExpression()
            self.analyzer.genWrite()
        else:
            self.error("(, identifier, +, -, any literal value, not")
    
    
    def assignmentStatement(self):
        # semantic records
        expressionRec = {}
        identRec = {}
        
        if self.lookahead is 'MP_IDENTIFIER':  # 49 AssignmentStatement -> VariableIdentifier ":=" Expression  OR
            
            id = self.variableIdentifier()
            identRec = self.analyzer.processId(id)
            print identRec
            self.match('MP_ASSIGN')
            expressionRec = self.expression()
            self.analyzer.genAssign(identRec, expressionRec)
            
        # This doesn't change parsing functionality
        # elif self.lookahead is 'MP_IDENTIFIER':   # 50 AssignmentStatement -> FunctionIdentifier ":=" Expression
        #    self.functionIdentifier()
        #    self.match('MP_ASSIGN')
        #    self.expression()
        else:
            self.error("identifier")
            
            
    
    def ifStatement(self):
        if self.lookahead is 'MP_IF':  # 51 IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
            self.match('MP_IF')
            self.booleanExpression()
            self.analyzer.incrementLabel()
            self.analyzer.genBranchFalse(self.analyzer.getLabel())
            self.match('MP_THEN')
            self.statement()
            self.optionalElsePart()
        else:
            self.error("if")
    
    
   
   
    def optionalElsePart(self):
        #TODO: Table says else is ambiguous? haven't looked at it yet
        if self.lookahead is 'MP_ELSE':  # 52 OptionalElsePart -> "else" Statement
            self.match('MP_ELSE')
            self.analyzer.genLabel(self.analyzer.getLabel())
            self.statement()
        elif self.lookahead in ['MP_SCOLON', 'MP_END', 'MP_UNTIL']:  # 53 OptionalElsePart -> lambda
            return
        else:
            self.error("else, ;, end, until")
            
    
                
    def repeatStatement(self):
        if self.lookahead is 'MP_REPEAT':  # 54 RepeatStatement -> "repeat" StatementSequence "until" BooleanExpression
            self.match('MP_REPEAT')
            self.analyzer.incrementLabel()
            self.analyzer.genLabel(self.analyzer.getLabel())
            self.statementSequence()
            self.match('MP_UNTIL')
            self.booleanExpression()
            self.analyzer.genBranchTrue(self.analyzer.getLabel() + 1)
            self.analyzer.genBranch(self.analyzer.getLabel())
            self.analyzer.genLabel(self.analyzer.getLabel() + 1)
        else:
            self.error("repeat")
            
    
    
    def whileStatement(self):
        if self.lookahead is 'MP_WHILE':  # 55 WhileStatement -> "while" BooleanExpression "do" Statement
            self.match('MP_WHILE')
            self.analyzer.incrementLabel()
            self.analyzer.genLabel(self.analyzer.getLabel())
            self.booleanExpression()
            self.analyzer.genBranchFalse(self.analyzer.getLabel() + 1)
            self.match('MP_DO')
            self.statement()
            self.analyzer.genBranch(self.analyzer.getLabel())
            self.analyzer.incrementLabel()
            self.analyzer.genLabel(self.analyzer.getLabel())
        else:
            self.error("while")
            
    
    
    def forStatement(self):
        ident_rec = {}
        expression_rec = {}
        
        if self.lookahead is 'MP_FOR':  # 56 ForStatement -> "for" ControlVariable ":=" InitialValue StepValue FinalValue "do" Statement
            self.match('MP_FOR')
            ident_rec = self.controlVariable()
            self.match('MP_ASSIGN')
            expression_rec = self.initialValue()
            self.analyzer.genAssign(ident_rec, expression_rec)
            step = self.stepValue()
            self.analyzer.incrementLabel()
            self.analyzer.genLabel(self.analyzer.getLabel())
            self.finalValue()
            self.analyzer.genPushId(ident_rec)
            if(step == "to"):
                self.analyzer.genBoolean(">", ident_rec)
                self.analyzer.genBranchTrue(self.analyzer.getLabel() + 1)
            elif(step == "downto"):
                self.analyzer.genBoolean("<", ident_rec)
                self.analyzer.genBranchTrue(self.analyzer.getLabel() + 1)
            self.match('MP_DO')
            self.statement()
            if(step == "to"):
                self.analyzer.genPushInt(str(1))
            elif(step == "downto"):
                self.analyzer.genPushInt(str(-1))
            self.analyzer.genPushId(ident_rec)
            self.analyzer.output("ADDS")
            self.analyzer.genAssign(ident_rec, expression_rec)
            self.analyzer.genBranch(self.analyzer.getLabel())
            self.analyzer.incrementLabel()
            self.analyzer.genLabel(self.analyzer.getLabel())
        else:
            self.error("for")
            
    
    
    def controlVariable(self):
        identRec = {}
        if self.lookahead is 'MP_IDENTIFIER':  # 57 ControlVariable -> VariableIdentifier
            id = self.variableIdentifier()                
            identRec = self.analyzer.processId(id)
            identRec["lexeme"] = id
            return identRec
        else:
            self.error("identifier")

    
    def initialValue(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',  # 58 InitialValue -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            return self.ordinalExpression()
        else:
            self.error("(, identifier, +, -, any literal value, not")
    
    
    
    def stepValue(self):
        if self.lookahead is 'MP_TO':  # 59 StepValue -> "to"
            return self.match('MP_TO')
        elif self.lookahead is 'MP_DOWNTO':  # 60 StepValue -> "downto"
            return self.match('MP_DOWNTO')
        else:
            self.error("to, downto")
        
    
    
    def finalValue(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',  # 61 FinalValue -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            self.ordinalExpression()
        else:
            self.error("(, identifier, +, -, any literal value, not")
            
    
    
    def procedureStatement(self):
        if self.lookahead is 'MP_IDENTIFIER':  # 62 ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
            procedureName = self.procedureIdentifier()
            self.optionalActualParameterList()
            label = self.symbolTableStack.getCurrentTable().find(procedureName)['label']
            self.analyzer.genCall(label)
        else:
            self.error("identifier")
    
    
    
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
            self.error(";, ), end, comma, then, else, until, to do, downto, an equality operator, an arithmetic operator, and, mod")
            
    
    
    def actualParameterTail(self):
        if self.lookahead is 'MP_COMMA':  # 65 ActualParameterTail -> "," ActualParameter ActualParameterTail
            self.match('MP_COMMA')
            self.actualParameter()
            self.actualParameterTail()
        elif self.lookahead is 'MP_RPAREN':  # 66 ActualParameterTail -> lambda
            return
        else:
            self.error("comma, )")
    
    
   
    def actualParameter(self):
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',   # 67 ActualParameter -> OrdinalExpression
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            self.ordinalExpression()
        else:
            self.error("(, identifier, +, -, any literal value, not")
            
    
    
    def expression(self):
        expression_rec = {}
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',   # 68 Expression -> SimpleExpression OptionalRelationalPart
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            expression_rec = self.simpleExpression()

            expression_rec = self.optionalRelationalPart(expression_rec)
            return expression_rec
#             return self.mapTokenToType(self.lookahead)
        else:
            self.error("(, identifier, +, -, any literal value, not")
         
    
    
    def optionalRelationalPart(self, expression_rec):
        
        if self.lookahead in ['MP_EQUAL', 'MP_LTHAN',  # 69 OptionalRelationalPart -> RelationalOperator SimpleExpression
                              'MP_GTHAN', 'MP_LEQUAL',
                              'MP_GEQUAL', 'MP_NEQUAL']:
            operator = self.relationalOperator()
            expression_rec = self.simpleExpression()          
            self.analyzer.genBoolean(operator, expression_rec)
            expression_rec["type"] = 'Boolean'
            return expression_rec
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', # 70 OptionalRelationalPart -> lambda
                                'MP_END', 'MP_COMMA',
                                'MP_THEN', 'MP_ELSE',
                                'MP_UNTIL','MP_DO', 
                                'MP_TO', 'MP_DOWNTO']:
            return expression_rec
        else:
            self.error("an equality operator, ;, ), then, else, until, do, to, downto")
        
    
       
    def relationalOperator(self):
        if self.lookahead is 'MP_EQUAL':  # 71 RelationalOperator -> "="
            operator = self.match('MP_EQUAL')           
        elif self.lookahead is 'MP_LTHAN':  # 72 RelationalOperator -> "<"
            operator = self.match('MP_LTHAN')
        elif self.lookahead is 'MP_GTHAN':  # 73 RelationalOperator -> ">"
            operator = self.match('MP_GTHAN')
        elif self.lookahead is 'MP_LEQUAL':  # 74 RelationalOperator -> "<="
            operator = self.match('MP_LEQUAL')
        elif self.lookahead is 'MP_GEQUAL':  # 75 RelationalOperator -> ">="
            operator = self.match('MP_GEQUAL')
        elif self.lookahead is 'MP_NEQUAL':  # 76 RelationalOperator -> "<>"
            operator = self.match('MP_NEQUAL')
        else:
            self.error("an equality operator")
        return operator    
    
    
    def simpleExpression(self):
        # semantic records
        termRec = {}
        termTailRec = {}
        
        if self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',   # 77 SimpleExpression -> OptionalSign Term TermTail
                              'MP_PLUS', 'MP_MINUS',
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                              'MP_NOT', 'MP_INTEGER_LIT',
                              'MP_TRUE', 'MP_FALSE']:
            
            sign = self.optionalSign()
            termRec = self.term()
            if sign == "-":
                self.analyzer.genNeg()
            termTailRec = termRec
            termTailRec = self.termTail(termTailRec)
            expressionRec = termTailRec     # This is what Rocky suggested
            return expressionRec
        else:
            self.error("(, identifier, +, -, any literal value, not")
            
    
    
    def termTail(self, termTailRec = {}):
        # Semantic Records
        addopRec = {}
        termRec = {}
        
        if self.lookahead in ['MP_PLUS', 'MP_MINUS', 'MP_OR']:  # 78 TermTail -> AddingOperator Term TermTail
            addopRec["lexeme"] = self.addingOperator()
            termRec = self.term()
            resultRec = self.analyzer.genArithmetic(termTailRec, addopRec, termRec)
            
            self.termTail(resultRec)
            termTailRec = resultRec
            
            return termTailRec
            
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', 'MP_END',  # 79 TermTail -> lambda
                                'MP_COMMA', 'MP_THEN', 'MP_ELSE',
                                'MP_UNTIL', 'MP_DO', 'MP_TO',
                                'MP_DOWNTO', 'MP_EQUAL', 'MP_LTHAN',
                                'MP_GTHAN', 'MP_LEQUAL', 'MP_GEQUAL',
                                'MP_NEQUAL']:
            return termTailRec
        else:
            self.error("+, -, or, ;, ), end, comma, then, else, until, do, to, downto, an equality operator")
            
    
    
    def optionalSign(self):
        if self.lookahead is 'MP_PLUS':  # 80 OptionalSign -> "+"
            self.match('MP_PLUS')
        elif self.lookahead is 'MP_MINUS':  # 81 OptionalSign -> "-"
            return self.match('MP_MINUS')
        elif self.lookahead in ['MP_LPAREN', 'MP_IDENTIFIER',  # 82 OptionalSign -> lambda
                                'MP_NOT', 'MP_INTEGER_LIT',
                                'MP_FLOAT_LIT', 'MP_FIXED_LIT', 'MP_STRING_LIT',
                                'MP_TRUE', 'MP_FALSE']:
            return
        else:
            self.error("+, -, (, identifier, +, -, any literal value, not")
    
    
    
    def addingOperator(self):
        if self.lookahead is 'MP_PLUS':  # 83 AddingOperator -> "+"
            return self.match('MP_PLUS')
        elif self.lookahead is 'MP_MINUS':  # 84 AddingOperator -> "-"
            return self.match('MP_MINUS')
        elif self.lookahead is 'MP_OR':  # 85 AddingOperator -> "or"
            return self.match('MP_OR')
        else:
            self.error("+, -, or")
            
    
    
    def term(self):
        termRec = {}
        
        if self.lookahead in ['MP_LPAREN',  # 86 Term -> Factor FactorTail
                           'MP_IDENTIFIER', 'MP_NOT',
                           'MP_INTEGER_LIT', 'MP_FLOAT_LIT', 'MP_FIXED_LIT',
                           'MP_STRING_LIT', 'MP_TRUE',
                           'MP_FALSE']:
            
            termRec["type"] = self.factor()
            termRec = self.factorTail(termRec)
            return termRec
#             return self.mapTokenToType(self.lookahead)
        else:
            self.error("(, identifier, +, -, any literal value, not")
            
            
    
    def factorTail(self, termRec):
        rightOp = {}
        operator = {}
        
        if self.lookahead in ['MP_TIMES', 'MP_DIV',  # 87 FactorTail -> MultiplyingOperator Factor FactorTail
                              'MP_MOD', 'MP_AND', 'MP_SLASH']:
            operator["lexeme"] = self.multiplyingOperator()
            rightOp["type"] = self.factor()
            self.analyzer.genArithmetic(termRec, operator, rightOp)
            self.factorTail(rightOp)
            return termRec
        elif self.lookahead in ['MP_SCOLON', 'MP_RPAREN', 'MP_END',  # 88 FactorTail -> lambda
                                'MP_COMMA', 'MP_THEN', 'MP_ELSE',
                                'MP_UNTIL', 'MP_DO', 'MP_TO', 'MP_DOWNTO',
                                'MP_EQUAL', 'MP_LTHAN', 'MP_GTHAN',
                                'MP_LEQUAL', 'MP_GEQUAL', 'MP_NEQUAL',
                                'MP_PLUS', 'MP_MINUS', 'MP_OR']:
            return termRec
        else:
            self.error("*, div, mod, and /, ;, ), end, comma, then, else, until, do, to, downto, an equality operator, +, -, or")
            
            
            
    def multiplyingOperator(self): 
        if self.lookahead is 'MP_TIMES':    # 89 MultiplyingOperator  -> "*"
            return self.match('MP_TIMES')
        elif self.lookahead is 'MP_DIV':    # 90 MultiplyingOperator  -> "div"
            return self.match('MP_DIV')
        elif self.lookahead is 'MP_MOD':    # 91 MultiplyingOperator  -> "mod"
            return self.match('MP_MOD')
        elif self.lookahead is 'MP_AND':    # 92 MultiplyingOperator  -> "and"
            return self.match('MP_AND')
        elif self.lookahead is 'MP_SLASH':  # 112 MultiplyingOperator -> "/"
            return self.match('MP_SLASH')
        else:
            self.error("*, div, mod, and, /")
            
    
    
    def factor(self):
        # semantic record
        identRec = {}
        
        if self.lookahead in ['MP_INTEGER_LIT']:  # 93 Factor -> UnsignedInteger
            integer = self.match('MP_INTEGER_LIT')
            self.analyzer.genPushInt(integer)
            return "Integer"
        elif self.lookahead is 'MP_IDENTIFIER':  # 94 Factor -> VariableIdentifier  OR  # 97 Factor -> FunctionIdentifier OptionalActualParameterList
            id_kind = self.analyzer.processId(self.scanner.lexeme)["kind"]
            if id_kind == "function":
                id = self.functionIdentifier()
                self.optionalActualParameterList()
            elif id_kind in ["var", "param"]:
                id = self.variableIdentifier()
                
                identRec["lexeme"] = id
                self.analyzer.genPushId(identRec)
                
            return self.analyzer.processId(id)["type"]
        
        elif self.lookahead is 'MP_NOT':  # 95 Factor -> "not" Factor
            self.match('MP_NOT');
            self.factor()
            self.analyzer.genNot()
            return "Boolean"
        elif self.lookahead is 'MP_LPAREN':  # 96 Factor -> "(" Expression ")"
            self.match('MP_LPAREN')
            type = self.expression()["type"]
            self.match('MP_RPAREN')
            return type
        elif self.lookahead in ['MP_FLOAT_LIT']:  # 113 Factor -> UnsignedFloat
            float = self.match('MP_FLOAT_LIT')
            self.analyzer.genPushFloat(float)
            return "Float"
        elif self.lookahead in ['MP_FIXED_LIT']:  # 113 Factor -> UnsignedFloat
            fixed = self.match('MP_FIXED_LIT')
            self.analyzer.genPushFloat(fixed)
            return "Float"
        elif self.lookahead in ['MP_STRING_LIT']:  # 114 Factor -> StringLiteral
            string = self.match('MP_STRING_LIT')
            self.analyzer.genPushString(string)
            return "String"
        elif self.lookahead in ['MP_TRUE']:  # 115 Factor -> "True"
            self.match('MP_TRUE')
            self.analyzer.genPushBoolean(1)
            return "Boolean"
        elif self.lookahead in ['MP_FALSE']:  # 116 Factor -> "False"
            self.match('MP_FALSE')
            self.analyzer.genPushBoolean(0)
            return "Boolean"
        else:
            self.error("(, identifier, +, -, any literal value, not")


    def programIdentifier(self):
        if(self.lookahead == "MP_IDENTIFIER"):  # 98 ProgramIdentifier -> Identifier
            return self.match("MP_IDENTIFIER")
        else:
            self.error("identifier")
    
    
    def variableIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 99 VariableIdentifier -> Identifier
            return self.match("MP_IDENTIFIER")
        else:
            self.error("identifier")
    
    
    def procedureIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 100 ProcedureIdentifier -> Identifier
            return self.match("MP_IDENTIFIER")
        else:
            self.error("identifier")
    
    
    def functionIdentifier(self): 
        if(self.lookahead == "MP_IDENTIFIER"):  # 101 FunctionIdentifier -> Identifier
            return self.match("MP_IDENTIFIER")
        else:
            self.error("identifier")
    
   
    def booleanExpression(self):
        if(self.lookahead in ["MP_LPAREN", "MP_IDENTIFIER",   # 102 BooleanExpression -> Expression
                              "MP_PLUS", "MP_MINUS",
                              "MP_NOT", "MP_INTEGER_LIT",
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT',
                              'MP_STRING_LIT', 'MP_TRUE',
                              'MP_FALSE']):
            self.expression()
        else:
            self.error("(, identifier, +, -, any literal value, not, +, -")
    
      
    def ordinalExpression(self):
        if(self.lookahead in ["MP_LPAREN", "MP_IDENTIFIER",   # 103 OrdinalExpression -> Expression
                              "MP_PLUS", "MP_MINUS",
                              "MP_NOT", "MP_INTEGER_LIT",
                              'MP_FLOAT_LIT', 'MP_FIXED_LIT',
                              'MP_STRING_LIT', 'MP_TRUE',
                              'MP_FALSE']):
            return self.expression()
        else:
            self.error("(, identifier, +, -, any literal value, not, +, -")
    
    
    def identifierList(self):
        if(self.lookahead == "MP_IDENTIFIER"):  # 104 IdentifierList -> Identifier IdentifierTail
            ident = []
            ident.append(self.scanner.lexeme)
            self.match("MP_IDENTIFIER")
            self.identifierTail(ident)
            return ident
        else:
            self.error("identifier")
    


    def identifierTail(self,ident): 
        if(self.lookahead == "MP_COMMA"):  # 105 IdentifierTail -> "," Identifier IdentifierTail
            self.match("MP_COMMA")
            ident.append(self.scanner.lexeme)
            self.match("MP_IDENTIFIER")
            self.identifierTail(ident)
        elif(self.lookahead == "MP_COLON"):  # 106 IdentifierTail -> lambda
            return
        else:
            self.error("comma, :")

    def error(self, expected):
        print "Syntax error found on line " + str(self.scanner.getLineNumber()) + ", column " + str(self.scanner.getColumnNumber())
        print "Found " + self.scanner.lexeme + " when expected one of: " + expected
        # print the caller
#         print inspect.stack()[1][3]
        sys.exit()
        
    def matchError(self, expected):
        print "Match error found on line " + str(self.scanner.getLineNumber()) + ", column " + str(self.scanner.getColumnNumber()) + " lexeme: " + self.scanner.lexeme
        print "Found " + self.lookahead + " when expected " + expected
        # print the caller
        sys.exit()

from Analyzer import Analyzer       
