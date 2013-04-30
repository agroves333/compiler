'''
Created on Mar 1, 2013

@author: adam
'''

import sys


class SymbolTableStack(object):

    def __init__(self):
        self.tables = []

    def addTable(self, name, label):
        nest = len(self.tables)
        next = self.getCurrentTable().name if len(self.tables) > 0 else None
        table = SymbolTable(name, nest, next, label)
        self.tables.append(table)

    def getCurrentTable(self):
        if len(self.tables) >= 1:
            return self.tables[len(self.tables) - 1]

    def popTable(self):
        if len(self.tables) >= 1:
            self.tables.pop()


class SymbolTable(object):

    def __init__(self, name, nest, next, label):
        self.name = name
        self.nest = nest
        self.size = 0
        self.next = next
        self.label = label
        self.entries = []

    def insertEntry(self, name, kind, type='', label='', firstOfKind = False):

        offset = 0 
        if kind in ['var', 'param']:
            size = 1
            prevOffset = self.entries[-1]["offset"] if len(self.entries) > 0 else 0
            offset = prevOffset + 4 if firstOfKind else (prevOffset + size)
            
        else:
            size = 0


        if self.find(name) is None:
            self.entries.append({"name":name, "kind":kind, "type":type, "size":size, "offset":offset, "label":label})
            self.size += size
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
        print '{0:<1s} {1:10s} {2:10s} {3:<10s} {4:32s} {0:>1s}'.format('|', self.name +"   L"+ str(self.label), 'Nest: '+ str(self.nest), 'Size: '+ str(self.size), 'Next-> '+ str(self.next))
        print '{0:1s}{1:=<67}{0:1s}'.format('+', '=')
        print '{0:<1s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {0:<1s}'.format('|', 'Name', 'Kind', 'Type', 'Size', 'Offset', 'Label')
        print '{0:1s}{1:-<67}{0:1s}'.format('+', '-')
        for entry in self.entries:
            print '{0:<1s} {1:10s} {2:10s} {3:10s} {4:<10d} {5:<10d} {6:10s} {0:<1s}'.format('|', entry['name'], entry['kind'], entry['type'], entry['size'], entry['offset'], "L"+str(entry['label']))
        print '{0:1s}{1:-<67}{0:1s}'.format('+', '-')+"\n"
