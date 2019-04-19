# coding=utf-8

# define Python user-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass


class duplicateNode(Error):
   """Eccezione usata quando voglio aggiungere un nodo nella struttura ma è già presente un nodo uguale"""
   pass
