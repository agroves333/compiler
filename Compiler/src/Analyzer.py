import sys
from Parser import Parser

class Analyzer(object):
    
    outFile = None
    
    def __init__(self, fileName):
        
        self.outFile = open(fileName + '.asm', 'wb')
        self.output('PUSH D0\n')
        
        
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
                        opIR = "SUBS"
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
    
    def genPushId(self, identRec, resultRec):
        pass
    
    def processId(self, id):
        for table in Parser.symbolTableStack[::-1]:
            result = table.find(id)
            if result != None:
                result["nest"] = table.nest
                return result
    

    def output(self, value):
        self.outFile.write(value+"\n")