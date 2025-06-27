# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 12:09:15 2024

@author: Gabriel
"""
import random
import pandas as pd

class Character:
    def __init__(self, Basis):
        self.Basis = Basis
        self._Result = None
        self.Card_Number = None
        self.Measurement = None
        self.df = self.get_DataFrame()
    @property
    def Result(self):
        """Qbit, either 0 or 1."""
        return self._Result
    @Result.setter
    def Result(self, Result):
        self._Result = Result
        self.df = self.get_DataFrame()
    def __repr__(self):
        return f"({self.Basis}, {self.Result})"
        #return f"Basis: {self.Basis}"+"\n"+f"Result: {self.Result}"
    def do_measurement(self, photon_basis, photon_result):
        "Do measurement in the self.basis for a photon in Basis."
        if self.Basis==photon_basis:
            self.Result = photon_result
            return self.Result
        else:
            self.Result = random.choice(["\u24EA", "\u2460"])
            return self.Result
    def get_DataFrame(self):
        df = pd.DataFrame({"Card_Number":self.Card_Number,
                                "Measurement":self.Measurement,
                                "Basis":self.Basis, "Result":self._Result},
                               index=[0])
        return df

class Alice(Character):
    def __init__(self, Basis, Result, Card_Number, Measurement):
        super().__init__(Basis)
        self._Result = Result
        self.Card_Number = Card_Number
        self.Measurement = Measurement
        self.df = self.get_DataFrame()
    def send_to_Bob(self, Eve, Bob):
        if Eve.is_there()==True:
           self.send_to_Eve(Eve, Bob)
        else:
            Bob.Result = Bob.do_measurement(self.Basis, self.Result)
    def send_to_Eve(self, Eve, Bob):
        Eve.do_measurement(self.Basis, self.Result)
        Eve.send_to_Bob(Bob)
        
class Bob(Character):
    def __init__(self, Basis, Card_Number, Measurement):
        super().__init__(Basis)
        self.Card_Number = Card_Number
        self.Measurement = Measurement

class Eve(Character):
    def __init__(self, Basis, eavesdropping:bool):
        super().__init__(Basis)
        self.eavesdropping = eavesdropping
        self.df = self.get_DataFrame()
    def is_there(self):
        return self.eavesdropping
    def send_to_Bob(self, Bob):
        Bob.Result = Bob.do_measurement(self.Basis, self.Result)
