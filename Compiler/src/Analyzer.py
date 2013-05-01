import sys
from Parser import Parser

class Analyzer(object):
    
    outFile = None
    
    def __init__(self, fileName, symbolTableStack):
        
        self.outFile = open(fileName + '.asm', 'wb')
        self.labelNumber = 1
        self.symbolTableStack = symbolTableStack
        
        
    def genAssign(self, ident_rec, expression_rec):
        if expression_rec["type"] != None:
            id_type = ident_rec["type"]
            nest = ident_rec["nest"]
            offset = ident_rec["offset"]
            exp_type = expression_rec["type"]
            
            if id_type == exp_type:
                pass
            elif (id_type == "Integer") & (exp_type == "Float"):
                self.output("CASTSI")
            elif (id_type == "Float") & (exp_type == "Integer"):
                self.output("CASTSF")
            else:
                self.typeError(id_type, exp_type)
            
            self.output('POP ' + str(offset) + '(D' + str(nest) +')')

    
    def genArithmetic(self, leftOp, operator, rightOp):
        opIR = ""
        if (leftOp != None) and (rightOp != None):                
            if leftOp["type"] == "Integer":
                if rightOp["type"] == "Float":
                    # if int then float, pop float into temporary register,
                    # cast int to float, push float from temporary register
                    self.output("POP D9")
                    self.output("CASTSF")
                    self.output("PUSH D9")
                    if operator["lexeme"] == "+":
                        opIR = "ADDSF"
                    elif operator["lexeme"] == "-":
                        opIR = "SUBSF"
                    elif operator["lexeme"] == "*":
                        opIR = "MULSF"
                    elif operator["lexeme"] == "/":
                        opIR = "DIVSF"
                    elif operator["lexeme"] == "div":
                        opIR = "DIVSF" + "\n" + "CASTSI"    
                        
                    else:
                        self.opError(leftOp["type"], operator["lexeme"])
                        
                elif leftOp["type"] == rightOp["type"]:
                    if operator["lexeme"] == "+":
                        opIR = "ADDS"
                    elif operator["lexeme"] == "-":
                        opIR = "SUBS"
                    elif operator["lexeme"] == "*":
                        opIR = "MULS"
                    elif operator["lexeme"] == "/":
                        opIR = "DIVS"
                    elif operator["lexeme"] == "mod":
                        opIR = "MODS"
                    elif operator["lexeme"] == "div":
                        opIR = "DIVS" + "\n" + "CASTSI" 
                    else:
                        self.opError(leftOp["type"], operator["lexeme"])
                else:
                    self.typeError(leftOp["type"], rightOp["type"])

                
            elif leftOp["type"] == "Float":
                if rightOp["type"] == "Integer":
                    self.output("CASTSF")
                elif leftOp["type"] == rightOp["type"]:
                    pass
                else:
                    self.typeError(leftOp["type"], rightOp["type"])
                    
                if operator["lexeme"] == "+":
                    opIR = "ADDSF"
                elif operator["lexeme"] == "-":
                    opIR = "SUBSF"
                elif operator["lexeme"] == "*":
                    opIR = "MULSF"
                elif operator["lexeme"] == "/":
                    opIR = "DIVSF"
                elif operator["lexeme"] == "div":
                    opIR = "DIVSF" + "\n" + "CASTSI"
                else:
                    self.opError(leftOp["type"], operator["lexeme"])
                    
            elif leftOp["type"] == "Boolean":
                if leftOp["type"] == rightOp["type"]:
                    pass
                else:
                    self.typeError(leftOp["type"], rightOp["type"])
                    
                if operator["lexeme"] == "and":
                    opIR = "ANDS"
                elif operator["lexeme"] == "or":
                    opIR = "ORS"
                else:
                    self.opError(leftOp["type"], operator["lexeme"])
                    
            else:
                self.opError(leftOp["type"], operator["lexeme"])
            
                
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
        
    def incrementSP(self, amount):
        self.output("ADD SP #"+str(amount)+" SP")
        
    def decrementSP(self, amount):
        self.output("SUB SP #"+str(amount)+" SP")
        
    def finishProcOrFuncAR(self):
        table = self.symbolTableStack.getCurrentTable()
        # only increment the runtime stack by the size of local variables, not params
        varSize = 0
        for entries in table.entries:
            if entries["kind"] in ["var", "function"]:
                varSize += 1
        self.incrementSP(varSize + 4)
            
        self.output("MOV D" +str(table.nest)+ " -" +str(table.size + 4) +"(SP)")
        self.output("SUB SP #" +str(table.size + 4) +" D"+str(table.nest))
        
        
    def endProcOrFunc(self, table):
        self.output("MOV -" +str(table.size + 4) +"(SP) D" +str(table.nest))
        
        # only decrement the runtime stack by the size of local variables, not params
        varSize = 0
        for entries in table.entries:
            if entries["kind"] in ["var", "function"]:
                varSize += 1
        self.output("SUB SP #"+str(varSize + 4)+" SP")
            
        if table.label == 1:
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
        
    def genBoolean(self, operator, leftOp, rightOp):
        if leftOp["type"] == "Integer":
            if rightOp["type"] == "Float":
                # if int then float, pop float into temporary register,
                # cast int to float, push float from temporary register
                self.output("POP D9")
                self.output("CASTSF")
                self.output("PUSH D9")
                
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
            elif leftOp["type"] == rightOp["type"]:
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
            else:
                self.typeError(leftOp["type"], rightOp["type"])
        
        elif leftOp["type"] == "Float":
            if rightOp["type"] == leftOp["type"]:
                pass
            elif rightOp["type"] == "Integer":
                self.output("CASTSF")
            else:
                self.typeError(leftOp["type"], rightOp["type"])
                
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
                
        else:
            self.invalidError(leftOp["type"])

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
        
    def genNot(self):
        self.output("NOTS")
    
    def genNeg(self):
        self.output("NEGS")
    
    def genNegf(self):
        self.output("NEGSF")
    
    def output(self, value):
        self.outFile.write(value+"\n")

    def getLabel(self):
        return self.labelNumber

    def incrementLabel(self):
        self.labelNumber += 1
        
    def typeError(self, type1, type2): 
        print "Type mismatch error: " + str(type1) + " and " + str(type2)
        sys.exit()
        
    def invalidError(self, type1):
        print "Invalid type for the current operation: " +str(type1)
        sys.exit()

    def opError(self, type1, operator):
        print "Invalid operator for " + type1 + ": " + str(operator)
        sys.exit()
