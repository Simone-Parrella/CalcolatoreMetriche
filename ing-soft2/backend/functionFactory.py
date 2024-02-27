"""Modulo per fattorizzare le funzioni"""
import inspect
from .presentation_layer import compute

class FunctionFactory:
    """ classe che realizza un factory pattern per le funzioni da eseguire su richiesta
    del client le funzioni gestite da questa calsse
    sono quelle presenti nel modulo 'compute'"""
    def __init__(self):
        """ inizializza il factory pattern con le funzioni presenti nel modulo 'compute'"""
        self.functList = dict(inspect.getmembers(compute, predicate= inspect.isfunction))

    def getFunct(self, functName):
        """ ritorna la funzione con il nome specificato, se non esiste ritorna None"""
        if functName not in self.functList:
            return None
        return self.functList[functName]
    