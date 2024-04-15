import Sofa.Core
import numpy as np
import pandas as pd 

class data_query(Sofa.Core.Controller):
    
    def __init__(self, *a, **kw):

        Sofa.Core.Controller.__init__(self, *a, **kw)
        self.node = kw["node"]          
        self.pressure = self.node.cavity.cavityPressure        
        self.index = 0
        self.quantity = 6
        lineal = np.linspace(0, 15000, self.quantity)
        reverse = np.linspace(15000, 0, self.quantity)
        self.pressureValues = np.append(lineal, reverse, axis=0)
        self.csvFile='taller2.csv'
        self.headers = ['Pressure', 'x', 'y', 'z']
        self.data = pd.DataFrame(columns=self.headers)

    def onAnimateEndEvent(self, edict):                        
        if self.index < len(self.pressureValues):
            pressure = self.pressureValues[self.index]
            self.pressure.pressure.value = pressure
            self.index += 1            
            tipPosition_mm = 1000 * np.mean(self.node.tipROI.position.value, axis=0)
            new_row = pd.DataFrame({'Pressure': [pressure], 'x': [tipPosition_mm[0]], 'y': [tipPosition_mm[1]], 'z': [tipPosition_mm[2]]})
            self.data = pd.concat([self.data, new_row])
            print(self.data)
            self.data.to_csv(self.csvFile, index=False)

    