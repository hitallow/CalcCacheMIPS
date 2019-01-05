# Classe que simboliza um slot na memoria
class Slot(object):
    def __new__(cls, indice, tag , endByte, **kwargs):
        self = super().__new__(cls)
        self.indice = indice
        self.tag = tag
        self.endByte = endByte
        return self
    def __init__(self , indice, tag, endByte ):
        self.indice = indice
        self.tag = tag
        self.endByte = endByte


    def alterIndice(self , indice):
        self.indice = indice

    def alterTag(self , tag):
        self.tag = tag

    def printSlot(self):
        print("----------------------------------------------------")
        tag = str(hex(int(self.tag,2)))[2:].upper()
        if(self.indice != 'x'):
            ind = str(hex(int(self.indice,2)))[2:].upper()
        else:
            ind = 'X'
        endB = str(hex(int(self.endByte,2)))[2:].upper()

        print("| %s | %s | %s |"%(ind , tag, endB))
        print("----------------------------------------------------")

    def getTag(self):
        return hex(int(self.tag , 2))[2:].upper()
    def getEndB(self):
        return hex(int(self.endByte, 2))[2:].upper()
    def getInd(self):
        return hex(int(self.indice, 2))[2:].upper()
