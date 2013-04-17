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
    
    def __init__(self, name, nest, size, next):
        self.name = name
        self.nest = nest
        self.size = size
        self.next = next
        self.entries = []
    
    def insert(self, name, kind, type, size, offset, label):
        self.entries.append({"name":name, "kind":kind, "type":type, "size":size, "offset":offset, "label":label})
        
    def increaseSize(self, size):
        self.size += size
        
    def setNext(self, next):
        self.next = next
    
    def setLabel(self, name, label):
        for entry in self.entries:
            if entry['name'] == name:
                entry['label'] = label
        
    def find(self, name):
        for entry in self.entries:
            if entry['name'] == name:
                return entry