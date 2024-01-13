from Imports import *
from functions import *
from slotIdentification import slotIdent

def p_stats(df) :

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

    p_CLS = df[['Date de prélèvement', 'MESCL2 (en mg/l)']]
    p_CLS.rename(columns = {'MESCL2 (en mg/l)':'p_CLS (mg/ml)'}, inplace = True )

    p_CLS = p_CLS.groupby(['Date de prélèvement'], as_index=False).mean()                # EQUATION => remplacer sum par mean
    p_CLS['p_CLS (g/h)'] = p_CLS['p_CLS (mg/ml)'] * p_DEBIT_MOY['p_DEBIT_MOY (m3/h)']     # EQUATION

    del p_CLS['p_CLS (mg/ml)']
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

    p_CLDemand['pCLDemand (g/h)'] = p_CLE['p_CLE (g/h)'] - p_CLS['p_CLS (g/h)']              # EQUATION 

    del p_CLDemand['p_CLS (g/h)']
    del p_CLDemand['p_CLE (g/h)']
    print(p_CLDemand)

    # Calcul du temps de séjour

    journeyTime = p_DEBIT.copy() # Si on ne fait pas une copie Pandas modifie directement p_DEBIT

    journeyTime['Temps de séjour (min)'] = 2960/journeyTime['p_DEBIT (m3/j)']*24*60    # EQUATION

    del journeyTime['p_DEBIT (m3/j)']
    print(journeyTime)

    # Concaténation des DataFrames obtenus

    aggregate_df = pd.merge(p_DEBIT_MOY, p_DEBIT, on = 'Date de prélèvement', how = 'inner')
    aggregate_df = pd.merge(aggregate_df, p_CLS, on = 'Date de prélèvement', how = 'inner')
    aggregate_df = pd.merge(aggregate_df, p_CLE, on = 'Date de prélèvement', how = 'inner')
    aggregate_df = pd.merge(aggregate_df, p_CLDemand, on = 'Date de prélèvement', how = 'inner')
    aggregate_df = pd.merge(aggregate_df, journeyTime, on = 'Date de prélèvement', how = 'inner')

    print(aggregate_df)

    return aggregate_df


def main() :

    print('Run slotIdent...')
    df = slotIdent(mesCL2, debJavel, DN1000, DN400)
    print('done')
    print()

    print('Permanent regime statistics...')
    print()
    aggregate_df = p_stats(df)

    print(aggregate_df['Date de prélèvement'].dtype)
    

if __name__ == '__main__' :
    main()


