'''
Created on Mar 1, 2013

@author: adam
'''


class SymbolTable(object):
    
    name = ''
    label = ''
    nest = 0
    next = None
    size = 0
    
    entries = []
    
    def __init__(self, name):
        self.name = name
        self.entries = []
    
    def insert(self, name, kind, type, size, offset, label):
        self.entries.append({"name":name, "kind":kind, "type":type, "size":size, "offset":offset, "label":label})
        
    def find(self, id):
        for entry in self.entries:
            if entry.has_key(id):
                return entry[id]