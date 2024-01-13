import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np

from Imports import *
from functions import instantInletFlow, splitDate

# Ces fonctions ne touchent qu'à l'analyse du fichier 'historique données bcc v02.xlsx'

# On concatène les données utiles des différentes pages du fichier en un seul DataFrame
def concatenateData(mesCL2, debJavel, DN1000, DN400) :

    # On combine les données de débit
    DN = instantInletFlow(DN400, DN1000)
    df = pd.merge(DN, splitDate(mesCL2), on = ['Date de prélèvement', 'Heure de prélèvement'], how = 'inner')
    df = pd.merge(df, splitDate(debJavel), on = ['Date de prélèvement', 'Heure de prélèvement'], how = 'inner')

    # On renomme les colonnes pour plus de lisibilité
    df.rename(columns={'VALEUR (en mg/l)':'MESCL2 (en mg/l)' , 'VALEUR (en L/h)':'DEBJAVEL (en L/h)'}, inplace = True)

    # On recréé une colonne horodate, qui servira dans la fonction #slotSignal
    df['Horodate'] = pd.to_datetime(df['Date de prélèvement'] + ' ' + df['Heure de prélèvement'])

    # Les index ne correspondent pas à un ordre croissant des horodates. Et les horodates ne sont pas dans un ordre croissant.
    # Il faut trier les données de manière à avoir les deux.
        # On trie les données
    df.sort_values('Horodate', inplace = True)
        # On réinitialise les index
    df.reset_index(inplace = True)
        # Les anciens indexs sont placés dans une colonne 'Index'. On la supprime car elle ne nous sert à rien
    del df['index']

    return df

# On repère les périodes de régine permanent (i.e. de fonctionnement). 
# La difficulté réside dans l'irrégularité des mesures instannées du capteur, qui rend difficile l'identification des périodes de fonctionnement
def slotSignal(df) :
    
    # On créé une colonne 'slot', copies des valeurs de 'DEBIT_ENTREE (m3/h)'
    df['slot'] = df['DEBIT_ENTREE (m3/h)']
    # Les lignes d'une même période d'activité seront identifiés par un même entier, unique à la période, appelé 'periodID'
    df['Activity'] = ''
    df['Activity Period'] = ''
    periodID = 0
    
    # Les données de slots seront réaffectées, selon qu'elle sont inférieur ou supérieur à une valeur seuil nommée 'meter'
    meter = 200
    # Pour pouvoir distinguer entre une erreur du capteur et une réelle fin de la période de fonctionnement, nous faisons intervenir
    # une fenenêtre des données suivant le point de contrôle, de longueur 'span'. On vérifie la valeur maximale prise dans cette fenêtre.
    # Si la valeur est plus grande que le seuil, la chute de valeur est une erreur capteur. Si la valeur est plus petite, elle relève d'une cessation de fonctionnement
    span = 50
    
    for i in range(1,len(df['slot'])-span-1) :
        preVal = df.at[i-1, 'slot']
        postVal = df.at[i+1, 'slot']

        if preVal < meter and postVal < meter :
            df.at[i, 'slot'] = 0
        elif preVal < meter and postVal > meter :
            df.at[i, 'slot'] = 3000
            df.at[i, 'Activity Period'] = periodID
            df.at[i, 'Activity'] = True
        elif preVal > meter and postVal > meter :
            df.at[i, 'slot'] = 3000
            df.at[i, 'Activity Period'] = periodID
            df.at[i, 'Activity'] = True
        elif preVal > meter and postVal < meter :
            postVals = df.iloc[i+1:i+span]['slot']
            if max(postVals) > meter :
                df.at[i, 'slot'] = 3000
                df.at[i, 'Activity Period'] = periodID
                df.at[i, 'Activity'] = True
            else :
                df.at[i, 'slot'] = 0
                periodID += 1



    return df

def slotIdent(mesCL2, debJavel, DN1000, DN400) :
    
    print('Concaténation des DataFrames...')
    df = concatenateData(mesCL2, debJavel, DN1000, DN400)
    print('DataFrame concaténé :')
    print(df)
    print()

    print ('Recherche périodes régime permanent...')
    df = slotSignal(df)
    print('DataFrame identifiant les périodes de fonctionnement :')
    print(df)
    print()

    return df

def main() :

    print('Concaténation des DataFrames...')
    df = concatenateData(mesCL2, debJavel, DN1000, DN400)
    print('DataFrame concaténé :')
    print(df)
    print()

    print ('Recherche périodes régime permanent...')
    df = slotSignal(df)
    print('DataFrame identifiant les périodes de fonctionnement :')
    print(df)
    print()

    print('Exportation Excel...')
    df.to_excel("slot.xlsx")
    print('Exportation finie.')

    print("Tracé de 'DEBIT_ENTREE (m3/h)' et du créneau : ")
    plt.plot(df['Horodate'], df['DEBIT_ENTREE (m3/h)'])
    plt.plot(df['Horodate'], df['slot'], color = 'red')

    plt.show()

if __name__ == '__main__' :
    main()

    
