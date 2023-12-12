import pandas as pd
import re

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

def inletFlow(DN400, DN1000) : 
    dataFrame = pd.merge(splitDate(DN400), splitDate(DN1000), on = ['Date de prélèvement', 'Heure de prélèvement'], how = 'outer', suffixes=('_DN400', '_DN1000'))
    dataFrame.fillna(0, inplace=True)
    dataFrame['DEBIT_ENTREE (m3/h)'] = dataFrame['VALEUR (en m3/h)_DN400'] + dataFrame['VALEUR (en m3/h)_DN1000']
    del dataFrame['VALEUR (en m3/h)_DN400']
    del dataFrame['VALEUR (en m3/h)_DN1000']
    
    return dataFrame
    
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
        
