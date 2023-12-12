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

# Test de waterChar() | EN COURS
'''waterchar_df = waterChar(df)
print(waterchar_df)'''

# Test de inletFlow() | EN COURS
inletflow_df = inletFlow(DN400, DN1000)
print(inletflow_df)

