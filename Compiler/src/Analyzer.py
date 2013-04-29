import sys
from Parser import Parser

class Analyzer(object):
    
    outFile = None
    
    def __init__(self, fileName, symbolTableStack):
        
        self.outFile = open(fileName + '.asm', 'wb')
        self.output('PUSH D0')
        self.labelNumber = 1
        self.symbolTableStack = symbolTableStack
        
        
    def genAssign(self, ident_rec, expression_rec):
        if expression_rec["type"] != None:
            type = ident_rec["type"]
            nest = ident_rec["nest"]
            offset = ident_rec["offset"]
            if type == expression_rec["type"]:
                self.output('POP ' + str(offset) + '(D' + str(nest) +')')

    
    def genArithmetic(self, leftOp, operator, rightOp):
        opIR = ""
        if (leftOp != None) and (rightOp != None):
            if leftOp["type"] == rightOp["type"]:
                
                if leftOp["type"] == "Integer":
                    if operator["lexeme"] == "+":
                        opIR = "ADDS"
                    if operator["lexeme"] == "-":
                        opIR = "SUBS"
                    if operator["lexeme"] == "*":
                        opIR = "MULS"
                    if operator["lexeme"] == "/":
                        opIR = "DIVS"
                    
                if leftOp["type"] in ["Float", "Fixed"]:
                    if operator["lexeme"] == "+":
                        opIR = "ADDSF"
                    if operator["lexeme"] == "-":
                        opIR = "SUBSF"
                    if operator["lexeme"] == "*":
                        opIR = "MULSF"
                    if operator["lexeme"] == "/":
                        opIR = "DIVSF"
                
        self.output(opIR)
        return {"type": leftOp["type"]}
    
    def genRead(self, identRec):
        nest = identRec["nest"]
        offset = identRec["offset"]
        if identRec["type"] == "String":
            self.output("RDS "+str(offset)+"(D"+str(nest)+")")
        elif identRec["type"] == "Integer":
            self.output("RD "+str(offset)+"(D"+str(nest)+")") 
        elif identRec["type"] == "Float":
            self.output("RDF "+str(offset)+"(D"+str(nest)+")")
            
    def genWrite(self):
        self.output("WRTS")
    
    def genWriteln(self):
        self.output('WRT #"\\n"')
    
    def genPushId(self, identRec):
        entry = self.processId(identRec["lexeme"])
        nest = entry["nest"]
        offset = entry["offset"]
        self.output("PUSH "+str(offset)+"(D"+str(nest)+")")
        resultRec = entry["type"]
        return resultRec
    
    def genPushInt(self, integer):
        self.output("PUSH #"+integer)
    
    def genPushFloat(self, float):
        self.output("PUSH #"+float)
    
    def genPushString(self, string):
        self.output('PUSH #"'+string+'"')
        
    def genPushBoolean(self, bool):
        self.output("PUSH #" + str(bool))
        
    def genIncreaseStack(self, amount):
        self.output("ADD SP #"+str(amount)+" SP")
        
    def endProcOrFunc(self, table):
        self.output("SUB SP #"+str(table.size)+" SP")
        if table.label == "L1":
            self.output("HLT")
        else:
            self.genRet()
        
    def genLabel(self, label):
        self.output("L" + str(label) +":")
        
    def genBranch(self, label):
        self.output("BR L" + str(label))
        
    def genCall(self, label):
        self.output("CALL L" + str(label))
    
    def genRet(self):
        self.output("RET")
        
    def genBoolean(self, operator, expression):
        if expression["type"] == "Integer":
            if operator == "=":  # 71 RelationalOperator -> "="
                self.output("CMPEQS")           
            elif operator == "<":  # 72 RelationalOperator -> "<"
                self.output("CMPLTS")
            elif operator == ">":  # 73 RelationalOperator -> ">"
                self.output("CMPGTS")
            elif operator == "<=":  # 74 RelationalOperator -> "<="
                self.output("CMPLES")
            elif operator == ">=":  # 75 RelationalOperator -> ">="
                self.output("CMPGES")
            elif operator == "<>":  # 76 RelationalOperator -> "<>"
                self.output("CMPNES")
        
        if expression["type"] in ["Float", "Fixed"]:
            if operator == "=":  # 71 RelationalOperator -> "="
                self.output("CMPEQSF")           
            elif operator == "<":  # 72 RelationalOperator -> "<"
                self.output("CMPLTSF")
            elif operator == ">":  # 73 RelationalOperator -> ">"
                self.output("CMPGTSF")
            elif operator == "<=":  # 74 RelationalOperator -> "<="
                self.output("CMPLESF")
            elif operator == ">=":  # 75 RelationalOperator -> ">="
                self.output("CMPGESF")
            elif operator == "<>":  # 76 RelationalOperator -> "<>"
                self.output("CMPNESF")

    def processId(self, id):
        for table in self.symbolTableStack.tables[::-1]: # Reverse tableStack to search from local to global scope
            result = table.find(id)
            if result != None:
                result["nest"] = table.nest
                return result
            
    def genForLoop(self, control, limit):              
        pass
    
    def genBranchFalse(self, label):
        self.output("BRFS L" + str(label))
        
    def genBranchTrue(self, label):
        self.output("BRTS L" + str(label))
    

    def output(self, value):
        self.outFile.write(value+"\n")

    def getLabel(self):
        return self.labelNumber

    def incrementLabel(self):
        self.labelNumber += 1
