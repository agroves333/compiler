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
    
    
    def __init__(self, name, nest, size, next, label):
        self.name = name
        self.nest = nest
        self.size = size
        self.next = next
        self.label = label
        self.entries = []


    def insert(self, name, kind, type, size, offset, label=''):
        
        self.entries.append({"name":name, "kind":kind, "type":type, "size":size, "offset":offset, "label":label})
        self.size += size 
        
        
    def setNext(self, next):
        self.next = next
    
        
    def find(self, name):
        for entry in self.entries:
            if entry['name'] == name:
                return entry