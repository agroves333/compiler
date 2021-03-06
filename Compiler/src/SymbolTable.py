'''
Created on Mar 1, 2013

@author: adam
'''

import sys


class SymbolTableStack(object):

    tables = []
    
    def addTable(self, name, label):
        nest = len(self.tables)
        next = self.getCurrentTable().name if len(self.tables) > 0 else None
        table = SymbolTable(name, nest, next, label)
        self.tables.append(table)

    def getCurrentTable(self):
        if len(self.tables) > 0:
            return self.tables[-1]

    def popTable(self):
        if len(self.tables) > 0:
            self.tables.pop()
            
    def updateType(self, name, type):
        for table in self.tables:
            for entry in table.entries:
                if entry["name"] == name:
                    entry["type"] = type
    @staticmethod                
    def getParamCount(name):
        for table in SymbolTableStack.tables:
            if (table.name == name):
                
                return table.paramCount

class SymbolTable(object):
    
    def __init__(self, name, nest, next, label):
        self.name = name
        self.nest = nest
        self.size = 0
        self.next = next
        self.label = label
        self.paramCount = 0
        self.entries = []


    def insertEntry(self, name, kind, type='', label='', firstOfKind = False):
        offset = 0 
        if kind in ['var', 'iparam', 'dparam']:
            size = 1
            prevOffset = self.entries[-1]["offset"] if len(self.entries) > 0 else 0
            offset = prevOffset + 4 if firstOfKind else (prevOffset + size)
            self.size += 1
        else:
            size = 0

        if kind in ['iparam', 'dparam']:
            self.paramCount += 1
            
        if self.find(name) is None:
            self.entries.append({"name":name, "kind":kind, "type":type, "size":size, "offset":offset, "label":label, "paramCount":SymbolTableStack.getParamCount(name) if (kind in ["function", "procedure"]) else 0})
        else:
            print "ERROR: Already have something named " + name + ".  Cannot declare another " + name + "."
            sys.exit()
    

        
    def setNext(self, next):
        self.next = next
        
    def find(self, name):
        for entry in self.entries:
            if entry['name'] == name:
                return entry
        

    def printTable(self):
        print '{0:1s}{1:=<67}{0:1s}'.format('+', '=')
        print '{0:<1s} {1:10s} {2:10s} {3:<10s} {4:15s} {5:16s} {0:>1s}'.format('|', self.name +"   L"+ str(self.label), 'Nest: '+ str(self.nest), 'Size: '+ str(self.size), 'Next-> '+ str(self.next), "#Params" +str(self.paramCount))
        print '{0:1s}{1:=<67}{0:1s}'.format('+', '=')
        print '{0:<1s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {0:<1s}'.format('|', 'Name', 'Kind', 'Type', 'Size', 'Offset', 'Label')
        print '{0:1s}{1:-<67}{0:1s}'.format('+', '-')
        
        for entry in self.entries:
            print '{0:<1s} {1:10s} {2:10s} {3:10s} {4:<10d} {5:<10d} {6:10s} {7:10s} {0:<1s}'.format('|', entry['name'], entry['kind'], entry['type'], entry['size'], entry['offset'], "L"+str(entry['label']) if entry['label'] != "" else "", "pCount "+str(entry["paramCount"]))
        print '{0:1s}{1:-<67}{0:1s}'.format('+', '-')+"\n"
