
class ProgramInternalForm():
    def __init__(self):
        self.__contentOfFile = []

    def add(self,token,id):
        self.__contentOfFile.append((token,id))

    def getContent(self):
        return self.__contentOfFile

    def __str__(self):
        return str(self.__contentOfFile)
