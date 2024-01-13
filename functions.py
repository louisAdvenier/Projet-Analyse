import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def main() :
    return

#######################################################################################################
# Fonctions qui concernent le fichier : 'historique données bcc v02.xlsx'                             #
#######################################################################################################

# Pour le fichier histDon, sépare l'horodate en une colonne date et une colonne heure
def splitDate(data): #VALIDEE
    # Scinder la colonne des dates
    data[['Date de prélèvement', 'Heure de prélèvement']] = data.HORODATE.str.split(" ", expand = True)
    # Supprimer l'ancienne colonne des dates
    del data['HORODATE']
    #Met les deux colonnes Date et Heure avant les valeurs
    data = data[['Heure de prélèvement'] + [col for col in data.columns if col != 'Heure de prélèvement']]
    data = data[['Date de prélèvement'] + [col for col in data.columns if col != 'Date de prélèvement']]

    return data


# Bilan instantanné sur les débits d'entrée
def instantInletFlow(DN400, DN1000) : 
    # Combine les deux dataFrames DN400 et DN1000 en les joignant sur 'Date de prélèvement' et 'Heure de prélèvement'
    dataFrame = pd.merge(splitDate(DN400), splitDate(DN1000), on = ['Date de prélèvement', 'Heure de prélèvement'], how = 'outer', suffixes=('_DN400', '_DN1000'))
    # Remplace les Nan par des 0 pour pouvoir faire des sommes
    dataFrame.fillna(0, inplace=True)
    # Somme des colonnes
    dataFrame['DEBIT_ENTREE (m3/h)'] = dataFrame['VALEUR (en m3/h)_DN400'] + dataFrame['VALEUR (en m3/h)_DN1000']
    # Suppression des colonnes inutiles
    del dataFrame['VALEUR (en m3/h)_DN400']
    del dataFrame['VALEUR (en m3/h)_DN1000']

    return dataFrame
    
def dailyInletFlow(instantInletFlow) :
    # Somme les debits d'entrée par jour
    dataFrame = instantInletFlow.groupby(['Date de prélèvement']).sum().reset_index()
    # Supprime la colonne 'Heure de prélèvement' désormais inutile
    del dataFrame['Heure de prélèvement']
    dataFrame.rename(columns={'DEBIT_ENTREE (m3/h)':'DEBIT_ENTREE (m3/j)'}, inplace = True)

    return dataFrame

def dailyChlorineDemand(mesCL2, debJavel, dailyInletFlow) :
    # Bilan journalier des sorties en CL2
    sortie_CL2 = splitDate(mesCL2)
    sortie_CL2 = sortie_CL2.groupby(['Date de prélèvement']).sum().reset_index()
    del sortie_CL2['Heure de prélèvement']
    # Bilan journalier des entrées en javel
    entree_Jav = splitDate(debJavel)
    entree_Jav = entree_Jav.groupby(['Date de prélèvement']).sum().reset_index()
    del entree_Jav['Heure de prélèvement']
    # Conversion debit journalier javel en equivalent entree CL2
    entree_Jav_col = entree_Jav['VALEUR (en L/h)']
    entree_Jav_eqCL2 = 140*entree_Jav_col/dailyInletFlow['DEBIT_ENTREE (m3/j)']
    # Conversion débit journalier sortie CL2 de mg/l en g/l
    sortie_CL2_col = sortie_CL2['VALEUR (en mg/l)']/1000
    # Creation DataFrame avec seulement les dates de prélèvement
    dataFrame = pd.DataFrame(dailyInletFlow['Date de prélèvement'])
    # Difference des deux colonnes
    dataFrame['DEMANDE_EN_CHLORE (g/m3)'] = sortie_CL2_col - entree_Jav_eqCL2

    return dataFrame

def journeyTime(DN400, DN1000) :

    dataFrame = pd.merge(splitDate(DN400), splitDate(DN1000), on = ['Date de prélèvement', 'Heure de prélèvement'], how = 'inner', suffixes=('_DN400', '_DN1000'))
    dataFrame = dataFrame.loc[(dataFrame['VALEUR (en m3/h)_DN400'] != 0) & (dataFrame['VALEUR (en m3/h)_DN1000'] != 0)]
    dataFrame['Temps de séjour (h)'] = 2960 / (dataFrame['VALEUR (en m3/h)_DN400'] + dataFrame['VALEUR (en m3/h)_DN1000'])

    print(dataFrame)

def dailyAverageJourneyTime(DN400, DN1000) :

    dataFrame = instantInletFlow(DN400, DN1000)
    dataFrame = dailyInletFlow(dataFrame)
    dataFrame['Temps de séjour (min)'] = 2960 / dataFrame['DEBIT_ENTREE (m3/j)'] * 24 * 60
    del dataFrame['DEBIT_ENTREE (m3/j)']

    print(dataFrame)


#######################################################################################################
# Fonctions qui concernent le fichier : 'Extraction qual. sortie VIL.xlsx'                            #
#######################################################################################################

# Pour le dataFrame extrBaseQual, extrait les données qui relèvent du COT
def COT(data) :
    # Récupère toutes les lignes donc le paramètre est un COT
    dataFrame = data[data['Paramètre'].str.contains('C Orga')]
    # Supprime la colonne paramètre désormais inutile
    del dataFrame['Paramètre']
    # Renomme la colonne 'Résultat' en 'COT (mg(C)/L)'
    dataFrame.rename(columns = {'Résultat':'COT (mg(C)/L)'}, inplace = True)
    
    return dataFrame  
  
# même fonction pour le pH
def pH(data) : 
    dataFrame = data[data['Paramètre'].str.contains('pH')]
    del dataFrame['Paramètre']
    dataFrame.rename(columns = {'Résultat':'pH'}, inplace = True)
    
    return dataFrame   
 
# même fonction pour la température de l'eau
def tempEau(data) :
    dataFrame = data[data['Paramètre'].str.contains('Temp. eau')]
    del dataFrame['Paramètre']
    dataFrame.rename(columns = {'Résultat':'TEMP (°C)'}, inplace = True)
    
    return dataFrame    
 
# Combine les trois DataFrame obtenus 
def dataCleanup(data) :
    # Les trois tableaux de données COT, pH et temp obtenus séparemment
    COTData = COT(data)
    pHData = pH(data)
    tempData = tempEau(data)
    # Combine les trois DataFrame précédent
    dataFrame = pd.merge(COTData, pHData, on = ['Date de prélèvement', 'Heure de prélèvement'], how = 'outer')
    dataFrame = pd.merge(dataFrame, tempData, on = ['Date de prélèvement', 'Heure de prélèvement'], how = 'outer')

    return dataFrame

# Moyenne les données sur le jour
def waterChar(data) : 
    dataFrame = pd.DataFrame(columns = ['Date de prélèvement', 'COT (mg(C)/L)', 'pH', 'TEMP (°C)'])
    print(data)
    data.sort_values(by='Date de prélèvement', inplace = True)
    print(data)
    oldDate = 0
    for date in data['Date de prélèvement'] :
        if date != oldDate : # pour ne pas répéter les entrées
            oldDate = date
            # selectionne toutes les lignes avec la même date
            selection = data.loc[data['Date de prélèvement'] == date]
            # moyenne des COT, pH et tempEau sur chaque selection
            COTMean = selection['COT (mg(C)/L)'].mean()
            pHMean = selection['pH'].mean()
            tempMean = selection['TEMP (°C)'].mean()
            # nouvelle ligne contenant les données moyennées pour la date
            newRow = pd.DataFrame([{'Date de prélèvement': date, 'COT (mg(C)/L)': COTMean, 'pH': pHMean , 'TEMP (°C)': tempMean}]) # Rem : objet de type dictionnaire lorsque entre {}
            # ajoute la nouvelle ligne au dataFrame 
            dataFrame = pd.concat([dataFrame, newRow], ignore_index=True)
            
    return dataFrame

# Fonction qui résume tout
def dailyWaterChar(extrBaseQual) :
    
    df = dataCleanup(extrBaseQual)
    df = waterChar(df)

    df['Date de prélèvement'] = df['Date de prélèvement'].astype(str)

    return df



if __name__ == '__main__' :
    main()
        
