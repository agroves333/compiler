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
        
    # 1 SystemGoal -> Program eof
    def systemGoal(self):
        if(self.lookahead == "MP_PROGRAM"):
            self.program()
        else:
            self.error()
            
    # 2 Program -> ProgramHeading ";" Block "."
    def program(self): pass
    
    # 3 ProgramHeading -> "program" ProgramIdentifier
    def programHeading(self): pass
    
    # 4 Block -> VariableDeclarationPart ProcedureAndFunctionDeclarationPart StatementPart
    def block(self): pass
    
    # 5 VariableDeclarationPart -> "var" VariableDeclaration ";" VariableDeclarationTail
    def variableDeclarationPart(self): pass
    
    # 6 VariableDeclarationTail -> VariableDeclaration ";" VariableDeclarationTail 
    def variableDeclarationTail6(self): pass
    
    # 7 VariableDeclarationTail -> lambda
    def variableDeclarationTail7(self): pass
    
    # 8   VariableDeclaration -> Identifierlist ":" Type  
    def variableDeclaration(self): pass
    
    # 9   Type -> "Integer"
    def type9(self): pass
    
    # 10   Type -> "Float"
    def type10(self): pass
    
    # 11   Type -> "Boolean"
    def type11(self): pass
    
    # 12 ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
    def procedureAndFunctionDeclarationPart12(self): pass
    
    # 13 ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
    def procedureAndFunctionDeclarationPart13(self): pass
    
    # 14 ProcedureAndFunctionDeclarationPart -> ProcedureDeclaration ProcedureAndFunctionDeclarationPart
    def procedureAndFunctionDeclarationPart14(self): pass
    
    # 15 ProcedureDeclaration -> ProcedureHeading ";" Block ";"
    def procedureDeclaration(self): pass
    
    # 16 FunctionDeclaration  -> FunctionHeading ";" Block ";"       
    def functionDeclaration(self): pass
    
    # 17 ProcedureHeading -> "procedure" procedureIdentifier OptionalFormalParameterList
    def procedureHeading(self): pass
    
    # 18 FunctionHeading -> "function" functionIdentifier OptionalFormalParameterList ":" Type
    def functionHeading(self): pass
    
    # 19 OptionalFormalParameterList -> "(" FormalParameterSection FormalParameterSectionTail ")"
    def optionalFormalParameterList19(self): pass
    
    # 20 OptionalFormalParameterList -> lambda
    def optionalFormalParameterList20(self): pass
    
    # 21 FormalParameterSectionTail -> ";" FormalParameterSection FormalParameterSectionTail
    def formalParameterSectionTail21(self): pass
    
    # 22 FormalParameterSectionTail -> lambda
    def formalParameterSectionTail22(self): pass
    
    # 23 FormalParameterSection -> ValueParameterSection
    def formalParameterSection23(self): pass
    
    # 24 FormalParameterSection -> VariableParameterSection
    def formalParameterSection24(self): pass
    
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
    def statementTail30(self): pass
    
    # 31 StatementTail -> lambda
    def statementTail31(self): pass
    
    # 32 Statement -> EmptyStatement
    def statement32(self): pass
    
    # 33 Statement -> CompoundStatement
    def statement33(self): pass
    
    # 34 Statement -> ReadStatement
    def statement34(self): pass
    
    # 35 Statement -> WriteStatement
    def statement35(self): pass
    
    # 36 Statement -> AssignmentStatement
    def statement36(self): pass
    
    # 37 Statement -> IfStatement
    def statement37(self): pass
    
    # 38 Statement -> WhileStatement
    def statement38(self): pass
    
    # 39 Statement -> RepeatStatement
    def statement39(self): pass
    
    # 40 Statement -> ForStatement
    def statement40(self): pass
    
    # 41 Statement -> ProcedureStatement
    def statement41(self): pass
    
    # 42 EmptyStatement -> lambda
    def emptyStatement(self): pass
    
    # 43 ReadStatement -> "read" "(" ReadParameter ReadParameterTail ")"
    def readStatement(self): pass
    
    # 44 ReadParameterTail -> "," ReadParameter ReadParameterTail
    def readParameterTail44(self): pass
    
    # 45 ReadParameterTail -> lambda
    def readParameterTail45(self): pass
    
    # 46 ReadParameter -> VariableIdentifier   
    def readParameter(self): pass
    
    # 47 WriteStatement -> "write" "(" WriteParameter WriteParameterTail ")"
    def writeStatement(self): pass
    
    # 48 WriteParameterTail -> "," WriteParameter
    def writeParameterTail48(self): pass
    
    # 49 WriteParameterTail -> lambda
    def writeParameterTail49(self): pass
    
    # 50 WriteParameter -> OrdinalExpression    
    def writeParameter(self): pass
    
    # 51 AssignmentStatement -> VariableIdentifier ":=" Expression
    def assignmentStatement51(self): pass
    
    # 52 AssignmentStatement -> FunctionIdentifier ":=" Expression  
    def assignmentStatement52(self): pass
    
    # 53 IfStatement -> "if" BooleanExpression "then" Statement OptionalElsePart
    def ifStatement(self): pass
    
    # 54 OptionalElsePart -> "else" Statement
    def optionalElsePart54(self): pass
    
    # 55 OptionalElsePart -> lambda 
    def optionalElsePart55(self): pass
    
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
    def stepValue61(self): pass
    
    # 62 StepValue -> "downto"
    def stepValue62(self): pass
    
    # 63 FinalValue -> OrdinalExpression
    def finalValue(self): pass
    
    # 64 ProcedureStatement -> ProcedureIdentifier OptionalActualParameterList
    def procedureStatement(self): pass
    
    # 65 OptionalActualParameterList -> "(" ActualParameter ActualParameterTail ")"
    def optionalActualParameterList65(self): pass
    
    # 66 OptionalActualParameterList -> lambda
    def optionalActualParameterList66(self): pass
    
    # 67 ActualParameterTail -> "," ActualParameter ActualParameterTail
    def actualParameterTail67(self): pass
    
    # 68 ActualParameterTail -> lambda
    def actualParameterTail68(self): pass
    
    # 69 ActualParameter -> OrdinalExpression
    def actualParameter(self): pass
    
    # 70 Expression -> SimpleExpression OptionalRelationalPart
    def expression(self): pass
    
    # 71 OptionalRelationalPart -> RelationalOperator SimpleExpression
    def optionalRelationalPart71(self): pass
    
    # 72 OptionalRelationalPart -> lambda
    def optionalRelationalPart72(self): pass
    
    # 73 RelationalOperator -> "="
    def relationalOperator73(self): pass
    
    # 74 RelationalOperator -> "<"
    def relationalOperator74(self): pass
    
    # 75 RelationalOperator -> ">"
    def relationalOperator75(self): pass
    
    # 76 RelationalOperator -> "<="
    def relationalOperator76(self): pass
    
    # 77 RelationalOperator -> ">="
    def relationalOperator77(self): pass
    
    # 78 RelationalOperator -> "<>"
    def relationalOperator78(self): pass
    
    # 79 SimpleExpression -> OptionalSign Term TermTail
    def simpleExpression(self): pass
    
    # 80 TermTail -> AddingOperator Term TermTail
    def termTail80(self): pass
    
    # 81 TermTail -> lambda
    def termTail81(self): pass
    
    # 82 OptionalSign -> "+"
    def optionalSign82(self): pass
    
    # 83 OptionalSign -> "-"
    def optionalSign83(self): pass
    
    # 84 OptionalSign -> lambda
    def optionalSign84(self): pass
    
    # 85 AddingOperator -> "+"
    def addingOperator85(self): pass
    
    # 86 AddingOperator -> "-"
    def addingOperator86(self): pass
   
    # 87 AddingOperator -> "or"
    def addingOperator87(self): pass
    
    # 88 Term -> Factor FactorTail    
    def term(self): pass
    
    # 89 FactorTail -> MultiplyingOperator Factor FactorTail
    def factorTail89(self): pass
    
    # 90 FactorTail -> lambda
    def factorTai90l(self): pass
    
    # 91 MultiplyingOperator  -> "*"
    def multiplyingOperator91(self): pass
    
    # 92 MultiplyingOperator  -> "div"
    def multiplyingOperator92(self): pass
    
    # 93 MultiplyingOperator  -> "mod"
    def multiplyingOperator93(self): pass
    
    # 94 MultiplyingOperator  -> "and"
    def multiplyingOperator94(self): pass
    
    # 95 Factor -> UnsignedInteger
    def factor95(self): pass
    
    # 96 Factor -> VariableIdentifier
    def factor96(self): pass
    
    # 97 Factor -> "not" Factor
    def factor97(self): pass
    
    # 98 Factor -> "(" Expression ")"
    def factor98(self): pass
    
    # 99 Factor -> FunctionIdentifier OptionalActualParameterList
    def factor99(self): pass
    
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
    def identifierTail107(self): pass
    
    # 108 IdentifierTail -> lambda
    def identifierTail108(self): pass
    
     
    def error(self):
        print "A parse error has been encountered"        
