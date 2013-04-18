'''
Created on Mar 1, 2013

@author: adam
'''


class SymbolTable(object):
    
    name = ''
    label = ''
    nest = 0
    size = 0
    next = None
    entries = []
    labelCounter = 1
    
    
    def __init__(self, name, nest, size, next):
        self.name = name
        self.label = "L1" if name == "Main" else ''
        self.nest = nest
        self.size = size
        self.next = next
        self.entries = []
    
    
    def insert(self, name, kind, type, size, offset, label=''):
        if kind in ['procedure', 'function']:
            SymbolTable.labelCounter += 1
            label = "L"+str(SymbolTable.labelCounter)
        
        self.entries.append({"name":name, "kind":kind, "type":type, "size":size, "offset":offset, "label":label})
        self.size += size 
        
        
    def setNext(self, next):
        self.next = next
    
        
    def find(self, name):
        for entry in self.entries:
            if entry['name'] == name:
                return entry