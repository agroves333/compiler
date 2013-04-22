import sys
from Parser import Parser

class Analyzer(object):
    
    outFile = None
    
    def __init__(self, fileName):
        
        self.outFile = open(fileName + '.asm', 'wb')
        self.output('PUSH D0')
        
        
    def genAssign(self, ident_rec, expression_rec):
        if expression_rec["type"] != None:
            result = self.processId(ident_rec["name"])
            if (result != None):
                type = result["type"]
                nest = result["nest"]
                if type == expression_rec["type"]:
                    self.output('POP D'+nest+'\n')

    
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
        self.output("PUSH #"+string)
        
    def genIncreaseStack(self, amount):
        self.output("ADD SP,"+str(amount)+",SP")
        
    def genDecreaseStack(self, amount):
        self.output("SUB SP,"+str(amount)+",SP")
    
    def processId(self, id):
        for table in Parser.symbolTableStack[::-1]: # Reverse tableStack to search from local to global scope
            result = table.find(id)
            if result != None:
                result["nest"] = table.nest
                return result
    

    def output(self, value):
        self.outFile.write(value+"\n")