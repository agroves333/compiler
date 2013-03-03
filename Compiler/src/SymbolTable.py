'''
Created on Mar 1, 2013

@author: adam
'''


class SymbolTable(object):
    
    name = '';
    
    entries = []
    
    def __init__(self, name):
        self.name = name
    
    def insert(self, id, type):
        self.entries.append({"id":id,"type":type})
        
    def find(self, id):
        for entry in self.entries:
            if entry.has_key(id):
                return entry[id]