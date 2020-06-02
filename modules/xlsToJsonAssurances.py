"""Module for parsing xls restitution and calculating quantiles and risk"""

import pandas as pd
import numpy as np
from io import BytesIO

quartiles = {'Q1': [0.25, 'Peu risqué'], 'Q2': [0.50, 'Moyennement risqué'], 'Q3': [0.75, "risqué"],
             'Q4': [1, "Très risqué"]}


def Normalizer(n, som):
    """
    method for normalizing values
    :param n: values
    :param som: sum of values
    :return: normalized value n / s or 0
    """""
    return n / som if not som == 0 else 0


def Risk(n, Q1, Q2, Q3):
    """
    method for assessing risk
    :param n: values
    :param Q1: quantile 1
    :param Q2: quantile 2
    :param Q3: quantile 3
    :return: String risk value
    """
    global quartiles
    if n < Q1:
        return quartiles['Q1'][1]
    elif n < Q2:
        return quartiles['Q2'][1]
    elif n < Q3:
        return quartiles['Q3'][1]
    else:
        return quartiles['Q4'][1]


def quantilesRiskCalculator(N4, N3, N2, N1, N):
    """
    method for preparing values and calculating quantiles and risk
    :param N4: values at n-4
    :param N3: values at n-3
    :param N2: values at n-2
    :param N1: values at n-1
    :param N: values at n
    :return: numpy array for quantile 1,
     numpy array for quantile 2,
     numpy array for quantile 3,
     list of risk values String
    """
    # calculating sum
    som = np.add(np.add(N4, N3), np.add(N2, N1))
    array_n = np.array((N4, N3, N2, N1))
    # normalizing values
    array_n_normalized = np.array([[Normalizer(j, s) for j, s in zip(n, som)] for n in array_n])
    N_normalized = np.array([Normalizer(j, s) for j, s in zip(N, som)])
    # quantiles calculation
    Quantiles = []
    for i in range(4):
        Quantiles.append(np.quantile(array_n_normalized, (1 + i) * 0.25, axis=0))
    # quantiles percentage calculation
    Q_percentiles = []
    for i in range(3):
        Q_percentiles.append(np.round(np.subtract(Quantiles[i + 1], Quantiles[0]) * 100, 2))
    # risk assessment
    risque = [Risk(n, Q1, Q2, Q3) for n, Q1, Q2, Q3
              in zip(N_normalized, Quantiles[0], Quantiles[1], Quantiles[2])]
    return Q_percentiles[0], Q_percentiles[1], Q_percentiles[2], risque


def xlsToJson(input):
    """
    method for parsing xls restitution
    :param input: bytes of xls file
    :return: json dict of values + quantiles and risk
    """
    global quartiles
    df = pd.read_excel(BytesIO(input), index_col=None, header=None)

    # preparation of  the excel file

    indexesToRemove = []
    cat = ''
    for index, row in df.iterrows():
        # Select rows indexes with col0 isnull
        if pd.isna(df.iloc[index, 0]):
            indexesToRemove.append(index)
            # Select & Set Category from col1 when not all values are null
            if not pd.isna(df.iloc[index]).all():
                cat = df.iloc[index, 1]
        df.loc[index, 'Cat'] = cat
        # Select rows indexes with col1 = 'Titre'
        if df.iloc[index, 0] == 'Titre':
            indexesToRemove.append(index)
    # removing selected cols
    for i in indexesToRemove:
        df = df.drop([i])
    df = df.reset_index(drop=True)
    # reorder cols
    df = df[df.columns[[6, 0, 1, 2, 3, 4, 5]]]
    # rename cols
    df = df.rename(columns={"Cat": "Category", 0: "SubCategory", 1: "N-4", 2: "N-3", 3: "N-2", 4: "N-1", 5: "N"})

    # Quantiles calculation & risk check

    df["Q1"], df["Q2"], df["Q3"], df["Risque"] = quantilesRiskCalculator(df['N-4'].values, df['N-3'].values,
                                                                         df['N-2'].values, df['N-1'].values,
                                                                         df['N'].values)

    # JSon preparation

    # Cat = Category  subCat = subCategory

    jsonDict = {}  # will hold values of each column for the current subCat
    listSubCat = []  # will hold all subCats of a Cat & their values for each column

    # loop to populate dict with data
    for index, row in df.iterrows():
        jsonSubDict = {}
        # loop to populate row values in subdict
        for i in range(2, 11):
            jsonSubDict[(df.columns[i])] = df.iloc[index, [i]][0]
        # check at the start of df or when a new cat is selected to reinitialize the list of subCats
        if cat != df.iloc[index, [0]][0] or index == 0:
            cat = df.iloc[index, [0]][0]
            listSubCat = []
        # populate list of subcats then json dict
        listSubCat.append({df.iloc[index, [1]][0]: jsonSubDict})
        jsonDict[cat] = listSubCat

    return jsonDict
