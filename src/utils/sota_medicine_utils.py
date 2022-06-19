import pandas as pd


def convert_ndc10_to_ndc11(ndcCode):
    """
    Convert NDC10 to NDC11.
    """

    splits = ndcCode.split('-')

    codeSplits = [str(len(int)) for int in splits]
    codeSplits = "".join(codeSplits)

    code = None

    if codeSplits == '442':
        code = '0' + splits[0] + splits[1] + splits[2]

    elif codeSplits == '532':
        code = splits[0] + '0' + splits[1] + splits[2]

    elif codeSplits == '541':
        code = splits[0] + splits[1] + '0' + splits[2]
    else:
        print("error")

    return code


def convert_to_atc_using_mine(user_medicine_list, NDC_ATC_FILE):

    # Read NTC to ATC File
    ndc_atc = pd.read_csv(NDC_ATC_FILE)

    # Convert to NTC 11
    ndc_atc['NDC'] = ndc_atc['NDC'].apply(medUtils.convert_ndc10_to_ndc11)


    # Join with ndc_atc
    user_medicine_list = user_medicine_list.merge(ndc_atc, on=['NDC'])

    user_medicine_list['ATC4'] = user_medicine_list['ATC4'].map(lambda x: x[:4])
    user_medicine_list = user_medicine_list.rename(columns={'ATC4': 'ATC3'})
    user_medicine_list = user_medicine_list.drop_duplicates()

    return user_medicine_list


def convert_to_atc_using_safedrug(med_pd, rxnorm2RXCUI_file, RXCUI2atc4_file):

    with open(rxnorm2RXCUI_file, 'r') as f:
        rxnorm2RXCUI = eval(f.read())
    rxnorm2atc4 = pd.read_csv(RXCUI2atc4_file)

    med_pd['RXCUI'] = med_pd['NDC'].map(rxnorm2RXCUI)
    med_pd.dropna(inplace=True)

    rxnorm2atc4 = rxnorm2atc4.drop(columns=['YEAR', 'MONTH', 'NDC'])
    rxnorm2atc4.drop_duplicates(subset=['RXCUI'], inplace=True)
    # Dahal ATC4

    med_pd.drop(index=med_pd[med_pd['RXCUI'].isin([''])].index, axis=0, inplace=True)
    med_pd['RXCUI'] = med_pd['RXCUI'].astype('int64')
    med_pd = med_pd.reset_index(drop=True)
    med_pd = med_pd.merge(rxnorm2atc4, on=['RXCUI'])
    med_pd.drop(columns=['NDC', 'RXCUI'], inplace=True)
    med_pd['ATC4'] = med_pd['ATC4'].map(lambda x: x[:4])
    med_pd = med_pd.rename(columns={'ATC4': 'ATC3'})
    med_pd = med_pd.drop_duplicates()
    med_pd = med_pd.reset_index(drop=True)
    return med_pd
