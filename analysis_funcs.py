from Imports import *
from functions import *
from slotIdentification import slotIdent
from p_funcs import * 



def main() :
    cleansedData(extrBaseQual, mesCL2, debJavel, DN400, DN1000)

    
    


def cleansedData(extrBaseQual, mesCL2, debJavel, DN400, DN1000) :

    # ExtrQual
    
    WaterChar = dailyWaterChar(extrBaseQual)
    print("Caractéristiques de l'eau :")
    print()
    print(WaterChar)

    # histDon

    WaterData = slotIdent(mesCL2, debJavel, DN1000, DN400)
    WaterData = p_stats(WaterData)

    # Concaténation des données

    df = pd.merge(WaterChar, WaterData, on = ['Date de prélèvement'], how = 'inner')
    print(" Données finales :")
    print()
    print(df)

    print('Exportation Excel...')
    df.to_excel("Données nettoyées.xlsx")
    print('Exportation finie.')

    return df






if __name__ == '__main__' :
    main()