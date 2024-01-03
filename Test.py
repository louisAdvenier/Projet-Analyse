from Imports import * 
from functions import *

# Test de splitDate | VALIDE
'''print('mesCL2 avant :')
print(mesCL2)
mesCL2 = splitDate(mesCL2)
print('mesCL2 après :')
print(mesCL2)'''

# Test de dataCleanup | VALIDE
'''print('extrBaseQual :')
print(extrBaseQual)'''

# Test de COT(), pH() et tempEau() | VALIDE
'''df = pH(extrBaseQual)
print(df)'''

# Test de dataCleanup() | VALIDE
'''df = dataCleanup(extrBaseQual)
print(df)'''

# Test de waterChar() | VALIDE
'''waterchar_df = waterChar(df)
print(waterchar_df)'''

# Test de instantInletFlow() et dailtInletFlow()| VALIDE
'''instantInletflow_df = instantInletFlow(DN400, DN1000)
print(instantInletflow_df)

dailyInletFlow_df = dailyInletFlow(instantInletflow_df)
print(dailyInletFlow_df)'''

# Test de dailyChlorineDemand() | VALIDE

'''dailyClDemand_df = dailyChlorineDemand(mesCL2, debJavel, dailyInletFlow_df) # !!! Necessite DailtInletFlow_df !!!
print(dailyClDemand_df)'''

# Test de journeyTime() | 

dailyAverageJourneyTime(DN400, DN1000)