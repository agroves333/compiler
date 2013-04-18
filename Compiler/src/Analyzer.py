

class Analyzer(object):
    
    def __init__(self, fileName):
        outFile = open(fileName + '.asm', 'w')
        outFile.write('PUSH D0\n')
        
        
    def genAssign(self, ident_rec, expression_rec):
        pass
    
    def genArithmetic(self, leftOp, operator, rightOp):
        pass
#         return result
    
    def genPushId(self, identRec, resultRec):
        pass
    
    def processId(self, ident_rec):
        pass
    
    
    