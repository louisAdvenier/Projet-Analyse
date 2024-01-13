    # Calcul du débit moyen par jour

    p_DEBIT_MOY = df[['Date de prélèvement', 'DEBIT_ENTREE (m3/h)']]

    p_DEBIT_MOY = p_DEBIT_MOY.groupby(['Date de prélèvement'], as_index=False).mean() # EQUATION

    p_DEBIT_MOY.rename(columns = {'DEBIT_ENTREE (m3/h)':'p_DEBIT_MOY (m3/h)'}, inplace = True)
    print(p_DEBIT_MOY)

    # Calcul du débit journalier p_DEBIT

    p_DEBIT = df[['Date de prélèvement', 'DEBIT_ENTREE (m3/h)']]

    p_DEBIT = p_DEBIT.groupby(['Date de prélèvement'], as_index=False).sum() # EQUATION

    p_DEBIT.rename(columns = {'DEBIT_ENTREE (m3/h)':'p_DEBIT (m3/j)'}, inplace = True)
    print(p_DEBIT)

    # Calcul de p_CLS

    p_CLS = df[['Date de prélèvement', 'MESCL2 (en mg/L)']]
    p_CLS.rename(columns = {'MESCL2 (en mg/L)':'p_CLS (mg/mL)'}, inplace = True )

    p_CLS = p_CLS.groupby(['Date de prélèvement'], as_index=False).mean()                # EQUATION => remplacer sum par mean
    p_CLS['p_CLS (g/h)'] = p_CLS['p_CLS (mg/L)'] * p_DEBIT_MOY['p_DEBIT_MOY (m3/h)']     # EQUATION

    del p_CLS['p_CLS (mg/l)']
    print(p_CLS)

    # Calcul de p_CLE

    p_CLE = df[['Date de prélèvement', 'DEBJAVEL (en L/h)']]
    p_CLE.rename(columns = {'DEBJAVEL (en L/h)':'p_Javel (L/h)'}, inplace = True )

    p_CLE = p_CLE.groupby(['Date de prélèvement'], as_index=False).mean()                # EQUATION => remplacer sum par mean
    p_CLE['p_CLE (g/h)'] = 140 * p_CLE['p_Javel (L/h)']                                 # EQUATION

    del p_CLE['p_Javel (L/h)']
    print(p_CLE)

    # Calcul de p_CLDemand

    p_CLDemand = pd.merge(p_CLS, p_CLE, on = ['Date de prélèvement'], how = 'inner')

    p_CLDemand['pCLDemand'] = p_CLE['p_CLS (g/h)'] - p_CLS['p_CLE (g/h)']              # EQUATION 

    del p_CLDemand['p_CLS (g/h)']
    del p_CLDemand['p_CLE (g/h)']
    print(p_CLDemand)

    # Calcul du temps de séjour

    journeyTime = p_DEBIT.copy() # Si on ne fait pas une copie Pandas modifie directement p_DEBIT

    journeyTime['Temps de séjour (min)'] = 2960/journeyTime['p_DEBIT (m3/j)']*24*60    # EQUATION

    del journeyTime['p_DEBIT (m3/j)']
    print(journeyTime)