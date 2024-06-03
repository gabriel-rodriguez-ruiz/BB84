# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 12:09:15 2024

@author: Gabriel
"""
import random

class Character:
    def __init__(self, Basis):
        self.Basis = Basis
        self.Result = None
    def __repr__(self):
        return f"({self.Basis}, {self.Result})"
        #return f"Basis: {self.Basis}"+"\n"+f"Result: {self.Result}"
    def do_measurement(self, photon_basis, photon_result):
        "Do measurement in the self.basis for a photon in Basis."
        if self.Basis==photon_basis:
            self.Result = photon_result
            return self.Result
        else:
            self.Result = random.choice([0, 1])
            return self.Result

class Alice(Character):
    def __init__(self, Basis, Result):
        super().__init__(Basis)
        self.Result = Result
    def send_to_Bob(self, Eve, Bob):
        if Eve.is_there()==True:
           self.send_to_Eve(Eve, Bob)
        else:
            Bob.Result = Bob.do_measurement(self.Basis, self.Result)
    def send_to_Eve(self, Eve, Bob):
        Eve.do_measurement(self.Basis, self.Result)
        Eve.send_to_Bob(Bob)
class Bob(Character):
    pass

class Eve(Character):
    def __init__(self, Basis, eavesdropping:bool):
        super().__init__(Basis)
        self.eavesdropping = eavesdropping
    def is_there(self):
        return self.eavesdropping
    def send_to_Bob(self, Bob):
        Bob.Result = Bob.do_measurement(self.Basis, self.Result)
