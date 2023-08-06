from dataclasses import dataclass


@dataclass
class PeripheralInformationData:

    __slots__ = 'perte', 'pert', 'par1', 'par2'

    def __init__(self, data: dict):
        self.perte = data['perTe']
        self.pert = data['perT']
        self.par1 = data['par1']
        self.par2 = data['par2']
