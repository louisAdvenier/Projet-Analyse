import pandas as pd

histDon = 'historique données bcc v02.xlsx'
ExtrQual = 'Extraction qual. sortie VIL.xlsx'

mesCL2 = pd.read_excel(histDon, sheet_name = 'Mesure CL2 sortie BCC')
debJavel = pd.read_excel(histDon, sheet_name = 'Débit de javel entrée BCC')
DN400 = pd.read_excel(histDon, sheet_name = 'Débit entrée DN400')
DN1000 = pd.read_excel(histDon, sheet_name = 'Débit entrée DN1000')
#DB409 = pd.read_excel(histDon, sheet_name = '4.09_Db')
#DB413 = pd.read_excel(histDon, sheet_name = '4.13_Db')
#DBE411 = pd.read_excel(histDon, sheet_name = '4.11_Dbe')
#DBS411 = pd.read_excel(histDon, sheet_name = '4.11_Dbs')

extrBaseQual = pd.read_excel(ExtrQual, sheet_name='Extraction base Qual.', usecols = ['Date de prélèvement', 'Heure de prélèvement', 'Paramètre', 'Résultat'])
